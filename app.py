"""
Streamlit Chatbot UI for Loan Application Submission
Run: streamlit run app.py
"""

import streamlit as st
import requests
from datetime import datetime
from utils.models import EmploymentType, LocationType
import json

# Page configuration
st.set_page_config(
    page_title="Loan Approval System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
    <style>
    .header {
        background: linear-gradient(to right, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .decision-approved {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 15px;
        border-radius: 5px;
    }
    .decision-rejected {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 15px;
        border-radius: 5px;
    }
    .decision-review {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 15px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://127.0.0.1:8000"

st.markdown("""
    <div class="header">
        <h1>🏦 Multi-Agent Loan Approval System</h1>
        <p>Intelligent automated loan application analysis powered by AI agents</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.title("Navigation")
    page = st.radio(
        "Select Page",
        ["Apply for Loan", "Application History", "Dashboard", "About"]
    )

if page == "Apply for Loan":
    st.subheader("Loan Application Form")

    # Create two columns for form
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Applicant Information")
        applicant_id = st.text_input(
            "Applicant ID",
            value="APP-" + datetime.now().strftime("%Y%m%d%H%M%S"),
            help="Unique identifier for the applicant"
        )
        age = st.number_input("Age", min_value=18, max_value=100, value=35)
        employment_type = st.selectbox(
            "Employment Type",
            [e.value for e in EmploymentType]
        )
        location = st.selectbox(
            "Location",
            [l.value for l in LocationType]
        )

    with col2:
        st.markdown("### Financial Information")
        income = st.number_input(
            "Annual Income ($)",
            min_value=1000,
            max_value=1000000,
            value=75000,
            step=5000
        )
        credit_score = st.slider(
            "Credit Score",
            min_value=300,
            max_value=850,
            value=720
        )
        existing_liabilities = st.number_input(
            "Existing Liabilities ($)",
            min_value=0,
            max_value=500000,
            value=50000,
            step=5000
        )

    st.markdown("### Loan Details")
    col3, col4 = st.columns(2)

    with col3:
        loan_amount = st.number_input(
            "Loan Amount ($)",
            min_value=1000,
            max_value=1000000,
            value=250000,
            step=10000
        )

    with col4:
        loan_tenure_months = st.number_input(
            "Loan Tenure (Months)",
            min_value=6,
            max_value=600,
            value=360
        )

    # Submit button
    if st.button("Submit Application", key="submit_btn", type="primary"):
        st.info("Processing your application with AI agents...")

        # Prepare application data
        application_data = {
            "applicant_id": applicant_id,
            "age": age,
            "income": income,
            "employment_type": employment_type,
            "credit_score": credit_score,
            "loan_amount": loan_amount,
            "loan_tenure_months": loan_tenure_months,
            "existing_liabilities": existing_liabilities,
            "location": location,
            "application_timestamp": datetime.utcnow().isoformat() + "Z"
        }

        try:
            # Submit to API
            response = requests.post(
                f"{API_BASE_URL}/applications/submit",
                json=application_data,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()

                st.success("Application processed successfully!")

                # Display decision with styling
                decision = result["decision"]
                classification = decision["classification"]

                if classification == "Approved":
                    st.markdown(
                        f"""
                        <div class="decision-approved">
                            <h3>✅ Application Approved</h3>
                            <p><strong>Decision:</strong> Your loan application has been approved!</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                elif classification == "Rejected":
                    st.markdown(
                        f"""
                        <div class="decision-rejected">
                            <h3>❌ Application Rejected</h3>
                            <p><strong>Decision:</strong> Unfortunately, your loan application has been rejected.</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:  # Review
                    st.markdown(
                        f"""
                        <div class="decision-review">
                            <h3>⏳ Pending Manual Review</h3>
                            <p><strong>Decision:</strong> Your application requires manual review by a lending officer.</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                # Display decision details
                st.markdown("### Decision Details")
                col_a, col_b, col_c = st.columns(3)

                with col_a:
                    st.metric("Risk Score", f"{decision['risk_score']}/100")

                with col_b:
                    st.metric("Confidence", f"{decision['confidence_level']:.0%}")

                with col_c:
                    st.metric("Status", classification)

                # Key factors
                st.markdown("### Key Decision Factors")
                for factor in decision["key_decision_factors"]:
                    st.write(f"• {factor}")

                # Detailed explanation
                st.markdown("### Detailed Explanation")
                st.text(decision["explanation"])

                # Agent Analysis Results (Tabs)
                if result.get("applicant_profile") or result.get("financial_risk"):
                    st.markdown("### Agent Analysis Results")

                    tab1, tab2, tab3 = st.tabs(
                        ["Applicant Profile", "Financial Risk", "Compliance"]
                    )

                    with tab1:
                        if result.get("applicant_profile"):
                            profile = result["applicant_profile"]
                            col_p1, col_p2 = st.columns(2)
                            with col_p1:
                                st.metric(
                                    "Income Stability Score",
                                    f"{profile['income_stability_score']:.1f}/100"
                                )
                            with col_p2:
                                st.metric(
                                    "Employment Risk",
                                    profile['employment_risk'].upper()
                                )
                            st.write(f"**Credit History:** {profile['credit_history_summary']}")
                            st.write(f"**Completeness:** {profile['application_completeness']:.1f}%")
                            if profile["flags"]:
                                st.write("**Flags:**")
                                for flag in profile["flags"]:
                                    st.write(f"  ⚠️ {flag}")

                    with tab2:
                        if result.get("financial_risk"):
                            risk = result["financial_risk"]
                            col_r1, col_r2, col_r3 = st.columns(3)
                            with col_r1:
                                st.metric("DTI Ratio", f"{risk['debt_to_income_ratio']:.1f}%")
                            with col_r2:
                                st.metric("Credit Risk", risk['credit_score_risk_level'].upper())
                            with col_r3:
                                st.metric("Loan Risk", risk['loan_amount_risk'].upper())
                            if risk["anomaly_detected"]:
                                st.warning(f"Anomaly: {risk['anomaly_description']}")
                            st.write("**Analysis:**")
                            st.text(risk["reasoning"])

                    with tab3:
                        if result.get("compliance_action"):
                            compliance = result["compliance_action"]
                            st.write(f"**Action Taken:** {compliance['action_taken'].upper()}")
                            st.write(f"**Case ID:** {compliance['case_id']}")
                            st.write(f"**Notification Sent:** {'✅ Yes' if compliance['notification_sent'] else '❌ No'}")
                            st.write("**Summary:**")
                            st.text(compliance["summary"])

            else:
                st.error(f"API Error: {response.status_code}")
                st.json(response.json())

        except requests.exceptions.ConnectionError:
            st.error(
                "⚠️ Cannot connect to API service. Make sure to run: `python service.py`"
            )
        except Exception as e:
            st.error(f"Error: {str(e)}")


elif page == "Application History":
    st.subheader("Application History")

    try:
        history_response = requests.get(f"{API_BASE_URL}/applications/history", timeout=10)

        if history_response.status_code == 200:
            applications = history_response.json().get("applications", [])

            if not applications:
                st.info("No applications submitted yet. Submit one from the 'Apply for Loan' page.")
            else:
                # Summary metrics
                total = len(applications)
                approved = sum(1 for a in applications if a["classification"] == "Approved")
                rejected = sum(1 for a in applications if a["classification"] == "Rejected")
                review = sum(1 for a in applications if a["classification"] == "Review")

                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Total Applications", total)
                col2.metric("Approved", approved)
                col3.metric("Rejected", rejected)
                col4.metric("Under Review", review)

                st.markdown("---")

                # Status filter
                status_filter = st.selectbox(
                    "Filter by Status",
                    ["All", "Approved", "Rejected", "Review"]
                )

                filtered = applications if status_filter == "All" else [
                    a for a in applications if a["classification"] == status_filter
                ]

                # Table
                for app_record in reversed(filtered):
                    classification = app_record["classification"]
                    badge = {"Approved": "✅", "Rejected": "❌", "Review": "⏳"}.get(classification, "")
                    css_class = {"Approved": "decision-approved", "Rejected": "decision-rejected", "Review": "decision-review"}.get(classification, "")

                    with st.expander(
                        f"{badge} {app_record['applicant_id']} — {classification}  |  Risk: {app_record['risk_score']}/100  |  {app_record['submitted_at'][:19].replace('T', ' ')} UTC",
                        expanded=False
                    ):
                        c1, c2, c3, c4 = st.columns(4)
                        c1.metric("Risk Score", f"{app_record['risk_score']}/100")
                        c2.metric("Confidence", f"{app_record['confidence_level']:.0%}")
                        c3.metric("Income", f"${app_record['income']:,}")
                        c4.metric("Loan Amount", f"${app_record['loan_amount']:,}")

                        d1, d2, d3 = st.columns(3)
                        d1.write(f"**Age:** {app_record['age']}")
                        d2.write(f"**Credit Score:** {app_record['credit_score']}")
                        d3.write(f"**Employment:** {app_record['employment_type']}")

                        if app_record.get("case_id"):
                            st.write(f"**Case ID:** `{app_record['case_id']}`")

        else:
            st.error(f"Failed to load history: {history_response.status_code}")

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to API service. Make sure to run: `python service.py`")
    except Exception as e:
        st.error(f"Error: {str(e)}")


elif page == "Dashboard":
    st.subheader("System Dashboard")

    try:
        # Fetch system statistics
        health_response = requests.get(f"{API_BASE_URL}/health")
        stats_response = requests.get(f"{API_BASE_URL}/statistics")
        workflow_response = requests.get(f"{API_BASE_URL}/workflow/info")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("System Status", "🟢 Healthy")

        with col2:
            st.metric("Service", "Loan Approval")

        with col3:
            st.metric("Agents", "4 Active")

        # System Information
        st.markdown("### System Configuration")
        if stats_response.status_code == 200:
            stats = stats_response.json()
            col_s1, col_s2 = st.columns(2)

            with col_s1:
                st.write("**Active Agents:**")
                for agent in stats.get("agents", []):
                    st.write(f"  ✓ {agent}")

            with col_s2:
                st.write("**MCP Servers:**")
                for server in stats.get("mcp_servers", []):
                    st.write(f"  ✓ {server}")

        # Workflow stages
        if workflow_response.status_code == 200:
            workflow = workflow_response.json()
            st.markdown("### Workflow Stages")

            for i, stage in enumerate(workflow["stages"], 1):
                with st.expander(f"Stage {i}: {stage['name']}", expanded=False):
                    col_in, col_out = st.columns(2)
                    with col_in:
                        st.write("**Inputs:**")
                        for inp in stage["inputs"]:
                            st.write(f"  • {inp}")
                    with col_out:
                        st.write("**Outputs:**")
                        for out in stage["outputs"]:
                            st.write(f"  • {out}")

    except Exception as e:
        st.error(f"Could not load dashboard: {str(e)}")


else:  # About
    st.subheader("About This System")

    st.markdown("""
    ## Multi-Agent Agentic AI Loan Approval System

    This system demonstrates a modern distributed AI architecture for automating loan approvals
    using specialized agents coordinated through LangGraph orchestration.

    ### Architecture Components

    **1. Presentation Layer**
    - Streamlit-based UI for easy loan submission and status tracking

    **2. Microservice Layer**
    - FastAPI service handling HTTP requests and validation

    **3. Orchestration Layer**
    - LangGraph engine coordinating agent workflows
    - Deterministic state management

    **4. Agent Layer** (4 specialized agents)
    - **Applicant Profile Agent**: Income stability, employment risk, credit history
    - **Financial Risk Agent**: DTI analysis, anomaly detection
    - **Loan Decision Agent**: Classification and risk scoring
    - **Compliance Orchestrator**: Actions and audit trails

    **5. Communication Layer**
    - MCP-style servers for data access
    - ApplicantDB, RiskRulesDB, DecisionSynthesis

    ### Key Features

    ✅ **Explainable Decisions**: All decisions include reasoning and key factors

    ✅ **Risk Scoring**: Quantified risk assessment (0-100)

    ✅ **Multi-Agent Coordination**: Specialized agents for different domains

    ✅ **Audit Trail**: Complete case tracking and compliance records

    ✅ **Scalable**: Microservices architecture for easy deployment

    ### Technology Stack

    - **UI**: Streamlit
    - **API**: FastAPI
    - **Orchestration**: LangGraph, LangChain
    - **MCP**: FastMCP-style servers
    - **LLM**: Anthropic Claude Sonnet 4.6
    - **Language**: Python 3.11+

    ### Decision Classifications

    🟢 **Approved**: Application meets all criteria with low risk

    🔴 **Rejected**: Application fails hard criteria (credit score, DTI, etc.)

    🟡 **Review**: Application requires manual review by lending officer

    ### How It Works

    1. User submits application via Streamlit UI
    2. FastAPI validates and normalizes data
    3. LangGraph orchestrator routes through agents
    4. Agents analyze data from MCP servers
    5. Final decision synthesized with Claude LLM
    6. Response returned with explanation

    """)

    st.markdown("---")
    st.markdown("""
    **Project**: Capstone - Multi-Agent Agentic AI System

    **Status**: Production-Ready

    **Version**: 1.0.0
    """)
