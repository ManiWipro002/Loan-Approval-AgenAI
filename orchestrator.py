"""
LangGraph-based Orchestration Engine
Coordinates multi-agent workflow for loan application analysis
"""

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal
from utils.models import (
    LoanApplicationInput,
    ApplicantProfileOutput,
    FinancialRiskOutput,
    LoanDecisionOutput,
    ComplianceActionOutput,
    LoanApplicationResponse
)
from agents.applicant_profile_agent import ApplicantProfileAgent
from agents.financial_risk_agent import FinancialRiskAgent
from agents.loan_decision_agent import LoanDecisionAgent
from agents.compliance_orchestrator import ComplianceOrchestrator
from datetime import datetime
import json


class AgentState(TypedDict):
    """State managed by LangGraph orchestrator"""
    application: LoanApplicationInput
    applicant_profile: ApplicantProfileOutput | None
    financial_risk: FinancialRiskOutput | None
    loan_decision: LoanDecisionOutput | None
    compliance_action: ComplianceActionOutput | None
    error: str | None


class LoanOrchestrator:
    """Main orchestration engine using LangGraph"""

    def __init__(self):
        self.applicant_agent = ApplicantProfileAgent()
        self.financial_agent = FinancialRiskAgent()
        self.decision_agent = LoanDecisionAgent()
        self.compliance_agent = ComplianceOrchestrator()

        self.graph = self._build_graph()

    def _build_graph(self):
        """Build LangGraph workflow"""

        workflow = StateGraph(AgentState)

        # Add nodes for each agent
        workflow.add_node("applicant_profile", self._analyze_applicant_profile)
        workflow.add_node("financial_risk", self._analyze_financial_risk)
        workflow.add_node("loan_decision", self._make_loan_decision)
        workflow.add_node("compliance_action", self._execute_compliance_action)

        # Define edges (workflow connections)
        workflow.add_edge(START, "applicant_profile")
        workflow.add_edge("applicant_profile", "financial_risk")
        workflow.add_edge("financial_risk", "loan_decision")
        workflow.add_edge("loan_decision", "compliance_action")
        workflow.add_edge("compliance_action", END)

        return workflow.compile()

    def _analyze_applicant_profile(self, state: AgentState) -> AgentState:
        """Node: Analyze applicant profile"""

        try:
            profile = self.applicant_agent.analyze(state["application"])
            state["applicant_profile"] = profile
            print(f"✓ Applicant Profile Agent: Income Stability Score = {profile.income_stability_score}")
        except Exception as e:
            state["error"] = f"Applicant Profile Agent Error: {str(e)}"
            print(f"✗ Error in Applicant Profile Agent: {e}")

        return state

    def _analyze_financial_risk(self, state: AgentState) -> AgentState:
        """Node: Analyze financial risk"""

        if state["error"]:
            return state

        try:
            risk = self.financial_agent.analyze(state["application"])
            state["financial_risk"] = risk
            print(f"✓ Financial Risk Agent: DTI Ratio = {risk.debt_to_income_ratio}%")
            print(f"  Credit Risk Level = {risk.credit_score_risk_level}")
        except Exception as e:
            state["error"] = f"Financial Risk Agent Error: {str(e)}"
            print(f"✗ Error in Financial Risk Agent: {e}")

        return state

    def _make_loan_decision(self, state: AgentState) -> AgentState:
        """Node: Make loan decision"""

        if state["error"] or not state["applicant_profile"] or not state["financial_risk"]:
            return state

        try:
            decision = self.decision_agent.decide(
                state["application"],
                state["applicant_profile"],
                state["financial_risk"]
            )
            state["loan_decision"] = decision
            print(f"✓ Loan Decision Agent: Decision = {decision.classification}")
            print(f"  Risk Score = {decision.risk_score}, Confidence = {decision.confidence_level}")
        except Exception as e:
            state["error"] = f"Loan Decision Agent Error: {str(e)}"
            print(f"✗ Error in Loan Decision Agent: {e}")

        return state

    def _execute_compliance_action(self, state: AgentState) -> AgentState:
        """Node: Execute compliance actions"""

        if state["error"] or not state["loan_decision"]:
            return state

        try:
            action = self.compliance_agent.execute_action(
                state["application"].applicant_id,
                state["loan_decision"]
            )
            state["compliance_action"] = action
            print(f"✓ Compliance Orchestrator: Action = {action.action_taken}")
            print(f"  Case ID = {action.case_id}")
        except Exception as e:
            state["error"] = f"Compliance Orchestrator Error: {str(e)}"
            print(f"✗ Error in Compliance Orchestrator: {e}")

        return state

    def process_application(self, application: LoanApplicationInput) -> LoanApplicationResponse:
        """Main entry point: Process loan application through workflow"""

        print(f"\n{'='*60}")
        print(f"Processing Loan Application: {application.applicant_id}")
        print(f"{'='*60}\n")

        # Initialize state
        initial_state: AgentState = {
            "application": application,
            "applicant_profile": None,
            "financial_risk": None,
            "loan_decision": None,
            "compliance_action": None,
            "error": None
        }

        # Execute graph
        final_state = self.graph.invoke(initial_state)

        # Build response
        response = self._build_response(final_state)

        print(f"\n{'='*60}")
        print(f"Final Decision: {response.decision.classification}")
        print(f"Risk Score: {response.decision.risk_score}/100")
        print(f"{'='*60}\n")

        return response

    def _build_response(self, state: AgentState) -> LoanApplicationResponse:
        """Build final response from state"""

        if state["error"]:
            return LoanApplicationResponse(
                applicant_id=state["application"].applicant_id,
                application_status="error",
                decision=LoanDecisionOutput(
                    classification="Review",
                    risk_score=75.0,
                    confidence_level=0.3,
                    key_decision_factors=["System error - requires manual review"],
                    explanation="Processing error occurred. Manual review required."
                ),
                error_message=state["error"],
                processing_timestamp=datetime.utcnow()
            )

        return LoanApplicationResponse(
            applicant_id=state["application"].applicant_id,
            application_status="success",
            decision=state["loan_decision"],
            applicant_profile=state["applicant_profile"],
            financial_risk=state["financial_risk"],
            compliance_action=state["compliance_action"],
            processing_timestamp=datetime.utcnow()
        )

    def visualize_workflow(self):
        """Print workflow structure"""

        print("\n" + "="*60)
        print("LOAN APPROVAL WORKFLOW")
        print("="*60)
        print("\n1. START")
        print("   ↓")
        print("2. Applicant Profile Agent")
        print("   - Income Stability Score")
        print("   - Employment Risk Assessment")
        print("   - Credit History Summary")
        print("   - Application Flags")
        print("   ↓")
        print("3. Financial Risk Agent")
        print("   - Debt-to-Income Ratio")
        print("   - Credit Score Risk Level")
        print("   - Loan Amount Risk Assessment")
        print("   - Anomaly Detection")
        print("   ↓")
        print("4. Loan Decision Agent")
        print("   - Classification (Approve/Reject/Review)")
        print("   - Risk Scoring")
        print("   - Confidence Assessment")
        print("   - Decision Factors & Explanation")
        print("   ↓")
        print("5. Compliance Orchestrator")
        print("   - Action Execution")
        print("   - Notification System")
        print("   - Audit Trail & Case ID")
        print("   ↓")
        print("6. END - Response to Microservice")
        print("\n" + "="*60 + "\n")
