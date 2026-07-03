# Quick Start Guide

This guide will get you running the Multi-Agent Loan Approval System in minutes.

## Prerequisites

- Python 3.11 or higher
- Virtual environment support
- API key from Anthropic (https://console.anthropic.com)

## Setup (5 minutes)

### 1. Create Virtual Environment

```bash
cd /home/ubuntu/Capetone_Project_Mani
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

On Windows (PowerShell):
```powershell
$env:ANTHROPIC_API_KEY = "your-api-key-here"
```

## Running the System (6 terminals)

Open 6 terminal windows/tabs and run the following in sequence:

### Terminal 1: MCP Server - ApplicantDB (Port 8001)
```bash
cd /home/ubuntu/Capetone_Project_Mani
source venv/bin/activate
python mcp_servers/applicant_db_server.py
```

Expected output:
```
Uvicorn running on http://127.0.0.1:8001
```

### Terminal 2: MCP Server - RiskRulesDB (Port 8002)
```bash
cd /home/ubuntu/Capetone_Project_Mani
source venv/bin/activate
python mcp_servers/risk_rules_server.py
```

Expected output:
```
Uvicorn running on http://127.0.0.1:8002
```

### Terminal 3: MCP Server - DecisionSynthesis (Port 8003)
```bash
cd /home/ubuntu/Capetone_Project_Mani
source venv/bin/activate
python mcp_servers/decision_synthesis_server.py
```

Expected output:
```
Uvicorn running on http://127.0.0.1:8003
```

### Terminal 4: FastAPI Microservice (Port 8000)
```bash
cd /home/ubuntu/Capetone_Project_Mani
source venv/bin/activate
python service.py
```

Expected output:
```
Uvicorn running on http://127.0.0.1:8000
API documentation available at http://127.0.0.1:8000/docs
```

### Terminal 5: Streamlit UI
```bash
cd /home/ubuntu/Capetone_Project_Mani
source venv/bin/activate
streamlit run app.py
```

Expected output:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

### Terminal 6: Test the API (Optional)
```bash
cd /home/ubuntu/Capetone_Project_Mani
source venv/bin/activate
python tests/test_api.py
```

## Using the System

### Via Streamlit UI

1. Open browser: http://localhost:8501
2. Go to "Apply for Loan" tab
3. Fill in application details
4. Click "Submit Application"
5. View decision results with agent analysis

### Via API

Submit application:
```bash
curl -X POST http://127.0.0.1:8000/applications/submit \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "APP-TEST-001",
    "age": 35,
    "income": 75000,
    "employment_type": "full-time",
    "credit_score": 720,
    "loan_amount": 250000,
    "loan_tenure_months": 360,
    "existing_liabilities": 50000,
    "location": "urban",
    "application_timestamp": "2024-01-01T00:00:00Z"
  }'
```

Check API docs: http://127.0.0.1:8000/docs

## Sample Test Cases

### Test Case 1: Likely Approval
```json
{
  "applicant_id": "APP-APPROVAL-001",
  "age": 35,
  "income": 100000,
  "employment_type": "full-time",
  "credit_score": 760,
  "loan_amount": 200000,
  "loan_tenure_months": 360,
  "existing_liabilities": 20000,
  "location": "urban",
  "application_timestamp": "2024-01-01T00:00:00Z"
}
```

Expected Decision: **Approved** (Risk Score: 25-35)

### Test Case 2: Likely Rejection
```json
{
  "applicant_id": "APP-REJECTION-001",
  "age": 28,
  "income": 30000,
  "employment_type": "self-employed",
  "credit_score": 550,
  "loan_amount": 400000,
  "loan_tenure_months": 360,
  "existing_liabilities": 100000,
  "location": "rural",
  "application_timestamp": "2024-01-01T00:00:00Z"
}
```

Expected Decision: **Rejected** (Risk Score: 75-90)

### Test Case 3: Pending Review
```json
{
  "applicant_id": "APP-REVIEW-001",
  "age": 32,
  "income": 60000,
  "employment_type": "full-time",
  "credit_score": 620,
  "loan_amount": 300000,
  "loan_tenure_months": 360,
  "existing_liabilities": 80000,
  "location": "semi-urban",
  "application_timestamp": "2024-01-01T00:00:00Z"
}
```

Expected Decision: **Review** (Risk Score: 50-65)

## Project Structure

```
capstone_project/
├── app.py                          # Streamlit UI
├── service.py                      # FastAPI microservice
├── orchestrator.py                 # LangGraph orchestration
├── agents/
│   ├── applicant_profile_agent.py
│   ├── financial_risk_agent.py
│   ├── loan_decision_agent.py
│   └── compliance_orchestrator.py
├── mcp_servers/
│   ├── applicant_db_server.py
│   ├── risk_rules_server.py
│   └── decision_synthesis_server.py
├── utils/
│   ├── models.py
│   ├── validators.py
│   └── config.py
├── requirements.txt
└── README.md
```

## Key Features Demonstration

### 1. Multi-Agent Architecture
Each agent is independently testable and modifiable:
- Applicant Profile Agent: Modify income stability calculation
- Financial Risk Agent: Adjust DTI thresholds
- Loan Decision Agent: Change classification logic
- Compliance Orchestrator: Update notification system

### 2. LangGraph Orchestration
The workflow shows clear agent coordination:
- Sequential execution with state passing
- Easy to add/remove stages
- Visualization available in orchestrator.py

### 3. Explainable Decisions
Each decision includes:
- Risk score with 0-100 scale
- Confidence level
- Key decision factors
- Detailed explanation

### 4. Live Code Modification
During evaluation, you can:
- Change agent thresholds
- Add new risk factors
- Modify decision criteria
- Update compliance actions

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port (Linux/Mac)
lsof -i :8000
kill -9 <PID>

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### API Connection Error
Ensure all 4 servers are running:
- ApplicantDB: http://127.0.0.1:8001
- RiskRulesDB: http://127.0.0.1:8002
- DecisionSynthesis: http://127.0.0.1:8003
- FastAPI Service: http://127.0.0.1:8000

### Missing Dependencies
```bash
pip install -r requirements.txt --upgrade
```

## Performance Metrics

Typical processing time: **2-5 seconds** per application
- Applicant Profile Analysis: ~0.3s
- Financial Risk Analysis: ~0.3s
- Loan Decision: ~0.4s
- Compliance Action: ~0.2s

## Next Steps

1. ✅ System is now operational
2. Try different loan applications
3. Review agent decision factors
4. Explore API documentation at /docs
5. Modify thresholds and re-test
6. Prepare for live evaluation

## Support

For issues or questions:
- Check logs in each terminal
- Review README.md for architecture details
- Examine orchestrator.py for workflow visualization
- Test MCP servers individually at their health endpoints

Good luck with your capstone evaluation! 🚀
