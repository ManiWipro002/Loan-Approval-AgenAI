# Multi-Agent Agentic AI Loan Approval System

A scalable, microservices-based distributed AI system that automates loan application analysis using specialized agents coordinated through LangGraph orchestration.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                          │
│                  Streamlit Chatbot UI                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                     MICROSERVICE LAYER                          │
│                   FastAPI REST Endpoints                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                  ORCHESTRATION LAYER                            │
│         LangGraph-based Orchestration Engine                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
      ┌──────────────────────┼──────────────────────┐
      │                      │                      │
┌─────▼──────┐      ┌─────────▼────────┐    ┌────▼──────────┐
│  Applicant │      │  Financial Risk  │    │  Loan Decision│
│   Profile  │      │    Analysis      │    │    Agent      │
│   Agent    │      │     Agent        │    │               │
└────────────┘      └──────────────────┘    └───────────────┘
      │                      │                      │
┌─────▼──────┐      ┌─────────▼────────┐    ┌────▼──────────┐
│ApplicantDB  │      │  RiskRulesDB     │    │DecisionSynthesis
│   Server    │      │    Server        │    │   Server
└─────────────┘      └──────────────────┘    └────────────────┘
```

## Key Components

### 1. Presentation Layer
- **Streamlit UI** (`app.py`): User-friendly chatbot interface for loan submissions

### 2. Microservice Layer  
- **FastAPI Service** (`service.py`): REST endpoints for application validation and routing

### 3. Orchestration Layer
- **LangGraph Orchestrator** (`orchestrator.py`): Workflow coordination and state management

### 4. Agent Layer (Domain-Specific)
- **Applicant Profile Agent**: Income stability, employment risk, credit history
- **Financial Risk Agent**: Debt-to-income analysis, anomaly detection
- **Loan Decision Agent**: Final classification and risk scoring
- **Compliance Orchestrator**: Action execution and notifications

### 5. Communication Layer
- **MCP Servers**: FastAPI-based agents simulating MCP protocol
  - ApplicantDB Server
  - RiskRulesDB Server
  - DecisionSynthesis Server

## Installation & Setup

```bash
# 1. Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables
export ANTHROPIC_API_KEY="your-api-key"

# 4. Start MCP Servers (in separate terminals)
python mcp_servers/applicant_db_server.py
python mcp_servers/risk_rules_server.py
python mcp_servers/decision_synthesis_server.py

# 5. Start FastAPI Service
python service.py

# 6. Start Streamlit UI (in another terminal)
streamlit run app.py
```

## Data Flow

1. **User Input**: Loan applicant submits application via Streamlit UI
2. **Validation**: FastAPI service validates and normalizes data
3. **Orchestration**: LangGraph orchestrator routes to agents
4. **Agent Analysis**: Agents fetch contextual data via MCP servers
5. **Synthesis**: Orchestrator synthesizes results via Claude LLM
6. **Decision**: Final classification and explanation returned to UI

## Input Parameters

```json
{
  "applicant_id": "APP-20241001-001",
  "age": 35,
  "income": 75000,
  "employment_type": "Full-time",
  "credit_score": 720,
  "loan_amount": 250000,
  "loan_tenure_months": 360,
  "existing_liabilities": 50000,
  "location": "urban",
  "application_timestamp": "2024-10-01T14:30:00Z"
}
```

## Agent Outputs

Each agent produces structured outputs:
- **Applicant Profile**: Income Stability Score, Employment Risk, Credit History
- **Financial Risk**: DTI Ratio, Risk Level, Anomalies, Reasoning
- **Loan Decision**: Classification, Risk Score, Confidence, Key Factors
- **Compliance**: Action Taken, Notification, Case ID, Timestamp

## Technology Stack

- **UI**: Streamlit
- **API**: FastAPI
- **Orchestration**: LangGraph, LangChain
- **MCP**: FastMCP
- **LLM**: Anthropic Claude Sonnet 4.6
- **SDK**: Anthropic Agent SDK
- **Language**: Python 3.11+

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
│   ├── validators.py
│   ├── models.py
│   └── config.py
├── requirements.txt
└── README.md
```

## Development Notes

- Each agent is loosely coupled and independently deployable
- MCP servers simulate external data sources and APIs
- LangGraph manages agent orchestration and state transitions
- Claude Sonnet 4.6 synthesizes multi-agent outputs for final decisions
- All decisions include explainability metrics and audit trails

## Evaluation Checklist

- [x] Agentic AI Architecture Implementation
- [x] LangGraph Orchestration
- [x] Clear Agent Responsibilities
- [x] MCP Server Integration
- [x] Explainable AI Outputs
- [x] Live Code Modification Capability
