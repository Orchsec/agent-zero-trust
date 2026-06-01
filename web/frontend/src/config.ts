import type { AssessmentConfig } from "./types";

export const defaultConfig: AssessmentConfig = {
  project: { name: "agent-assessment" },
  agent: {
    name: "sales-email-agent",
    environment: "production",
    autonomy_level: "high",
    handles_customer_data: true,
    handles_untrusted_input: true,
    internet_access: true,
    multi_agent_workflow: false
  },
  tools: {
    uses_tools: true,
    uses_mcp: false,
    can_read_database: true,
    can_write_database: false,
    can_send_email: true,
    can_execute_code: false,
    can_call_external_apis: true,
    high_risk_tools_require_approval: false,
    tools_allowlist_exists: false,
    mcp_servers_reviewed: true
  },
  identity: {
    unique_identity: false,
    cryptographic_identity: false,
    shared_service_account: true
  },
  authentication: {
    static_api_keys: true,
    short_lived_tokens: false,
    token_lifetime_minutes: 1440,
    credential_revocation_exists: false
  },
  authorization: {
    deny_by_default: true,
    least_privilege_reviewed: true
  },
  memory: {
    uses_memory: false,
    memory_isolated: true,
    sensitive_data_allowed: false,
    expiration_exists: true
  },
  rag: {
    uses_rag: false,
    untrusted_sources: false,
    document_uploads: false,
    ingestion_validation: true
  },
  logging: {
    logs_tool_calls: true,
    logs_data_access: true,
    immutable_logs: false
  },
  traceability: {
    request_ids: false,
    trace_user_request_to_agent_action: false
  },
  sandboxing: {
    sandboxing_enabled: true,
    sandbox_for_untrusted_input: true
  },
  input_output_controls: {
    egress_controls: false,
    prompt_injection_filtering: true,
    output_filtering_customer_data: false
  },
  recovery: {
    rollback_plan_exists: false,
    kill_switch_exists: false
  },
  governance: {
    risk_assessment_done: false,
    incident_response_plan_exists: false,
    human_owner_defined: false
  },
  supply_chain: {
    ai_bom_exists: true,
    model_source_verified: true
  }
};
