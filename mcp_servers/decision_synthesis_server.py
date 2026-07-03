"""
MCP Server simulating DecisionSynthesis - stores and retrieves decision records
Run: python mcp_servers/decision_synthesis_server.py
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn
from datetime import datetime

app = FastAPI(title="DecisionSynthesis MCP Server")

# In-memory storage for demonstration
decision_store = {}


class DecisionRecord(BaseModel):
    applicant_id: str
    decision: str
    risk_score: float
    confidence: float
    case_id: str
    timestamp: str


class StoreDecisionRequest(BaseModel):
    applicant_id: str
    decision: str
    risk_score: float
    confidence: float
    case_id: str


@app.post("/store_decision")
async def store_decision(request: StoreDecisionRequest) -> dict:
    """Store decision record for audit trail"""

    record = DecisionRecord(
        applicant_id=request.applicant_id,
        decision=request.decision,
        risk_score=request.risk_score,
        confidence=request.confidence,
        case_id=request.case_id,
        timestamp=datetime.utcnow().isoformat()
    )

    decision_store[request.case_id] = record.dict()

    return {
        "status": "stored",
        "case_id": request.case_id,
        "applicant_id": request.applicant_id,
        "decision": request.decision
    }


@app.get("/retrieve_decision/{case_id}")
async def retrieve_decision(case_id: str) -> dict:
    """Retrieve stored decision"""

    if case_id not in decision_store:
        raise HTTPException(status_code=404, detail=f"Case {case_id} not found")

    return decision_store[case_id]


@app.get("/applicant_history/{applicant_id}")
async def get_applicant_history(applicant_id: str) -> dict:
    """Get all decisions for applicant"""

    history = [
        record for record in decision_store.values()
        if record["applicant_id"] == applicant_id
    ]

    if not history:
        return {
            "applicant_id": applicant_id,
            "decisions": [],
            "total_applications": 0
        }

    return {
        "applicant_id": applicant_id,
        "decisions": history,
        "total_applications": len(history),
        "latest_decision": max(history, key=lambda x: x["timestamp"])
    }


@app.get("/statistics")
async def get_statistics():
    """Get decision statistics"""

    total_decisions = len(decision_store)
    approved = sum(1 for r in decision_store.values() if r["decision"] == "Approved")
    rejected = sum(1 for r in decision_store.values() if r["decision"] == "Rejected")
    review = sum(1 for r in decision_store.values() if r["decision"] == "Review")

    avg_confidence = (
        sum(r["confidence"] for r in decision_store.values()) / total_decisions
        if total_decisions > 0 else 0
    )
    avg_risk = (
        sum(r["risk_score"] for r in decision_store.values()) / total_decisions
        if total_decisions > 0 else 0
    )

    return {
        "total_decisions": total_decisions,
        "approved": approved,
        "rejected": rejected,
        "pending_review": review,
        "average_confidence": round(avg_confidence, 3),
        "average_risk_score": round(avg_risk, 2)
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "DecisionSynthesis MCP Server"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8003)
