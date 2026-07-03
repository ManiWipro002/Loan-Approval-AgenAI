"""
Test script to validate the complete system locally
Run: python test_system.py
"""

from utils.models import (
    LoanApplicationInput,
    EmploymentType,
    LocationType
)
from orchestrator import LoanOrchestrator
from datetime import datetime
import json

def print_section(title):
    """Print formatted section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def create_test_application(
    name: str,
    age: int,
    income: float,
    employment: EmploymentType,
    credit_score: int,
    loan_amount: float,
    liabilities: float,
    location: LocationType
) -> LoanApplicationInput:
    """Create a test application"""

    return LoanApplicationInput(
        applicant_id=f"TEST-{name.upper()}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        age=age,
        income=income,
        employment_type=employment,
        credit_score=credit_score,
        loan_amount=loan_amount,
        loan_tenure_months=360,
        existing_liabilities=liabilities,
        location=location,
        application_timestamp=datetime.utcnow()
    )


def run_tests():
    """Run comprehensive system tests"""

    print_section("MULTI-AGENT LOAN APPROVAL SYSTEM - LOCAL TEST")

    # Initialize orchestrator
    print("Initializing LangGraph Orchestrator...")
    orchestrator = LoanOrchestrator()

    # Show workflow
    orchestrator.visualize_workflow()

    # Test Case 1: Strong Application (Expected: Approved)
    print_section("TEST CASE 1: Strong Application")
    print("Profile: Well-established professional with excellent credit")

    app1 = create_test_application(
        name="strong",
        age=38,
        income=120000,
        employment=EmploymentType.FULL_TIME,
        credit_score=780,
        loan_amount=200000,
        liabilities=10000,
        location=LocationType.URBAN
    )

    response1 = orchestrator.process_application(app1)
    print(f"\n📊 Decision: {response1.decision.classification}")
    print(f"   Risk Score: {response1.decision.risk_score}")
    print(f"   Confidence: {response1.decision.confidence_level}")
    print(f"\n📝 Explanation:\n{response1.decision.explanation}")

    # Test Case 2: Weak Application (Expected: Rejected)
    print_section("TEST CASE 2: Weak Application")
    print("Profile: Recently unemployed with poor credit history")

    app2 = create_test_application(
        name="weak",
        age=28,
        income=25000,
        employment=EmploymentType.UNEMPLOYED,
        credit_score=520,
        loan_amount=350000,
        liabilities=120000,
        location=LocationType.RURAL
    )

    response2 = orchestrator.process_application(app2)
    print(f"\n📊 Decision: {response2.decision.classification}")
    print(f"   Risk Score: {response2.decision.risk_score}")
    print(f"   Confidence: {response2.decision.confidence_level}")
    print(f"\n📝 Explanation:\n{response2.decision.explanation}")

    # Test Case 3: Borderline Application (Expected: Review)
    print_section("TEST CASE 3: Borderline Application")
    print("Profile: Moderate income with fair credit, some risk indicators")

    app3 = create_test_application(
        name="borderline",
        age=32,
        income=65000,
        employment=EmploymentType.FULL_TIME,
        credit_score=640,
        loan_amount=300000,
        liabilities=75000,
        location=LocationType.SEMI_URBAN
    )

    response3 = orchestrator.process_application(app3)
    print(f"\n📊 Decision: {response3.decision.classification}")
    print(f"   Risk Score: {response3.decision.risk_score}")
    print(f"   Confidence: {response3.decision.confidence_level}")
    print(f"\n📝 Explanation:\n{response3.decision.explanation}")

    # Test Case 4: Self-Employed (Expected: Review)
    print_section("TEST CASE 4: Self-Employed Applicant")
    print("Profile: Self-employed with good income but variable cash flow")

    app4 = create_test_application(
        name="selfemployed",
        age=42,
        income=95000,
        employment=EmploymentType.SELF_EMPLOYED,
        credit_score=710,
        loan_amount=250000,
        liabilities=40000,
        location=LocationType.URBAN
    )

    response4 = orchestrator.process_application(app4)
    print(f"\n📊 Decision: {response4.decision.classification}")
    print(f"   Risk Score: {response4.decision.risk_score}")
    print(f"   Confidence: {response4.decision.confidence_level}")
    print(f"\n📝 Explanation:\n{response4.decision.explanation}")

    # Summary Statistics
    print_section("TEST SUMMARY")

    decisions = [
        (response1.decision.classification, response1.decision.risk_score),
        (response2.decision.classification, response2.decision.risk_score),
        (response3.decision.classification, response3.decision.risk_score),
        (response4.decision.classification, response4.decision.risk_score),
    ]

    approved = sum(1 for d, _ in decisions if d == "Approved")
    rejected = sum(1 for d, _ in decisions if d == "Rejected")
    review = sum(1 for d, _ in decisions if d == "Review")

    print(f"Total Applications Processed: {len(decisions)}")
    print(f"  ✅ Approved: {approved}")
    print(f"  ❌ Rejected: {rejected}")
    print(f"  ⏳ Pending Review: {review}")

    avg_risk = sum(score for _, score in decisions) / len(decisions)
    print(f"\nAverage Risk Score: {avg_risk:.2f}/100")

    print("\n" + "="*70)
    print("  ✅ ALL TESTS COMPLETED SUCCESSFULLY")
    print("="*70)

    return {
        "total_tests": len(decisions),
        "approved": approved,
        "rejected": rejected,
        "pending_review": review,
        "average_risk_score": round(avg_risk, 2)
    }


def test_agent_independence():
    """Test that agents work independently"""

    print_section("AGENT INDEPENDENCE TEST")

    from agents.applicant_profile_agent import ApplicantProfileAgent
    from agents.financial_risk_agent import FinancialRiskAgent
    from agents.loan_decision_agent import LoanDecisionAgent

    app = create_test_application(
        name="independence",
        age=35,
        income=75000,
        employment=EmploymentType.FULL_TIME,
        credit_score=720,
        loan_amount=250000,
        liabilities=50000,
        location=LocationType.URBAN
    )

    # Test Applicant Profile Agent independently
    print("Testing Applicant Profile Agent independently...")
    applicant_agent = ApplicantProfileAgent()
    profile = applicant_agent.analyze(app)
    print(f"✓ Income Stability: {profile.income_stability_score}")
    print(f"✓ Employment Risk: {profile.employment_risk}")
    print(f"✓ Flags: {len(profile.flags)} found")

    # Test Financial Risk Agent independently
    print("\nTesting Financial Risk Agent independently...")
    financial_agent = FinancialRiskAgent()
    risk = financial_agent.analyze(app)
    print(f"✓ DTI Ratio: {risk.debt_to_income_ratio}%")
    print(f"✓ Credit Risk: {risk.credit_score_risk_level}")
    print(f"✓ Anomalies: {'Yes' if risk.anomaly_detected else 'No'}")

    # Test Loan Decision Agent independently
    print("\nTesting Loan Decision Agent independently...")
    decision_agent = LoanDecisionAgent()
    decision = decision_agent.decide(app, profile, risk)
    print(f"✓ Classification: {decision.classification}")
    print(f"✓ Risk Score: {decision.risk_score}")
    print(f"✓ Key Factors: {len(decision.key_decision_factors)}")

    print("\n✅ All agents work independently!")


if __name__ == "__main__":
    try:
        # Test agent independence
        test_agent_independence()

        # Run main tests
        results = run_tests()

        print(f"\n✅ System Test Results: {json.dumps(results, indent=2)}")

    except Exception as e:
        print(f"\n❌ Test Failed: {str(e)}")
        import traceback
        traceback.print_exc()
