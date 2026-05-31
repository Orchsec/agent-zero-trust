"""Pydantic schema for agent assessment configs."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, StrictBool, field_validator


class Environment(StrEnum):
    development = "development"
    staging = "staging"
    production = "production"


class AutonomyLevel(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ProjectConfig(StrictModel):
    name: str = "unnamed-project"
    owner: str | None = None


class AgentDetails(StrictModel):
    name: str
    environment: Environment = Environment.development
    autonomy_level: AutonomyLevel = AutonomyLevel.low
    handles_customer_data: StrictBool = False
    handles_untrusted_input: StrictBool = False
    internet_access: StrictBool = False
    multi_agent_workflow: StrictBool = False


class ToolConfig(StrictModel):
    uses_tools: StrictBool = False
    uses_mcp: StrictBool = False
    can_read_database: StrictBool = False
    can_write_database: StrictBool = False
    can_send_email: StrictBool = False
    can_execute_code: StrictBool = False
    can_call_external_apis: StrictBool = False
    high_risk_tools_require_approval: StrictBool = True
    tools_allowlist_exists: StrictBool = True
    mcp_servers_reviewed: StrictBool = True


class IdentityConfig(StrictModel):
    unique_identity: StrictBool = True
    cryptographic_identity: StrictBool = False
    shared_service_account: StrictBool = False


class AuthenticationConfig(StrictModel):
    static_api_keys: StrictBool = False
    short_lived_tokens: StrictBool = True
    token_lifetime_minutes: int = Field(default=60, ge=1)
    credential_revocation_exists: StrictBool = True


class AuthorizationConfig(StrictModel):
    deny_by_default: StrictBool = True
    least_privilege_reviewed: StrictBool = True


class LoggingConfig(StrictModel):
    logs_tool_calls: StrictBool = True
    logs_data_access: StrictBool = True
    immutable_logs: StrictBool = False


class TraceabilityConfig(StrictModel):
    request_ids: StrictBool = True
    trace_user_request_to_agent_action: StrictBool = True


class MemoryConfig(StrictModel):
    uses_memory: StrictBool = False
    memory_isolated: StrictBool = True
    sensitive_data_allowed: StrictBool = False
    expiration_exists: StrictBool = True


class RagConfig(StrictModel):
    uses_rag: StrictBool = False
    untrusted_sources: StrictBool = False
    document_uploads: StrictBool = False
    ingestion_validation: StrictBool = True


class SandboxingConfig(StrictModel):
    sandboxing_enabled: StrictBool = True
    sandbox_for_untrusted_input: StrictBool = True


class InputOutputControlsConfig(StrictModel):
    egress_controls: StrictBool = True
    prompt_injection_filtering: StrictBool = True
    output_filtering_customer_data: StrictBool = True


class RecoveryConfig(StrictModel):
    rollback_plan_exists: StrictBool = True
    kill_switch_exists: StrictBool = True


class GovernanceConfig(StrictModel):
    risk_assessment_done: StrictBool = True
    incident_response_plan_exists: StrictBool = True
    human_owner_defined: StrictBool = True


class SupplyChainConfig(StrictModel):
    ai_bom_exists: StrictBool = True
    model_source_verified: StrictBool = True


class AgentConfig(StrictModel):
    project: ProjectConfig = Field(default_factory=ProjectConfig)
    agent: AgentDetails
    tools: ToolConfig = Field(default_factory=ToolConfig)
    identity: IdentityConfig = Field(default_factory=IdentityConfig)
    authentication: AuthenticationConfig = Field(default_factory=AuthenticationConfig)
    authorization: AuthorizationConfig = Field(default_factory=AuthorizationConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    traceability: TraceabilityConfig = Field(default_factory=TraceabilityConfig)
    memory: MemoryConfig = Field(default_factory=MemoryConfig)
    rag: RagConfig = Field(default_factory=RagConfig)
    sandboxing: SandboxingConfig = Field(default_factory=SandboxingConfig)
    input_output_controls: InputOutputControlsConfig = Field(
        default_factory=InputOutputControlsConfig
    )
    recovery: RecoveryConfig = Field(default_factory=RecoveryConfig)
    governance: GovernanceConfig = Field(default_factory=GovernanceConfig)
    supply_chain: SupplyChainConfig = Field(default_factory=SupplyChainConfig)

    @field_validator("agent")
    @classmethod
    def agent_name_is_not_blank(cls, value: AgentDetails) -> AgentDetails:
        if not value.name.strip():
            raise ValueError("agent.name must not be blank")
        return value
