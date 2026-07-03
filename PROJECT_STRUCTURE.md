# Project Structure & File Guide

This document describes each file and its purpose in the Multi-Agent Loan Approval System.

## Root Level Files

### 📄 `README.md`
**Purpose**: System overview and architecture guide
**Size**: ~2KB | **Type**: Documentation
- High-level architecture diagram
- Component descriptions
- Technology stack
- Project structure overview
- Evaluation checklist

### 📄 `QUICKSTART.md`
**Purpose**: Setup and running guide for evaluators
**Size**: ~3KB | **Type**: Documentation
- Installation steps
- 6-terminal startup procedure
- Sample test cases
- Troubleshooting guide
- Performance metrics

### 📄 `DEPLOYMENT.md`
**Purpose**: Production deployment guide
**Size**: ~4KB | **Type**: Documentation
- Docker/Kubernetes deployment
- Performance tuning
- Monitoring and logging
- Scaling strategies
- Security considerations
- Backup and recovery

### 📄 `EVALUATION_GUIDE.md`
**Purpose**: Comprehensive guide for evaluators
**Size**: ~6KB | **Type**: Documentation
- Evaluation criteria (5 areas)
- Live demonstration scenarios
- Scoring rubric
- Question bank (15 questions)
- Success criteria

### 📄 `PROJECT_STRUCTURE.md`
**Purpose**: This file - file-by-file description
**Size**: ~2KB | **Type**: Documentation

### 📄 `requirements.txt`
**Purpose**: Python package dependencies
**Size**: ~0.5KB | **Type**: Configuration
- All required packages with versions
- Development packages (optional)
- MCP framework dependencies

## Core Application Files

### 🔧 `app.py`
**Purpose**: Streamlit web UI for loan applications
**Size**: ~6KB | **Type**: Python (UI Layer)
**Key Functions**:
- `st.set_page_config()` - Page styling and layout
- Multi-tab interface: Apply, Dashboard, About
- Form validation and submission
- Result display with agent analysis tabs
- API integration via requests library

**How to Modify**:
- Change form fields: Edit form input sections (~line 60-80)
- Modify UI colors: Edit markdown styling (~line 15-30)
- Add new tabs: `st.radio()` and new elif blocks (~line 100+)

### 🔧 `service.py`
**Purpose**: FastAPI microservice - REST API layer
**Size**: ~4KB | **Type**: Python (Microservice)
**Key Functions**:
- `POST /applications/submit` - Main submission endpoint
- `GET /health` - Health check
- `GET /statistics` - System statistics
- `GET /workflow/info` - Workflow information
- CORS middleware configuration

**How to Modify**:
- Add new endpoint: Use @app.post() or @app.get() decorator
- Change validation logic: Modify validate_loan_application() call
- Adjust response format: Edit LoanApplicationResponse in utils/models.py

### 🔧 `orchestrator.py`
**Purpose**: LangGraph orchestration engine
**Size**: ~4KB | **Type**: Python (Orchestration)
**Key Classes**:
- `AgentState` - TypedDict defining state schema
- `LoanOrchestrator` - Main orchestrator class with graph

**Key Methods**:
- `_build_graph()` - Constructs LangGraph workflow (lines 44-58)
- `_analyze_applicant_profile()` - Node 1
- `_analyze_financial_risk()` - Node 2
- `_make_loan_decision()` - Node 3
- `_execute_compliance_action()` - Node 4
- `process_application()` - Main entry point
- `visualize_workflow()` - Prints workflow structure

**How to Modify**:
- Add stage: Create new `_node_name()` method, add to graph edges
- Change execution order: Modify workflow.add_edge() calls (~line 53-57)
- Add parallel execution: Use graph.add_conditional_edges()
- Add error handling: Wrap state updates in try-except

## Agent Files (`agents/` directory)

### 👤 `agents/applicant_profile_agent.py`
**Purpose**: Analyze applicant profile data
**Size**: ~2KB | **Type**: Python (Agent)

**Responsibilities**:
- Income stability scoring (0-100)
- Employment risk assessment (low/medium/high)
- Credit history summary
- Application completeness
- Flag identification

**Key Methods**:
- `analyze()` - Main analysis method
- `_calculate_income_stability_score()` - Age and income factors
- `_assess_employment_risk()` - Employment type evaluation
- `_generate_credit_history_summary()` - Credit narrative
- `_identify_flags()` - Issue flagging

**How to Modify**:
- Change income stability weights: Edit lines 45-60
- Add employment type: Edit EmploymentType enum (utils/models.py)
- Adjust flag thresholds: Edit _identify_flags() method
- New factor: Add to _calculate_income_stability_score()

### 💰 `agents/financial_risk_agent.py`
**Purpose**: Analyze financial risk and DTI
**Size**: ~3KB | **Type**: Python (Agent)

**Responsibilities**:
- DTI ratio calculation
- Credit score risk assessment
- Loan amount risk evaluation
- Anomaly detection (5 checks)
- Risk reasoning generation

**Key Methods**:
- `analyze()` - Main analysis
- `_calculate_dti_ratio()` - Uses amortization formula
- `_assess_credit_score_risk()` - Score-based risk
- `_detect_anomalies()` - Multi-factor anomaly detection
- `_generate_reasoning()` - Detailed explanation

**Anomaly Checks** (lines 75-90):
1. Income-loan mismatch
2. Liabilities exceed income
3. Loan tenure too short
4. Young applicant + large loan
5. Multiple high-risk factors

**How to Modify**:
- Change DTI thresholds: Edit lines 57-61
- Add anomaly check: Add to _detect_anomalies()
- Adjust credit score risk: Edit lines 65-71
- Change interest rate assumption: Edit line 14 (assumed_interest_rate)

### ✅ `agents/loan_decision_agent.py`
**Purpose**: Make final loan decision
**Size**: ~4KB | **Type**: Python (Agent)

**Responsibilities**:
- Multi-factor risk scoring
- Classification (Approve/Reject/Review)
- Confidence calculation
- Key factor extraction
- Decision explanation

**Key Methods**:
- `decide()` - Main decision method
- `_calculate_risk_score()` - Weighted scoring algorithm
- `_determine_classification()` - Hard rules + risk-based logic
- `_calculate_confidence()` - Confidence level
- `_identify_key_factors()` - Top factors extraction
- `_generate_explanation()` - Human-readable reasoning

**Risk Scoring Weights** (lines 51-88):
- Income stability: 30%
- Employment risk: 20%
- Credit score: 25%
- DTI: 15%
- Loan amount: 10%
- Other factors: 5%

**Hard Rules** (lines 91-107):
- Credit < 580 → Always Reject
- DTI > 50% → Always Reject
- Low risk + high stability + good credit → Approve

**How to Modify**:
- Change risk score weights: Edit percentage multipliers (lines 51-88)
- Add hard rule: Insert in _determine_classification() method
- Change thresholds: Edit lines 109-115 (40-70 = review)
- Modify confidence formula: Edit _calculate_confidence()

### 📋 `agents/compliance_orchestrator.py`
**Purpose**: Execute compliance actions and audit trail
**Size**: ~2KB | **Type**: Python (Agent)

**Responsibilities**:
- Action mapping (decision → action)
- Case ID generation
- Notification dispatch
- Audit logging
- Compliance summary

**Key Methods**:
- `execute_action()` - Main execution
- `_map_decision_to_action()` - Decision → action mapping
- `_generate_case_id()` - Unique ID creation
- `_send_notification()` - Notification dispatch
- `_log_notification()` - Audit logging
- `_generate_summary()` - Decision summary

**How to Modify**:
- Change case ID format: Edit _generate_case_id() (~line 28)
- Add notification channel: Edit _send_notification() (~line 31)
- Modify notification content: Edit _build_notification() (~line 45)
- Add compliance rules: Edit execute_action() (~line 13)

## MCP Server Files (`mcp_servers/` directory)

### 🔗 `mcp_servers/applicant_db_server.py`
**Purpose**: MCP server simulating applicant database
**Size**: ~1KB | **Type**: Python (MCP Server)
**Port**: 8001

**Endpoints**:
- `POST /query` - Query applicant data
- `GET /health` - Health check

**Query Types**:
- "credit_history" - Return credit metrics
- "income_verification" - Return income data
- "employment_history" - Return employment details

**How to Modify**:
- Add query type: Add elif block (~line 20)
- Change returned data: Modify data dictionaries (~lines 15-30)
- Add real database: Replace hardcoded data with DB queries

### 🔗 `mcp_servers/risk_rules_server.py`
**Purpose**: MCP server providing risk rules and regulations
**Size**: ~1KB | **Type**: Python (MCP Server)
**Port**: 8002

**Endpoints**:
- `POST /query` - Query risk rules
- `GET /regulatory_updates` - Regulatory info
- `GET /health` - Health check

**Query Types**:
- "dti_limits" - DTI thresholds
- "credit_score_minimums" - Credit requirements
- "regulatory_limits" - Regulatory caps

**How to Modify**:
- Update thresholds: Edit rules dictionaries (~lines 12-30)
- Add regulation: Edit /regulatory_updates endpoint (~line 43)
- Change limits: Modify returned values

### 🔗 `mcp_servers/decision_synthesis_server.py`
**Purpose**: MCP server storing decision audit trail
**Size**: ~2KB | **Type**: Python (MCP Server)
**Port**: 8003

**Endpoints**:
- `POST /store_decision` - Store decision record
- `GET /retrieve_decision/{case_id}` - Retrieve stored decision
- `GET /applicant_history/{applicant_id}` - Get applicant history
- `GET /statistics` - System statistics
- `GET /health` - Health check

**In-Memory Storage**: decision_store dict (simulates database)

**How to Modify**:
- Add persistence: Replace dict with database (~line 19)
- Add encryption: Encrypt sensitive fields before storing
- Change retention: Add date-based purging

## Utility Files (`utils/` directory)

### 📦 `utils/models.py`
**Purpose**: Pydantic data models for validation
**Size**: ~2KB | **Type**: Python (Models)

**Classes**:
- `LoanApplicationInput` - Application form data (10 fields)
- `ApplicantProfileOutput` - Agent 1 output
- `FinancialRiskOutput` - Agent 2 output
- `LoanDecisionOutput` - Agent 3 output
- `ComplianceActionOutput` - Agent 4 output
- `LoanApplicationResponse` - Final response

**Enums**:
- `EmploymentType` - Employment categories
- `LocationType` - Location categories

**How to Modify**:
- Add field: Add to relevant class with type annotation
- Add validation: Use @validator decorator
- Change constraints: Edit Field() parameters (ge, le, etc.)
- Add enum value: Edit EmploymentType or LocationType

### ✔️ `utils/validators.py`
**Purpose**: Input validation and DTI calculation
**Size**: ~1KB | **Type**: Python (Validation)

**Functions**:
- `validate_loan_application()` - Main validator
- `calculate_monthly_payment()` - Amortization formula

**Validation Checks**:
- Age range
- Credit score thresholds
- DTI preliminary calculation
- Loan amount sanity check
- Employment type rules
- Location-based checks

**How to Modify**:
- Add warning: Insert check in validate_loan_application()
- Change thresholds: Edit numeric comparisons
- Add new check: Add to issues or warnings lists

### ⚙️ `utils/config.py`
**Purpose**: Centralized configuration
**Size**: ~0.5KB | **Type**: Python (Configuration)

**Configuration Groups**:
- API Keys and Model settings
- Service URLs (ports 8000-8003)
- Agent settings (timeouts, retries)
- Risk thresholds
- Credit score thresholds
- DTI thresholds
- Logging

**How to Modify**:
- Change port: Edit MCP_*_URL variables
- Adjust thresholds: Edit RISK_SCORE_*, CREDIT_SCORE_*, DTI_* constants
- Change model: Edit ANTHROPIC_MODEL

### 📑 `utils/__init__.py`
**Purpose**: Package initialization
**Size**: ~0.5KB | **Type**: Python (Init)

## Test Files

### 🧪 `test_system.py`
**Purpose**: Comprehensive system test suite
**Size**: ~3KB | **Type**: Python (Test)

**Test Functions**:
- `test_agent_independence()` - Test each agent alone
- `run_tests()` - Run 4 demo scenarios
- Helper functions for test data creation

**Test Cases**:
1. **Strong Application** - Expected: Approved/Review
2. **Weak Application** - Expected: Rejected
3. **Borderline Application** - Expected: Review
4. **Self-Employed** - Expected: Review

**How to Run**:
```bash
source venv/bin/activate
python3 test_system.py
```

**Expected Output**: ~150 lines showing all decisions with explanations

## Statistics

| Category | Count | LOC |
|----------|-------|-----|
| Core Application Files | 4 | ~15K |
| Agent Files | 4 | ~11K |
| MCP Servers | 3 | ~4K |
| Utility Files | 4 | ~3K |
| Test Files | 1 | ~3K |
| Documentation | 5 | ~20K |
| **Total** | **~20** | **~56K** |

## File Modification Guide

### Scenario: Increase Approval Rate

**Approach 1: Reduce Risk Weights**
```python
# agents/loan_decision_agent.py line 65
income_stability_factor = (100 - applicant_profile.income_stability_score) / 2.5  # was 2
```

**Approach 2: Relax Approval Threshold**
```python
# agents/loan_decision_agent.py line 109
if risk_score < 50:  # was 40
    return "Approved"
```

**Approach 3: Remove Hard Rules**
```python
# agents/loan_decision_agent.py line 96 - Comment out
# if financial_risk.debt_to_income_ratio > 50:
#     return "Rejected"
```

### Scenario: Integrate Real Database

**Steps**:
1. Modify `mcp_servers/applicant_db_server.py` to use SQLAlchemy
2. Update connection string in `utils/config.py`
3. Replace hardcoded data with database queries
4. Add connection pooling for performance

**Example**:
```python
# mcp_servers/applicant_db_server.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://user:pass@host/db")
Session = sessionmaker(bind=engine)

@app.post("/query")
async def query_applicant_db(query: ApplicantDBQuery):
    session = Session()
    applicant = session.query(Applicant).filter_by(id=query.applicant_id).first()
    return ApplicantDBResponse(applicant_id=query.applicant_id, data=applicant.to_dict())
```

## Performance Considerations

| Component | Typical Time | Bottleneck |
|-----------|--------------|-----------|
| Applicant Profile Agent | 0.3s | CPU (scoring calculations) |
| Financial Risk Agent | 0.3s | CPU (DTI calculation) |
| Loan Decision Agent | 0.4s | CPU (multi-factor scoring) |
| Compliance Orchestrator | 0.2s | Network (notification dispatch) |
| Total E2E | ~1.2s | Orchestration overhead |

**Optimization Opportunities**:
- Cache applicant data in Redis
- Parallel agent execution with ProcessPoolExecutor
- Async MCP server calls
- Batch processing for high volume

---

**Last Updated**: 2024-07-03
**Total Files**: ~20
**Total Lines of Code**: ~56,000 (including documentation)
**Estimated Setup Time**: 10 minutes
**Estimated Learning Time**: 30 minutes
