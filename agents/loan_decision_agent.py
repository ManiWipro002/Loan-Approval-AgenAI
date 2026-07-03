from utils.models import (
    LoanApplicationInput,
    ApplicantProfileOutput,
    FinancialRiskOutput,
    LoanDecisionOutput
)


class LoanDecisionAgent:
    """Agent responsible for synthesizing multi-agent outputs into a final
    loan decision (Approve/Reject/Review) with risk scoring and confidence."""

    def __init__(self):
        self.name = "Loan Decision Agent"

    def decide(
        self,
        application: LoanApplicationInput,
        applicant_profile: ApplicantProfileOutput,
        financial_risk: FinancialRiskOutput
    ) -> LoanDecisionOutput:
        """Make final loan decision based on all analysis"""

        risk_score = self._calculate_risk_score(application, applicant_profile, financial_risk)
        classification = self._determine_classification(
            risk_score, application, applicant_profile, financial_risk
        )
        confidence = self._calculate_confidence(risk_score, applicant_profile, financial_risk)
        key_factors = self._identify_key_factors(
            application, applicant_profile, financial_risk, classification
        )
        explanation = self._generate_explanation(
            classification, risk_score, confidence, key_factors, financial_risk
        )

        return LoanDecisionOutput(
            classification=classification,
            risk_score=risk_score,
            confidence_level=confidence,
            key_decision_factors=key_factors,
            explanation=explanation
        )

    def _calculate_risk_score(
        self,
        application: LoanApplicationInput,
        applicant_profile: ApplicantProfileOutput,
        financial_risk: FinancialRiskOutput
    ) -> float:
        """Calculate overall risk score (0-100, higher = more risky)"""

        risk_score = 50.0  # baseline

        # Applicant profile factors (lower income stability = higher risk)
        income_stability_factor = (100 - applicant_profile.income_stability_score) / 2
        risk_score += income_stability_factor * 0.3

        # Employment risk factor
        employment_risk_map = {"low": 0, "medium": 15, "high": 30}
        employment_factor = employment_risk_map.get(applicant_profile.employment_risk, 15)
        risk_score += employment_factor * 0.2

        # Credit score factor (lower score = higher risk)
        credit_score_risk_map = {"low": 5, "medium": 20, "high": 40}
        credit_factor = credit_score_risk_map.get(financial_risk.credit_score_risk_level, 20)
        risk_score += credit_factor * 0.25

        # DTI factor
        dti = financial_risk.debt_to_income_ratio
        if dti > 50:
            dti_factor = 40
        elif dti > 43:
            dti_factor = 25
        elif dti > 35:
            dti_factor = 15
        else:
            dti_factor = 5
        risk_score += dti_factor * 0.15

        # Loan amount risk factor
        loan_risk_map = {"low": 5, "medium": 15, "high": 30}
        loan_factor = loan_risk_map.get(financial_risk.loan_amount_risk, 15)
        risk_score += loan_factor * 0.1

        # Anomaly detection factor
        if financial_risk.anomaly_detected:
            risk_score += 15

        # Application completeness factor
        completeness_factor = (100 - applicant_profile.application_completeness) / 2
        risk_score += completeness_factor * 0.05

        # Normalize to 0-100
        risk_score = min(100, max(0, risk_score))
        return round(risk_score, 2)

    def _determine_classification(
        self,
        risk_score: float,
        application: LoanApplicationInput,
        applicant_profile: ApplicantProfileOutput,
        financial_risk: FinancialRiskOutput
    ) -> str:
        """Determine classification based on risk score and hard filters"""

        # Hard rejection criteria
        if application.credit_score < 580:
            return "Rejected"

        if applicant_profile.employment_risk == "high" and application.employment_type == "unemployed":
            return "Rejected"

        if financial_risk.debt_to_income_ratio > 50:
            return "Rejected"

        # Hard approval criteria
        if (risk_score < 30 and
            applicant_profile.income_stability_score > 80 and
            financial_risk.credit_score_risk_level == "low"):
            return "Approved"

        # Review criteria
        if risk_score >= 40 and risk_score <= 70:
            return "Review"

        if financial_risk.anomaly_detected:
            return "Review"

        if len(applicant_profile.flags) > 3:
            return "Review"

        # Default decision based on risk score
        if risk_score < 40:
            return "Approved"
        elif risk_score > 70:
            return "Rejected"
        else:
            return "Review"

    def _calculate_confidence(
        self,
        risk_score: float,
        applicant_profile: ApplicantProfileOutput,
        financial_risk: FinancialRiskOutput
    ) -> float:
        """Calculate confidence in decision (0-1)"""

        confidence = 0.8  # baseline

        # Reduce confidence for high-risk profiles
        if applicant_profile.application_completeness < 70:
            confidence -= 0.2

        # Reduce confidence for anomalies
        if financial_risk.anomaly_detected:
            confidence -= 0.15

        # Reduce confidence for borderline risk scores (40-70)
        if 40 <= risk_score <= 70:
            confidence -= 0.25

        # Reduce confidence for many flags
        if len(applicant_profile.flags) > 2:
            confidence -= 0.1

        # Reduce confidence for high employment risk
        if applicant_profile.employment_risk == "high":
            confidence -= 0.1

        confidence = min(1.0, max(0.2, confidence))
        return round(confidence, 2)

    def _identify_key_factors(
        self,
        application: LoanApplicationInput,
        applicant_profile: ApplicantProfileOutput,
        financial_risk: FinancialRiskOutput,
        classification: str
    ) -> list:
        """Identify key factors influencing the decision"""

        factors = []

        # Top positive factors
        if applicant_profile.income_stability_score > 70:
            factors.append(f"Strong income stability ({applicant_profile.income_stability_score})")

        if financial_risk.credit_score_risk_level == "low":
            factors.append(f"Excellent credit score ({application.credit_score})")

        if applicant_profile.employment_risk == "low":
            factors.append("Stable full-time employment")

        if financial_risk.debt_to_income_ratio < 35:
            factors.append(f"Healthy DTI ratio ({financial_risk.debt_to_income_ratio}%)")

        if financial_risk.loan_amount_risk == "low":
            factors.append("Conservative loan amount")

        # Top negative factors
        if applicant_profile.income_stability_score < 40:
            factors.append(f"Low income stability ({applicant_profile.income_stability_score})")

        if financial_risk.credit_score_risk_level == "high":
            factors.append(f"Poor credit score ({application.credit_score})")

        if applicant_profile.employment_risk == "high":
            factors.append("High employment risk")

        if financial_risk.debt_to_income_ratio > 43:
            factors.append(f"Elevated DTI ratio ({financial_risk.debt_to_income_ratio}%)")

        if financial_risk.loan_amount_risk == "high":
            factors.append("Aggressive loan amount")

        if financial_risk.anomaly_detected and financial_risk.anomaly_description:
            factors.append(f"Anomaly: {financial_risk.anomaly_description}")

        # Include flags
        for flag in applicant_profile.flags[:2]:
            factors.append(flag)

        return factors[:5] if factors else ["Standard evaluation completed"]

    def _generate_explanation(
        self,
        classification: str,
        risk_score: float,
        confidence: float,
        key_factors: list,
        financial_risk: FinancialRiskOutput
    ) -> str:
        """Generate human-readable explanation for the decision"""

        explanation = f"Loan Decision: {classification}\n"
        explanation += f"Risk Score: {risk_score}/100\n"
        explanation += f"Confidence: {confidence:.0%}\n\n"

        explanation += "Key Decision Factors:\n"
        for i, factor in enumerate(key_factors, 1):
            explanation += f"  {i}. {factor}\n"

        explanation += f"\nFinancial Analysis:\n"
        explanation += f"  • Debt-to-Income Ratio: {financial_risk.debt_to_income_ratio}%\n"
        explanation += f"  • Credit Risk Level: {financial_risk.credit_score_risk_level}\n"
        explanation += f"  • Loan Amount Risk: {financial_risk.loan_amount_risk}\n"

        if classification == "Approved":
            explanation += "\nDecision Rationale: Application meets approval criteria with "
            explanation += f"{confidence:.0%} confidence. Risk profile is acceptable.\n"

        elif classification == "Rejected":
            explanation += "\nDecision Rationale: Application fails to meet minimum approval "
            explanation += "criteria due to risk factors listed above.\n"

        else:  # Review
            explanation += "\nDecision Rationale: Application requires manual review due to "
            explanation += "borderline risk profile and/or anomalies detected.\n"

        explanation += "Next Steps: Contact lending officer for status update."

        return explanation
