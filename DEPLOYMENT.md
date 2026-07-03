# Deployment Guide

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│          USER INTERFACE LAYER (Streamlit)                    │
│  http://localhost:8501 - Web-based chatbot UI               │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP
┌────────────────────────▼────────────────────────────────────┐
│          MICROSERVICE LAYER (FastAPI)                        │
│  http://localhost:8000 - REST API & Orchestration          │
│  ├─ POST /applications/submit                               │
│  ├─ GET /applications/{id}/status                           │
│  └─ GET /docs (Swagger UI)                                  │
└────────────────────────┬────────────────────────────────────┘
                         │ Invokes
┌────────────────────────▼────────────────────────────────────┐
│      ORCHESTRATION LAYER (LangGraph + Agent SDK)             │
│  - State Management                                          │
│  - Workflow Coordination                                     │
│  - Agent Sequencing                                          │
└────────────────────────┬────────────────────────────────────┘
        ┌───────────────┼───────────────┐
        │               │               │
   ┌────▼─────┐    ┌────▼─────┐   ┌────▼─────┐
   │ Agent 1  │    │ Agent 2  │   │ Agent 3  │
   │Applicant │    │Financial │   │Decision  │
   │ Profile  │    │  Risk    │   │ & Comp   │
   └────┬─────┘    └────┬─────┘   └────┬─────┘
        │               │               │
        └───────────────┼───────────────┘
                    │ Queries
        ┌───────────┼───────────┐
        │           │           │
   ┌────▼────┐ ┌────▼────┐ ┌────▼────┐
   │MCP Srv 1│ │MCP Srv 2│ │MCP Srv 3│
   │ Appli   │ │RiskDB   │ │Decision │
   │ DB      │ │         │ │Synth    │
   │ :8001   │ │ :8002   │ │ :8003   │
   └─────────┘ └─────────┘ └─────────┘
```

## Installation Steps

### Step 1: System Requirements
- Python 3.11+
- 2GB RAM minimum
- 500MB disk space
- Network access for API calls

### Step 2: Clone/Setup Project
```bash
cd /home/ubuntu/Capetone_Project_Mani
python3.11 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export FASTAPI_HOST="127.0.0.1"
export FASTAPI_PORT="8000"
export LOG_LEVEL="INFO"
```

## Deployment Configuration

### Local Development
All services on localhost with different ports:
- Streamlit UI: 8501
- FastAPI Service: 8000
- MCP Servers: 8001, 8002, 8003

### Docker Deployment (Production)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "service:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t loan-approval-system .
docker run -p 8000:8000 -e ANTHROPIC_API_KEY="..." loan-approval-system
```

### Kubernetes Deployment

`k8s-deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: loan-approval-system
spec:
  replicas: 3
  selector:
    matchLabels:
      app: loan-approval
  template:
    metadata:
      labels:
        app: loan-approval
    spec:
      containers:
      - name: api
        image: loan-approval-system:latest
        ports:
        - containerPort: 8000
        env:
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: anthropic
---
apiVersion: v1
kind: Service
metadata:
  name: loan-approval-service
spec:
  selector:
    app: loan-approval
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
```

Deploy:
```bash
kubectl apply -f k8s-deployment.yaml
```

## Service Startup Order

**Critical**: Start services in this order:

1. **MCP Servers** (dependencies, no dependencies)
   ```bash
   # Terminal 1
   python mcp_servers/applicant_db_server.py
   
   # Terminal 2
   python mcp_servers/risk_rules_server.py
   
   # Terminal 3
   python mcp_servers/decision_synthesis_server.py
   ```

2. **FastAPI Microservice** (depends on MCP servers)
   ```bash
   # Terminal 4
   python service.py
   ```

3. **Streamlit UI** (depends on FastAPI)
   ```bash
   # Terminal 5
   streamlit run app.py
   ```

## Performance Tuning

### FastAPI Configuration
```python
# service.py - Production settings
uvicorn.run(
    app,
    host="0.0.0.0",
    port=8000,
    workers=4,  # For multi-core processing
    log_level="info",
    access_log=True
)
```

### Agent Timeouts
Edit `utils/config.py`:
```python
AGENT_TIMEOUT = 60  # seconds
MAX_RETRIES = 3
```

### Orchestration Optimization
- Parallel agent execution where possible
- Caching of applicant data
- Connection pooling to MCP servers

## Monitoring & Logging

### Log Configuration
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('loan_system.log'),
        logging.StreamHandler()
    ]
)
```

### Key Metrics to Monitor
- **API Response Time**: Target < 5 seconds
- **Agent Processing Time**: Target < 2 seconds per agent
- **Error Rate**: Target < 0.1%
- **Throughput**: Requests per minute

### Health Checks
```bash
# Check all services
for port in 8000 8001 8002 8003; do
  curl http://localhost:$port/health
done
```

## Scaling Considerations

### Horizontal Scaling
- Multiple FastAPI instances behind load balancer
- Each instance with own orchestrator
- Shared MCP server pool

### Vertical Scaling
- Increase worker threads in FastAPI
- Optimize agent algorithms
- Cache frequently accessed data

### Database Integration
For production, replace in-memory MCP servers with:
- PostgreSQL for applicant data
- Redis for caching
- Elasticsearch for audit logs

Example migration:
```python
# mcp_servers/applicant_db_server.py
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

DATABASE_URL = "postgresql://user:password@localhost/loan_db"
engine = create_engine(DATABASE_URL)

@app.post("/query")
async def query_applicant_db(query: ApplicantDBQuery):
    with Session(engine) as session:
        applicant = session.query(Applicant).filter_by(
            id=query.applicant_id
        ).first()
        # Return data
```

## Security Considerations

### API Security
```python
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer

security = HTTPBearer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["Authorization"],
)
```

### Data Protection
- Encrypt sensitive fields (SSN, DOB)
- Use HTTPS only
- Implement request signing
- Audit all decisions

### Rate Limiting
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/applications/submit")
@limiter.limit("10/minute")
async def submit_loan_application(request: Request, application: LoanApplicationInput):
    ...
```

## Backup & Recovery

### Data Backup Strategy
```bash
# Backup decision records
sqlite3 decisions.db ".dump" > decisions_backup.sql

# Backup configuration
cp -r config/ config_backup/
```

### Disaster Recovery
1. Maintain hot standby of FastAPI service
2. Replicate MCP server data
3. Regular testing of failover
4. Document recovery procedures

## CI/CD Pipeline

### GitHub Actions Example
```yaml
name: Deploy Loan System

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python test_system.py

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to production
        run: |
          docker build -t loan-system:${{ github.sha }} .
          docker push registry.example.com/loan-system:${{ github.sha }}
```

## Troubleshooting Deployment Issues

### Port Already in Use
```bash
# Find process using port
lsof -i :8000
kill -9 <PID>
```

### Memory Issues
```bash
# Increase virtual memory
sysctl -w vm.swappiness=60

# Monitor memory
watch -n 1 free -h
```

### API Timeout
- Check MCP server connectivity
- Increase AGENT_TIMEOUT in config.py
- Profile agent performance

### High Error Rate
- Check Anthropic API quota
- Verify API key validity
- Review logs for specific errors

## Maintenance Schedule

| Task | Frequency | Owner |
|------|-----------|-------|
| System monitoring | Daily | DevOps |
| Log rotation | Weekly | DevOps |
| Database backup | Daily | Database Admin |
| Security updates | As needed | Security |
| Performance review | Monthly | Engineering |
| Disaster recovery test | Quarterly | DevOps |

## Post-Deployment Validation

1. ✅ All services start without errors
2. ✅ Health checks pass for all endpoints
3. ✅ Sample applications process correctly
4. ✅ API response times < 5 seconds
5. ✅ Decisions are consistent and explainable
6. ✅ Audit logs are being recorded
7. ✅ Error handling works properly
8. ✅ UI displays decisions clearly

## Support & Escalation

| Issue Level | Response Time | Escalation |
|-------------|---------------|-----------|
| Critical | 15 minutes | On-call engineer |
| High | 1 hour | Team lead |
| Medium | 4 hours | Engineer |
| Low | 24 hours | Backlog |
