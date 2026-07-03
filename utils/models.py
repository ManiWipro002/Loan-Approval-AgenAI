from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, List, Literal
from datetime import datetime
from enum import Enum


class EmploymentType(str, Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"
    SELF_EMPLOYED = "self-employed"
    UNEMPLOYED = "unemployed"


class LocationType(str, Enum):
    URBAN = "urban"
    SEMI_URBAN = "semi-urban"
    RURAL = "rural"


class LoanApplicationInput(BaseModel):
    """Input loan application data"""
    applicant_id: str
    age: int = Field(ge=18, le=100)
    income: float = Field(ge=0)
    employment_type: EmploymentType
    credit_score: int = Field(ge=300, le=850)
    loan_amount: float = Field(ge=1000)
    loan_tenure_months: int = Field(ge=6, le=600)
    existing_liabilities: float = Field(ge=0)
    location: LocationType
    application_timestamp: datetime

    @validator('age')
    def validate_age(cls, v):
        if v < 18:
            raise ValueError("Applicant must be 18 or older")
        return v


class ApplicantProfileOutput(BaseModel):
    """Output from Applicant Profile Agent"""
    income_stability_score: float = Field(ge=0, le=100)
    employment_risk: Literal["low", "medium", "high"]
    credit_history_summary: str
    application_completeness: float = Field(ge=0, le=100)
    flags: List[str] = Field(default_factory=list)


class FinancialRiskOutput(BaseModel):
    """Output from Financial Risk Agent"""
    debt_to_income_ratio: float
    credit_score_risk_level: Literal["low", "medium", "high"]
    loan_amount_risk: Literal["low", "medium", "high"]
    anomaly_detected: bool
    anomaly_description: Optional[str] = None
    reasoning: str


class LoanDecisionOutput(BaseModel):
    """Output from Loan Decision Agent"""
    classification: Literal["Approved", "Rejected", "Review"]
    risk_score: float = Field(ge=0, le=100)
    confidence_level: float = Field(ge=0, le=1)
    key_decision_factors: List[str]
    explanation: str


class ComplianceActionOutput(BaseModel):
    """Output from Compliance & Action Orchestrator"""
    action_taken: Literal["approved", "rejected", "pending_review"]
    notification_sent: bool
    case_id: str
    timestamp: datetime
    summary: str


class LoanApplicationResponse(BaseModel):
    """Complete response for a loan application"""
    applicant_id: str
    application_status: Literal["success", "error"]
    decision: LoanDecisionOutput
    applicant_profile: Optional[ApplicantProfileOutput] = None
    financial_risk: Optional[FinancialRiskOutput] = None
    compliance_action: Optional[ComplianceActionOutput] = None
    error_message: Optional[str] = None
    processing_timestamp: datetime = Field(default_factory=datetime.utcnow)
