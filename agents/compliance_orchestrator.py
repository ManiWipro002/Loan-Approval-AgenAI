from datetime import datetime
from utils.models import LoanDecisionOutput, ComplianceActionOutput
import uuid


class ComplianceOrchestrator:
    """Agent responsible for executing compliance actions, sending notifications,
    and creating audit records for loan decisions."""

    def __init__(self):
        self.name = "Compliance & Action Orchestrator"

    def execute_action(
        self,
        applicant_id: str,
        decision: LoanDecisionOutput
    ) -> ComplianceActionOutput:
        """Execute compliance actions based on decision"""

        action_taken = self._map_decision_to_action(decision.classification)
        case_id = self._generate_case_id(applicant_id)
        notification_sent = self._send_notification(applicant_id, action_taken, case_id)
        summary = self._generate_summary(applicant_id, action_taken, decision)

        return ComplianceActionOutput(
            action_taken=action_taken,
            notification_sent=notification_sent,
            case_id=case_id,
            timestamp=datetime.utcnow(),
            summary=summary
        )

    def _map_decision_to_action(self, classification: str) -> str:
        """Map decision classification to compliance action"""

        action_map = {
            "Approved": "approved",
            "Rejected": "rejected",
            "Review": "pending_review"
        }
        return action_map.get(classification, "pending_review")

    def _generate_case_id(self, applicant_id: str) -> str:
        """Generate unique case ID for audit trail"""

        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        unique_suffix = str(uuid.uuid4())[:8]
        return f"CASE-{applicant_id}-{timestamp}-{unique_suffix}"

    def _send_notification(
        self,
        applicant_id: str,
        action: str,
        case_id: str
    ) -> bool:
        """Send notification to applicant and internal systems"""

        try:
            # In production, this would integrate with notification services
            # (email, SMS, internal audit systems, etc.)

            notification_content = self._build_notification(applicant_id, action, case_id)

            # Simulate sending notification
            self._log_notification(applicant_id, action, case_id, notification_content)

            return True

        except Exception as e:
            print(f"Error sending notification: {e}")
            return False

    def _build_notification(self, applicant_id: str, action: str, case_id: str) -> str:
        """Build notification content"""

        action_messages = {
            "approved": "Your loan application has been APPROVED!",
            "rejected": "Your loan application has been REJECTED.",
            "pending_review": "Your loan application is under REVIEW."
        }

        message = f"Dear Applicant {applicant_id},\n\n"
        message += f"{action_messages.get(action, 'Your application is being processed.')}\n"
        message += f"Case ID: {case_id}\n"
        message += f"Timestamp: {datetime.utcnow().isoformat()}\n\n"
        message += "You will receive further updates via your registered communication channels.\n"

        return message

    def _log_notification(self, applicant_id: str, action: str, case_id: str, content: str):
        """Log notification for audit trail"""

        # In production, this would write to secure audit logs
        log_entry = {
            "applicant_id": applicant_id,
            "action": action,
            "case_id": case_id,
            "timestamp": datetime.utcnow().isoformat(),
            "notification_content": content
        }

        # Simulate logging
        print(f"[AUDIT LOG] {log_entry}")

    def _generate_summary(self, applicant_id: str, action: str, decision: LoanDecisionOutput) -> str:
        """Generate summary of compliance action"""

        summary = f"Loan Application Summary:\n"
        summary += f"  Applicant ID: {applicant_id}\n"
        summary += f"  Decision: {decision.classification}\n"
        summary += f"  Risk Score: {decision.risk_score}/100\n"
        summary += f"  Confidence: {decision.confidence_level:.0%}\n"
        summary += f"  Action Taken: {action.upper()}\n"

        if action == "pending_review":
            summary += f"  Status: Pending manual review by lending officer\n"
        elif action == "approved":
            summary += f"  Status: Pre-approved - documentation required for final disbursement\n"
        else:  # rejected
            summary += f"  Status: Application rejected - applicant may appeal\n"

        return summary
