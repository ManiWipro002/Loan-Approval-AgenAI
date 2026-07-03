import os
from typing import Optional

# API Configuration
ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = "claude-sonnet-4-6"

# Service Configuration
FASTAPI_HOST = os.getenv("FASTAPI_HOST", "127.0.0.1")
FASTAPI_PORT = int(os.getenv("FASTAPI_PORT", "8000"))

# MCP Servers Configuration
MCP_APPLICANT_DB_URL = os.getenv("MCP_APPLICANT_DB_URL", "http://127.0.0.1:8001")
MCP_RISK_RULES_URL = os.getenv("MCP_RISK_RULES_URL", "http://127.0.0.1:8002")
MCP_DECISION_SYNTHESIS_URL = os.getenv("MCP_DECISION_SYNTHESIS_URL", "http://127.0.0.1:8003")

# Agent Configuration
AGENT_TIMEOUT = 30  # seconds
MAX_RETRIES = 3

# Risk Thresholds
RISK_SCORE_APPROVE_THRESHOLD = 40
RISK_SCORE_REVIEW_THRESHOLD = 70

# Credit Score Thresholds
CREDIT_SCORE_MINIMUM = 580
CREDIT_SCORE_WARNING = 620

# DTI Thresholds
DTI_MAXIMUM = 50
DTI_PREFERRED = 43

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
