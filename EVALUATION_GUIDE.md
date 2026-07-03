# Capstone Evaluation Guide

This document guides evaluators through the Multi-Agent Loan Approval System implementation and provides live demonstration scenarios.

## Evaluation Objectives

This capstone demonstrates:
1. ✅ **Agentic AI Architecture** - 4 specialized agents working together
2. ✅ **LangGraph Orchestration** - Deterministic workflow management
3. ✅ **Clear Agent Responsibilities** - Each agent has a specific domain
4. ✅ **MCP Integration** - Standardized agent communication
5. ✅ **Explainable AI** - Decisions with reasoning and audit trails
6. ✅ **Live Code Modification** - Easy to adapt during evaluation

## Quick Start for Evaluators

### Prerequisites
- Python 3.11+
- 5-10 minutes setup time
- Text editor (VS Code recommended)

### One-Command Setup
```bash
cd /home/ubuntu/Capetone_Project_Mani
python3 -m venv venv
source venv/bin/activate
pip install -q langgraph langchain anthropic pydantic fastapi uvicorn streamlit requests
```

### Run Test Suite (No Services Required)
```bash
source venv/bin/activate
python3 test_system.py
```

**Expected Output**: 4 test cases with decisions (Approved, Rejected, Review)

### Live System Demo (6 terminals)
```bash
# Terminal 1-3: Start MCP Servers
source venv/bin/activate
python3 mcp_servers/applicant_db_server.py  # Port 8001
python3 mcp_servers/risk_rules_server.py    # Port 8002
python3 mcp_servers/decision_synthesis_server.py  # Port 8003

# Terminal 4: Start FastAPI Service
python3 service.py  # Port 8000

# Terminal 5: Start Streamlit UI
streamlit run app.py  # Port 8501

# Terminal 6: Test API (optional)
curl -X GET http://127.0.0.1:8000/health
```

## Evaluation Criteria

### 1. Agentic AI Architecture (20%)

#### Demonstration
Show the 4 specialized agents:
```python
# Each agent is independently instantiated and testable
from agents.applicant_profile_agent import ApplicantProfileAgent
from agents.financial_risk_agent import FinancialRiskAgent
from agents.loan_decision_agent import LoanDecisionAgent
from agents.compliance_orchestrator import ComplianceOrchestrator

app1 = ApplicantProfileAgent()
app2 = FinancialRiskAgent()
app3 = LoanDecisionAgent()
app4 = ComplianceOrchestrator()
```

#### Key Points to Verify
- [ ] Each agent has a single, well-defined responsibility
- [ ] Agents are loosely coupled (can be tested independently)
- [ ] Clear input/output contracts for each agent
- [ ] Agents follow domain-driven design principles

#### Evaluation Questions
1. **Q: What does each agent do?**
   - **A:** See agent responsibilities in README.md
   
2. **Q: Can agents work independently?**
   - **A:** Yes, run `test_system.py` line 57+ shows independent testing

3. **Q: How do agents communicate?**
   - **A:** Through clearly defined Pydantic models (utils/models.py)

### 2. LangGraph Orchestration (25%)

#### Demonstration
```bash
# Show workflow structure
source venv/bin/activate
python3 -c "from orchestrator import LoanOrchestrator; o = LoanOrchestrator(); o.visualize_workflow()"
```

#### Expected Visualization
```
1. START → 2. Applicant Profile → 3. Financial Risk 
→ 4. Loan Decision → 5. Compliance → 6. END
```

#### Key Points to Verify
- [ ] Workflow is a DAG (Directed Acyclic Graph)
- [ ] State flows through defined edges
- [ ] Each node is a distinct agent
- [ ] State management is explicit (AgentState TypedDict)
- [ ] Orchestrator handles errors gracefully

#### Evaluation Questions
1. **Q: How is the workflow defined?**
   - **A:** See `orchestrator.py` line 54-82 (_build_graph method)

2. **Q: How is state managed?**
   - **A:** AgentState TypedDict passed through graph.invoke()

3. **Q: Can we add/remove stages?**
   - **A:** Yes, modify graph edges in _build_graph() method

### 3. Agent Responsibilities & MCP (20%)

#### Agent Breakdown

**Agent 1: Applicant Profile Agent** (agents/applicant_profile_agent.py)
- **Input**: LoanApplicationInput
- **Processing**:
  - Age-based income stability scoring
  - Employment type risk assessment
  - Credit history summary generation
  - Flag identification
- **Output**: ApplicantProfileOutput
  - income_stability_score: 0-100
  - employment_risk: low/medium/high
  - credit_history_summary: String
  - flags: List of issues

**Agent 2: Financial Risk Agent** (agents/financial_risk_agent.py)
- **Input**: LoanApplicationInput
- **Processing**:
  - DTI (Debt-to-Income) ratio calculation
  - Credit score risk assessment
  - Loan amount risk evaluation
  - Anomaly detection (5 different checks)
- **Output**: FinancialRiskOutput
  - dti_ratio: 0-100%
  - credit_score_risk_level: low/medium/high
  - loan_amount_risk: low/medium/high
  - anomaly_detected: Boolean
  - reasoning: Detailed explanation

**Agent 3: Loan Decision Agent** (agents/loan_decision_agent.py)
- **Input**: Application + outputs from agents 1&2
- **Processing**:
  - Multi-factor risk scoring algorithm
  - Hard filter criteria (credit < 580 = reject)
  - Classification logic (40-70 = review)
  - Confidence calculation
  - Key factor extraction
- **Output**: LoanDecisionOutput
  - classification: Approved/Rejected/Review
  - risk_score: 0-100
  - confidence_level: 0-1
  - key_decision_factors: List
  - explanation: String

**Agent 4: Compliance Orchestrator** (agents/compliance_orchestrator.py)
- **Input**: Decision + applicant_id
- **Processing**:
  - Action mapping (classification → action)
  - Case ID generation
  - Notification dispatch simulation
  - Audit log creation
- **Output**: ComplianceActionOutput
  - action_taken: approved/rejected/pending_review
  - notification_sent: Boolean
  - case_id: String (audit trail)
  - summary: String

#### MCP Servers

**MCP Server 1: ApplicantDB** (mcp_servers/applicant_db_server.py)
- Port: 8001
- Endpoint: `POST /query`
- Query types: credit_history, income_verification, employment_history
- Use case: Fetch applicant historical data

**MCP Server 2: RiskRulesDB** (mcp_servers/risk_rules_server.py)
- Port: 8002
- Endpoint: `POST /query`
- Query types: dti_limits, credit_score_minimums, regulatory_limits
- Use case: Query regulatory thresholds and rules

**MCP Server 3: DecisionSynthesis** (mcp_servers/decision_synthesis_server.py)
- Port: 8003
- Endpoint: `POST /store_decision`, `GET /retrieve_decision/{case_id}`
- Use case: Audit trail and decision history

#### Evaluation Questions
1. **Q: Show me the MCP servers**
   - **A:** `ls -la mcp_servers/` - 3 independent FastAPI services
   
2. **Q: How are MCP servers used?**
   - **A:** Currently simulated; can be extended with actual data sources
   
3. **Q: Can we change agent logic?**
   - **A:** Yes, edit agent files and re-run. Example: Change DTI threshold in financial_risk_agent.py line 60

### 4. Explainable AI Outputs (15%)

#### Example Decision Explanation
```
Loan Decision: Review
Risk Score: 58.75/100
Confidence: 55%

Key Decision Factors:
  1. Strong income stability (100.0)
  2. Excellent credit score (780)
  3. Stable full-time employment
  4. Healthy DTI ratio (14.31%)
  5. Conservative loan amount

Financial Analysis:
  • Debt-to-Income Ratio: 14.31%
  • Credit Risk Level: low
  • Loan Amount Risk: low

Decision Rationale: Application requires manual review 
due to borderline risk profile and/or anomalies detected.
```

#### Explainability Features
- [ ] Every decision has a numeric risk score (0-100)
- [ ] Confidence level provided (0-1 scale)
- [ ] Top 5 decision factors listed
- [ ] Detailed financial analysis included
- [ ] Plain English rationale provided
- [ ] Next steps included
- [ ] Audit trail via case ID

#### Verification
Run test and inspect output:
```bash
source venv/bin/activate
python3 test_system.py | grep -A 30 "Decision Factors"
```

### 5. Live Code Modification (10%)

#### Scenario: Change DTI Threshold

**Before:**
```python
# financial_risk_agent.py line 57
if dti > 50:
    dti_factor = 40
elif dti > 43:
    dti_factor = 25
```

**Modify to:**
```python
if dti > 45:  # Changed from 50 to 45
    dti_factor = 40
elif dti > 40:  # Changed from 43 to 40
    dti_factor = 25
```

**Re-run Test:**
```bash
source venv/bin/activate
python3 test_system.py
```

**Expected Result**: Risk scores for borderline cases will increase

#### Other Modification Examples
1. Add new anomaly detection rule (financial_risk_agent.py line 100)
2. Change credit score classification (loan_decision_agent.py line 120)
3. Add new applicant flag (applicant_profile_agent.py line 95)
4. Modify confidence calculation (loan_decision_agent.py line 165)

## Live Demonstration Scenarios

### Scenario 1: Submit High-Risk Application (5 minutes)

**Setup:**
```bash
# Terminal 1-5: Start all services
# (See Quick Start above)
```

**Demo:**
1. Open http://localhost:8501
2. Go to "Apply for Loan" tab
3. Enter:
   - Age: 25
   - Income: $30,000
   - Employment: self-employed
   - Credit Score: 550
   - Loan Amount: $400,000
   - Existing Liabilities: $100,000
4. Click Submit
5. **Expected Result**: Rejected (Risk Score > 80)
6. **Verify**: Shows key decision factors explaining why

### Scenario 2: Modify Agent & Re-test (5 minutes)

**Step 1: Edit agent**
```bash
# Edit applicant_profile_agent.py
# Change line 98: employment_type == EmploymentType.SELF_EMPLOYED from "high" to "medium"
```

**Step 2: Re-submit Same Application**
- Risk score should decrease
- Classification might change from Rejected to Review

**Key Point**: Demonstrates live code modification capability

### Scenario 3: View Agent Analysis (3 minutes)

**In Streamlit UI:**
1. Click "Agent Analysis Results" tabs
2. Show:
   - Applicant Profile tab: Income stability, employment risk, flags
   - Financial Risk tab: DTI, credit risk, anomalies
   - Compliance tab: Case ID, action, notification status
3. **Verify**: Each agent's output is clearly visible

### Scenario 4: Check API Documentation (2 minutes)

**In Browser:**
1. Open http://localhost:8000/docs
2. Show:
   - `/applications/submit` endpoint with schema
   - `/workflow/info` showing 4 agents
   - `/statistics` showing system status
3. **Try It Out**: Use Swagger UI to submit application

## Evaluation Scoring Rubric

| Criterion | Points | Excellent | Good | Fair | Poor |
|-----------|--------|-----------|------|------|------|
| Architecture | 20 | 4 independent agents, clear boundaries | 3+ agents, mostly independent | 2+ agents, some coupling | Single monolithic system |
| Orchestration | 25 | LangGraph with clear DAG, proper state mgmt | LangGraph DAG works, basic state | Basic workflow execution | Ad-hoc execution |
| Responsibilities | 20 | Each agent has 1 clear duty, MCP defined | Most agents focused, MCP described | Roles unclear | Responsibilities mixed |
| Explainability | 15 | Risk score, factors, confidence, reasoning | Risk score, factors, explanation | Basic explanation | No explanation |
| Modifiability | 10 | Easy code changes, immediate effect | Changes possible, needs restart | Changes require re-test | Very difficult to modify |
| **Total** | **100** | 90-100 | 80-89 | 70-79 | <70 |

## Question Bank for Evaluators

### Conceptual Questions

1. **What is an agentic AI system?**
   - Answer: Multiple specialized agents working together, each with a specific domain responsibility

2. **How does LangGraph differ from simple function calls?**
   - Answer: LangGraph provides explicit state management, error handling, and workflow visualization

3. **Why separate into 4 agents?**
   - Answer: Each domain (applicant profile, financial risk, decision, compliance) has different logic and data requirements

4. **What happens if an agent fails?**
   - Answer: See orchestrator.py line 84-86 - error is caught and state.error is set

5. **How is this different from rule-based systems?**
   - Answer: Agents can learn from data, adapt logic, and provide explanations vs. hard-coded rules

### Technical Questions

6. **What are the input parameters for the system?**
   - Answer: See utils/models.py LoanApplicationInput (10 parameters)

7. **How is DTI ratio calculated?**
   - Answer: `(loan_payment + liability_payment) / monthly_income * 100%` (utils/validators.py line 15)

8. **What makes a loan "Approved"?**
   - Answer: Risk score < 40, multiple positive factors, no hard rejection criteria (loan_decision_agent.py line 110)

9. **How do MCP servers work?**
   - Answer: FastAPI endpoints simulating external services (mcp_servers/*.py)

10. **Can agents run in parallel?**
    - Answer: Current implementation is sequential; could be modified for parallel execution

### Implementation Questions

11. **Show me the most complex agent algorithm**
    - Answer: Loan Decision Agent risk scoring (loan_decision_agent.py lines 50-95)

12. **How would you add a new agent?**
    - Answer: Create new agent class, add node to graph in orchestrator.py, define outputs

13. **What if we need to integrate with a real database?**
    - Answer: Replace MCP server implementations with database queries (DEPLOYMENT.md)

14. **How is this system scalable?**
    - Answer: Microservices architecture allows independent scaling, agent logic is stateless (DEPLOYMENT.md)

15. **What compliance features are included?**
    - Answer: Audit trail (case IDs), decision logs, notification dispatch, regulatory rule checking

## Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| "Port already in use" | Service still running | `lsof -i :PORT` then kill |
| "ModuleNotFoundError" | Missing dependencies | `pip install -r requirements.txt` |
| API responds slowly | MCP servers not running | Start all servers in order |
| Decision seems wrong | Threshold values outdated | Check financial_risk_agent.py thresholds |
| Streamlit UI won't load | API service not running | Verify http://localhost:8000/health |

## Success Criteria for Evaluators

✅ **You'll know the implementation is successful when:**

1. All 4 test cases in `test_system.py` complete without errors
2. Decisions have clear reasoning with risk scores
3. Agent outputs are independently testable
4. LangGraph workflow is visualized correctly
5. Streamlit UI displays decisions and agent analysis
6. Code modifications produce immediate effects
7. System responds within 5 seconds per request
8. No hard-coded decision rules (all driven by agent logic)

## Evaluation Deliverables

### What Will Be Graded
1. ✅ Working system (all 6 components functional)
2. ✅ Code quality (clean, well-organized, documented)
3. ✅ Architecture understanding (explained during walkthrough)
4. ✅ Agent independence (can modify each agent separately)
5. ✅ Decision explainability (reasoning is clear)
6. ✅ LangGraph usage (proper orchestration)

### Post-Evaluation
- Feedback form (provided separately)
- Code review notes
- Architecture assessment
- Recommendations for production deployment

## Additional Resources

- `README.md` - System overview and architecture
- `QUICKSTART.md` - Setup and running instructions
- `DEPLOYMENT.md` - Production deployment guide
- `orchestrator.py` - LangGraph implementation details
- `test_system.py` - Complete test suite
- Source code - Fully commented and modular

---

**Evaluation Duration**: ~30-45 minutes
**Setup Time**: ~10 minutes
**System Uptime**: 24/7 (all components are stateless)
