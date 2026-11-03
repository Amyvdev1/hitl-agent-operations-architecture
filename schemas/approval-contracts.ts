export type TaskState = "PENDING_APPROVAL" | "APPROVED" | "BLOCKED" | "RECOVERED";
export type HumanApproval = Readonly<{
  tenantId: string;
  taskId: string;
  revision: number;
  argumentsSha256: string;
  status: "HUMAN_VERIFIED" | "REJECTED";
  role: "approver";
  expiresAtEpochSeconds: number;
}>;
// Shape only: server-side runtime validation, authorization and atomic consumption are required.
