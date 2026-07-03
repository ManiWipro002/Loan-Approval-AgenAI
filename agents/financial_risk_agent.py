from utils.models import LoanApplicationInput, FinancialRiskOutput
from utils.validators import calculate_monthly_payment
from typing import Tuple


class FinancialRiskAgent:
    """Agent responsible for analyzing financial risk including DTI ratio,
    credit score risk, loan amount risk, and anomaly detection."""

    def __init__(self):
        self.name = "Financial Risk Agent"
        self.assumed_interest_rate = 0.065  # 6.5% annual

    def analyze(self, application: LoanApplicationInput) -> FinancialRiskOutput:
        """Analyze financial risk"""

        dti_ratio = self._calculate_dti_ratio(application)
        credit_risk = self._assess_credit_score_risk(application)
        loan_risk = self._assess_loan_amount_risk(application)
        anomaly_detected, anomaly_desc = self._detect_anomalies(application)
        reasoning = self._generate_reasoning(
            dti_ratio, credit_risk, loan_risk, anomaly_detected, anomaly_desc
        )

        return FinancialRiskOutput(
            debt_to_income_ratio=dti_ratio,
            credit_score_risk_level=credit_risk,
            loan_amount_risk=loan_risk,
            anomaly_detected=anomaly_detected,
            anomaly_description=anomaly_desc,
            reasoning=reasoning
        )

    def _calculate_dti_ratio(self, application: LoanApplicationInput) -> float:
        """Calculate debt-to-income ratio"""

        monthly_income = application.income / 12

        if monthly_income == 0:
            return 100.0

        # Calculate proposed loan payment
        monthly_loan_payment = calculate_monthly_payment(
            application.loan_amount,
            application.loan_tenure_months,
            self.assumed_interest_rate
        )

        # Calculate existing liability payment (assume 5-year payoff)
        monthly_liability_payment = (
            application.existing_liabilities / 60 if application.existing_liabilities > 0 else 0
        )

        total_monthly_debt = monthly_loan_payment + monthly_liability_payment
        dti = (total_monthly_debt / monthly_income) * 100

        return round(min(100.0, dti), 2)

    def _assess_credit_score_risk(self, application: LoanApplicationInput) -> str:
        """Assess credit score risk: low, medium, high"""

        if application.credit_score >= 740:
            return "low"
        elif application.credit_score >= 670:
            return "medium"
        else:
            return "high"

    def _assess_loan_amount_risk(self, application: LoanApplicationInput) -> str:
        """Assess loan amount risk relative to income"""

        loan_to_income_ratio = application.loan_amount / application.income

        if loan_to_income_ratio <= 3:
            return "low"
        elif loan_to_income_ratio <= 5:
            return "medium"
        else:
            return "high"

    def _detect_anomalies(self, application: LoanApplicationInput) -> Tuple[bool, str]:
        """Detect financial anomalies"""

        anomalies = []

        # Very low income with high loan request
        if application.income < 30000 and application.loan_amount > 200000:
            anomalies.append("Income-loan mismatch (very high loan for income level)")

        # Very high existing liabilities
        if application.existing_liabilities > application.income:
            anomalies.append("Existing liabilities exceed annual income")

        # Unusual loan tenure
        if application.loan_tenure_months < 12 and application.loan_amount > 100000:
            anomalies.append("Very short tenure for large loan amount")

        # Young age with very high loan request
        if application.age < 25 and application.loan_amount > 500000:
            anomalies.append("Young applicant requesting very large loan")

        # Multiple high-risk factors
        if (application.credit_score < 600 and
            application.existing_liabilities > 50000 and
            application.loan_amount > 300000):
            anomalies.append("Multiple high-risk factors present")

        if anomalies:
            return True, "; ".join(anomalies)
        return False, None

    def _generate_reasoning(
        self,
        dti: float,
        credit_risk: str,
        loan_risk: str,
        anomaly_detected: bool,
        anomaly_desc: str
    ) -> str:
        """Generate detailed reasoning for financial risk assessment"""

        reasoning_parts = []

        reasoning_parts.append(f"DTI Ratio: {dti}%")

        if dti > 50:
            reasoning_parts.append("- DTI exceeds safe limit (>50%), indicating potential repayment difficulty")
        elif dti > 43:
            reasoning_parts.append("- DTI is elevated (>43%), marginally acceptable")
        else:
            reasoning_parts.append("- DTI is within acceptable range")

        reasoning_parts.append(f"Credit Risk: {credit_risk}")
        if credit_risk == "high":
            reasoning_parts.append("- Credit score indicates history of delinquencies or payment issues")
        elif credit_risk == "medium":
            reasoning_parts.append("- Credit score shows acceptable history with room for improvement")

        reasoning_parts.append(f"Loan Amount Risk: {loan_risk}")
        if loan_risk == "high":
            reasoning_parts.append("- Loan amount is 5x+ annual income, indicating high risk")
        elif loan_risk == "medium":
            reasoning_parts.append("- Loan amount is 3-5x annual income")

        if anomaly_detected:
            reasoning_parts.append(f"Anomalies Detected: {anomaly_desc}")

        return "\n".join(reasoning_parts)
