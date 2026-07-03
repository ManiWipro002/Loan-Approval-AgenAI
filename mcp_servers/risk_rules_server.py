"""
MCP Server simulating RiskRulesDB - provides risk assessment rules and regulatory data
Run: python mcp_servers/risk_rules_server.py
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="RiskRulesDB MCP Server")


class RiskRulesQuery(BaseModel):
    rule_type: str  # "dti_limits", "credit_score_minimums", "regulatory_limits"
    location: str = None
    loan_type: str = "personal"


class RiskRulesResponse(BaseModel):
    rule_type: str
    rules: dict
    effective_date: str = "2024-01-01"


@app.post("/query")
async def query_risk_rules(query: RiskRulesQuery) -> RiskRulesResponse:
    """Query risk assessment rules"""

    if query.rule_type == "dti_limits":
        rules = {
            "maximum_dti": 50,
            "preferred_dti": 43,
            "minimum_dti": 0,
            "calculation_method": "total_debt_payments / gross_monthly_income",
            "includes_new_loan": True
        }

    elif query.rule_type == "credit_score_minimums":
        rules = {
            "minimum_score": 580,
            "preferred_score": 620,
            "excellent_score": 740,
            "good_score": 670,
            "fair_score": 620,
            "poor_score": 580
        }

    elif query.rule_type == "regulatory_limits":
        rules = {
            "maximum_loan_amount": 1000000,
            "maximum_tenure_months": 600,
            "minimum_tenure_months": 6,
            "location_restrictions": {},
            "age_restrictions": {"minimum": 18, "maximum": 120},
            "employment_restrictions": ["self-employed", "part-time"]
        }

    else:
        raise HTTPException(status_code=400, detail=f"Unknown rule type: {query.rule_type}")

    return RiskRulesResponse(
        rule_type=query.rule_type,
        rules=rules
    )


@app.get("/regulatory_updates")
async def get_regulatory_updates():
    """Get latest regulatory updates"""
    return {
        "last_updated": "2024-12-15",
        "regulations": [
            "Dodd-Frank Act compliance",
            "FAIR Lending compliance",
            "Equal Credit Opportunity Act",
            "Truth in Lending Act"
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "RiskRulesDB MCP Server"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)
