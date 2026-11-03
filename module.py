"""Offline reference validator; no authentication or side effects."""
from dataclasses import dataclass
import hashlib
import json

def digest(arguments):
    encoded = json.dumps(arguments, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    return hashlib.sha256(encoded).hexdigest()

@dataclass(frozen=True)
class Approval:
    tenant: str
    task: str
    revision: int
    arguments_hash: str
    expires_at: int
    status: str = "HUMAN_VERIFIED"
    role: str = "approver"

def authorize(approval, *, tenant, task, revision, arguments, now, state):
    if not tenant or not task or state != "PENDING_APPROVAL":
        raise ValueError("invalid task state")
    if approval.tenant != tenant or approval.task != task or approval.revision != revision:
        raise ValueError("approval scope mismatch")
    if approval.status != "HUMAN_VERIFIED" or approval.role != "approver":
        raise ValueError("human approval required")
    if now >= approval.expires_at:
        raise ValueError("approval expired")
    if approval.arguments_hash != digest(arguments):
        raise ValueError("arguments changed")
    return "APPROVED"
