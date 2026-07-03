from utils.models import LoanApplicationInput, ApplicantProfileOutput, EmploymentType
from typing import Dict, List


class ApplicantProfileAgent:
    """Agent responsible for analyzing applicant profile and determining income stability,
    employment risk, and credit history."""

    def __init__(self):
        self.name = "Applicant Profile Agent"

    def analyze(self, application: LoanApplicationInput) -> ApplicantProfileOutput:
        """Analyze applicant profile"""

        income_stability_score = self._calculate_income_stability_score(application)
        employment_risk = self._assess_employment_risk(application)
        credit_history_summary = self._generate_credit_history_summary(application)
        completeness = self._calculate_application_completeness(application)
        flags = self._identify_flags(application)

        return ApplicantProfileOutput(
            income_stability_score=income_stability_score,
            employment_risk=employment_risk,
            credit_history_summary=credit_history_summary,
            application_completeness=completeness,
            flags=flags
        )

    def _calculate_income_stability_score(self, application: LoanApplicationInput) -> float:
        """Calculate income stability score (0-100)"""
        score = 50.0

        # Age factor - peak earning years 35-55
        if 35 <= application.age <= 55:
            score += 15
        elif 25 <= application.age < 35:
            score += 5
        elif application.age > 55:
            score -= 10

        # Employment type factor
        if application.employment_type == EmploymentType.FULL_TIME:
            score += 25
        elif application.employment_type == EmploymentType.PART_TIME:
            score += 5
        elif application.employment_type == EmploymentType.SELF_EMPLOYED:
            score += 10
        elif application.employment_type == EmploymentType.UNEMPLOYED:
            score -= 50

        # Income level factor
        if 50000 <= application.income <= 150000:
            score += 10
        elif application.income > 150000:
            score += 15
        elif application.income < 30000:
            score -= 15

        return min(100, max(0, score))

    def _assess_employment_risk(self, application: LoanApplicationInput) -> str:
        """Assess employment risk: low, medium, high"""

        if application.employment_type == EmploymentType.UNEMPLOYED:
            return "high"

        if application.employment_type == EmploymentType.SELF_EMPLOYED:
            return "high" if application.age < 30 else "medium"

        if application.employment_type == EmploymentType.PART_TIME:
            return "medium"

        # Full-time employment
        if application.age > 60:
            return "medium"

        return "low"

    def _generate_credit_history_summary(self, application: LoanApplicationInput) -> str:
        """Generate credit history summary based on credit score"""

        if application.credit_score >= 750:
            return "Excellent credit history - consistent payment patterns expected"
        elif application.credit_score >= 700:
            return "Good credit history - minor delinquencies may be present"
        elif application.credit_score >= 650:
            return "Fair credit history - some payment issues noted"
        elif application.credit_score >= 580:
            return "Poor credit history - multiple delinquencies or high utilization"
        else:
            return "Very poor credit history - serious delinquencies or charge-offs"

    def _calculate_application_completeness(self, application: LoanApplicationInput) -> float:
        """Calculate application completeness percentage (0-100)"""
        completeness = 100.0

        # All required fields are present by validation, so we check for quality
        if application.age < 21:
            completeness -= 10

        if application.credit_score < 580:
            completeness -= 20

        return min(100, max(0, completeness))

    def _identify_flags(self, application: LoanApplicationInput) -> List[str]:
        """Identify any flags in applicant profile"""
        flags = []

        if application.age < 21:
            flags.append("Under-age applicant")

        if application.age > 65:
            flags.append("Near retirement age")

        if application.employment_type == EmploymentType.SELF_EMPLOYED:
            flags.append("Self-employed - requires income verification")

        if application.employment_type == EmploymentType.UNEMPLOYED:
            flags.append("Currently unemployed")

        if application.credit_score < 620:
            flags.append("Subprime credit score")

        if application.location == "rural":
            flags.append("Rural location")

        if application.existing_liabilities > application.income * 0.5:
            flags.append("High existing liabilities")

        return flags
