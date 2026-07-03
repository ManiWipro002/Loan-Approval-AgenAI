"""
FastAPI Microservice Layer
Handles HTTP requests and routes to orchestration engine
Run: python service.py
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from utils.models import LoanApplicationInput, LoanApplicationResponse
from utils.validators import validate_loan_application
from orchestrator import LoanOrchestrator
import uvicorn
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Loan Approval Microservice",
    description="Multi-Agent AI system for loan application analysis",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = LoanOrchestrator()

# In-memory application history store
application_history: list[dict] = []


@app.on_event("startup")
async def startup_event():
    """Startup event"""
    logger.info("Loan Approval Microservice starting...")
    orchestrator.visualize_workflow()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Loan Approval Microservice",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/applications/submit", response_model=LoanApplicationResponse)
async def submit_loan_application(application: LoanApplicationInput) -> LoanApplicationResponse:
    """
    Submit loan application for processing

    The system will:
    1. Validate application data
    2. Route through Applicant Profile Agent
    3. Route through Financial Risk Agent
    4. Route through Loan Decision Agent
    5. Execute Compliance Actions
    6. Return decision with explanation
    """

    logger.info(f"Received loan application: {application.applicant_id}")

    try:
        # Validate application
        validation_result = validate_loan_application(application)

        if not validation_result["is_valid"]:
            logger.warning(f"Validation failed for {application.applicant_id}: {validation_result['issues']}")
            # Continue processing, but flag for review
            if validation_result["issues"]:
                logger.error(f"Critical issues: {validation_result['issues']}")

        # Log warnings
        if validation_result["warnings"]:
            logger.warning(f"Warnings: {validation_result['warnings']}")

        logger.info(f"Initial DTI check: {validation_result['dti']}%")

        # Process through orchestration engine
        response = orchestrator.process_application(application)

        logger.info(f"Application processed: {application.applicant_id} -> {response.decision.classification}")

        # Store in history
        application_history.append({
            "applicant_id": application.applicant_id,
            "submitted_at": datetime.utcnow().isoformat(),
            "age": application.age,
            "income": application.income,
            "loan_amount": application.loan_amount,
            "credit_score": application.credit_score,
            "employment_type": application.employment_type,
            "classification": response.decision.classification,
            "risk_score": response.decision.risk_score,
            "confidence_level": response.decision.confidence_level,
            "case_id": response.compliance_action.case_id if response.compliance_action else None,
        })

        return response

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")

    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@app.get("/applications/history")
async def get_application_history():
    """Return all submitted applications with their decisions"""
    return {"applications": application_history}


@app.get("/applications/{applicant_id}/status")
async def get_application_status(applicant_id: str):
    """Get application status by applicant ID"""
    matches = [a for a in application_history if a["applicant_id"] == applicant_id]
    if not matches:
        return {
            "applicant_id": applicant_id,
            "status": "not_found",
            "message": "No application found for this ID"
        }
    latest = matches[-1]
    return {
        "applicant_id": applicant_id,
        "status": "processed",
        "classification": latest["classification"],
        "risk_score": latest["risk_score"],
        "submitted_at": latest["submitted_at"],
    }


@app.get("/statistics")
async def get_system_statistics():
    """Get system statistics"""

    return {
        "service": "Loan Approval System",
        "uptime": "running",
        "agents": [
            "Applicant Profile Agent",
            "Financial Risk Agent",
            "Loan Decision Agent",
            "Compliance Orchestrator"
        ],
        "mcp_servers": [
            "ApplicantDB (port 8001)",
            "RiskRulesDB (port 8002)",
            "DecisionSynthesis (port 8003)"
        ]
    }


@app.get("/workflow/info")
async def get_workflow_info():
    """Get workflow information"""

    return {
        "workflow_name": "Multi-Agent Loan Approval",
        "orchestrator": "LangGraph",
        "agents": 4,
        "stages": [
            {
                "name": "Applicant Profile Analysis",
                "inputs": ["age", "income", "employment_type", "credit_score"],
                "outputs": ["income_stability_score", "employment_risk", "flags"]
            },
            {
                "name": "Financial Risk Analysis",
                "inputs": ["income", "loan_amount", "existing_liabilities"],
                "outputs": ["dti_ratio", "credit_risk_level", "anomalies"]
            },
            {
                "name": "Loan Decision",
                "inputs": ["applicant_profile", "financial_risk"],
                "outputs": ["classification", "risk_score", "explanation"]
            },
            {
                "name": "Compliance & Actions",
                "inputs": ["decision", "applicant_id"],
                "outputs": ["case_id", "notification", "audit_trail"]
            }
        ]
    }


@app.get("/")
async def root():
    """Root endpoint"""

    return {
        "name": "Multi-Agent Loan Approval System",
        "version": "1.0.0",
        "endpoints": {
            "health": "GET /health",
            "submit_application": "POST /applications/submit",
            "application_status": "GET /applications/{applicant_id}/status",
            "statistics": "GET /statistics",
            "workflow_info": "GET /workflow/info"
        },
        "documentation": "http://localhost:8000/docs"
    }


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )
