export type Environment = "development" | "staging" | "production";
export type AutonomyLevel = "low" | "medium" | "high";

export type AssessmentConfig = {
  project: { name: string };
  agent: {
    name: string;
    environment: Environment;
    autonomy_level: AutonomyLevel;
    handles_customer_data: boolean;
    handles_untrusted_input: boolean;
    internet_access: boolean;
    multi_agent_workflow: boolean;
  };
  tools: {
    uses_tools: boolean;
    uses_mcp: boolean;
    can_read_database: boolean;
    can_write_database: boolean;
    can_send_email: boolean;
    can_execute_code: boolean;
    can_call_external_apis: boolean;
    high_risk_tools_require_approval: boolean;
    tools_allowlist_exists: boolean;
    mcp_servers_reviewed: boolean;
  };
  identity: {
    unique_identity: boolean;
    cryptographic_identity: boolean;
    shared_service_account: boolean;
  };
  authentication: {
    static_api_keys: boolean;
    short_lived_tokens: boolean;
    token_lifetime_minutes: number;
    credential_revocation_exists: boolean;
  };
  authorization: {
    deny_by_default: boolean;
    least_privilege_reviewed: boolean;
  };
  memory: {
    uses_memory: boolean;
    memory_isolated: boolean;
    sensitive_data_allowed: boolean;
    expiration_exists: boolean;
  };
  rag: {
    uses_rag: boolean;
    untrusted_sources: boolean;
    document_uploads: boolean;
    ingestion_validation: boolean;
  };
  logging: {
    logs_tool_calls: boolean;
    logs_data_access: boolean;
    immutable_logs: boolean;
  };
  traceability: {
    request_ids: boolean;
    trace_user_request_to_agent_action: boolean;
  };
  sandboxing: {
    sandboxing_enabled: boolean;
    sandbox_for_untrusted_input: boolean;
  };
  input_output_controls: {
    egress_controls: boolean;
    prompt_injection_filtering: boolean;
    output_filtering_customer_data: boolean;
  };
  recovery: {
    rollback_plan_exists: boolean;
    kill_switch_exists: boolean;
  };
  governance: {
    risk_assessment_done: boolean;
    incident_response_plan_exists: boolean;
    human_owner_defined: boolean;
  };
  supply_chain: {
    ai_bom_exists: boolean;
    model_source_verified: boolean;
  };
};

export type Finding = {
  id: string;
  title: string;
  category: string;
  severity: "Critical" | "High" | "Medium" | "Low";
  description: string;
  recommendation: string;
  evidence: string;
};

export type ScanResult = {
  agent_name: string;
  environment: string;
  score: number;
  readiness_level: string;
  blast_radius: "Low" | "Medium" | "High" | "Critical";
  summary: Record<string, number>;
  category_scores: Record<string, number>;
  findings: Finding[];
};
