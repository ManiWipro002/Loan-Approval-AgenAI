from utils.models import LoanApplicationInput


def validate_loan_application(application: LoanApplicationInput) -> dict:
    """Validate loan application data and check for issues"""
    issues = []
    warnings = []

    # Age validation
    if application.age < 21:
        warnings.append("Applicant is under 21 - may require additional verification")
    if application.age > 65:
        warnings.append("Applicant is over 65 - may face tenure limitations")

    # Income validation
    if application.income < 20000:
        warnings.append("Income is below typical threshold - higher risk")
    if application.income > 500000:
        warnings.append("High income - verify source legitimacy")

    # Credit score validation
    if application.credit_score < 580:
        issues.append("Credit score below 580 - typically not approvable")
    elif application.credit_score < 620:
        warnings.append("Credit score in subprime range - requires manual review")

    # DTI preliminary check
    monthly_income = application.income / 12
    monthly_loan_payment = calculate_monthly_payment(
        application.loan_amount,
        application.loan_tenure_months,
        0.065  # assumed 6.5% interest rate
    )
    monthly_liability_payment = application.existing_liabilities / 60  # assume 5-year payoff
    total_monthly_debt = monthly_loan_payment + monthly_liability_payment
    dti = (total_monthly_debt / monthly_income) * 100

    if dti > 50:
        issues.append("Debt-to-Income ratio exceeds 50% - high risk")
    elif dti > 43:
        warnings.append("Debt-to-Income ratio above 43% - marginal")

    # Loan amount validation
    if application.loan_amount > application.income * 5:
        warnings.append("Loan amount exceeds 5x annual income")

    # Employment type
    if application.employment_type == "self-employed":
        warnings.append("Self-employed status requires income verification")
    elif application.employment_type == "unemployed":
        issues.append("Unemployed applicants cannot be approved")

    # Location-based checks
    if application.location == "rural":
        warnings.append("Rural location may affect property valuation")

    return {
        "is_valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "dti": round(dti, 2)
    }


def calculate_monthly_payment(principal: float, months: int, annual_rate: float) -> float:
    """Calculate monthly payment using amortization formula"""
    if months == 0:
        return 0
    monthly_rate = annual_rate / 12
    if monthly_rate == 0:
        return principal / months
    payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / (
        (1 + monthly_rate) ** months - 1
    )
    return payment
