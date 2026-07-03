"""
MCP Server simulating ApplicantDB - provides applicant profile data
Run: python mcp_servers/applicant_db_server.py
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="ApplicantDB MCP Server")


class ApplicantDBQuery(BaseModel):
    applicant_id: str
    query_type: str  # "credit_history", "income_verification", "employment_history"


class ApplicantDBResponse(BaseModel):
    applicant_id: str
    query_type: str
    data: dict
    source: str = "ApplicantDB"


@app.post("/query")
async def query_applicant_db(query: ApplicantDBQuery) -> ApplicantDBResponse:
    """Query applicant database for historical data"""

    if query.query_type == "credit_history":
        data = {
            "credit_history_length_years": 15,
            "payment_history": "95% on-time payments",
            "delinquencies_past_24_months": 0,
            "collections": False,
            "bankruptcy_history": False,
            "credit_inquiries_6_months": 2
        }

    elif query.query_type == "income_verification":
        data = {
            "verified_income": True,
            "income_source": "W2 Employment",
            "income_consistency": "stable",
            "yoy_income_growth": 3.5,
            "employment_length_years": 7
        }

    elif query.query_type == "employment_history":
        data = {
            "current_employer": "Tech Corp",
            "employment_duration_months": 84,
            "employment_type": "Full-time",
            "position": "Senior Developer",
            "previous_employers": 2,
            "employment_gaps": False
        }

    else:
        raise HTTPException(status_code=400, detail=f"Unknown query type: {query.query_type}")

    return ApplicantDBResponse(
        applicant_id=query.applicant_id,
        query_type=query.query_type,
        data=data
    )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ApplicantDB MCP Server"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
