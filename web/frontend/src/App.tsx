import {
  AlertTriangle,
  ArrowLeft,
  ArrowRight,
  Clipboard,
  Download,
  FileCode2,
  FileJson,
  Play,
  ShieldCheck
} from "lucide-react";
import yaml from "js-yaml";
import { useMemo, useState } from "react";

import { defaultConfig } from "./config";
import type { AssessmentConfig, AutonomyLevel, Environment, ScanResult } from "./types";

type FieldPath = string;

type ToggleField = {
  label: string;
  path: FieldPath;
};

type Step = {
  title: string;
  fields: ToggleField[];
};

const steps: Step[] = [
  {
    title: "Agent Basics",
    fields: [
      { label: "Handles customer data", path: "agent.handles_customer_data" },
      { label: "Handles untrusted input", path: "agent.handles_untrusted_input" },
      { label: "Internet access", path: "agent.internet_access" },
      { label: "Multi-agent workflow", path: "agent.multi_agent_workflow" }
    ]
  },
  {
    title: "Tool Access",
    fields: [
      { label: "Uses tools", path: "tools.uses_tools" },
      { label: "Uses MCP", path: "tools.uses_mcp" },
      { label: "Can read database", path: "tools.can_read_database" },
      { label: "Can write database", path: "tools.can_write_database" },
      { label: "Can send email", path: "tools.can_send_email" },
      { label: "Can execute code", path: "tools.can_execute_code" },
      { label: "Can call external APIs", path: "tools.can_call_external_apis" },
      { label: "High-risk tools require approval", path: "tools.high_risk_tools_require_approval" },
      { label: "Tool allowlist exists", path: "tools.tools_allowlist_exists" },
      { label: "MCP servers reviewed", path: "tools.mcp_servers_reviewed" }
    ]
  },
  {
    title: "Identity And Credentials",
    fields: [
      { label: "Unique agent identity", path: "identity.unique_identity" },
      { label: "Cryptographic identity", path: "identity.cryptographic_identity" },
      { label: "Shared service account", path: "identity.shared_service_account" },
      { label: "Static API keys", path: "authentication.static_api_keys" },
      { label: "Short-lived tokens", path: "authentication.short_lived_tokens" },
      { label: "Credential revocation exists", path: "authentication.credential_revocation_exists" }
    ]
  },
  {
    title: "Memory And RAG",
    fields: [
      { label: "Uses memory", path: "memory.uses_memory" },
      { label: "Memory isolated", path: "memory.memory_isolated" },
      { label: "Sensitive data allowed in memory", path: "memory.sensitive_data_allowed" },
      { label: "Memory expiration exists", path: "memory.expiration_exists" },
      { label: "Uses RAG", path: "rag.uses_rag" },
      { label: "RAG uses untrusted sources", path: "rag.untrusted_sources" },
      { label: "Document uploads", path: "rag.document_uploads" },
      { label: "Ingestion validation", path: "rag.ingestion_validation" }
    ]
  },
  {
    title: "Logging And Traceability",
    fields: [
      { label: "Logs tool calls", path: "logging.logs_tool_calls" },
      { label: "Logs data access", path: "logging.logs_data_access" },
      { label: "Immutable logs", path: "logging.immutable_logs" },
      { label: "Request IDs", path: "traceability.request_ids" },
      {
        label: "Trace user request to agent action",
        path: "traceability.trace_user_request_to_agent_action"
      }
    ]
  },
  {
    title: "Controls And Recovery",
    fields: [
      { label: "Sandboxing enabled", path: "sandboxing.sandboxing_enabled" },
      { label: "Sandbox for untrusted input", path: "sandboxing.sandbox_for_untrusted_input" },
      { label: "Egress controls", path: "input_output_controls.egress_controls" },
      { label: "Prompt injection filtering", path: "input_output_controls.prompt_injection_filtering" },
      {
        label: "Output filtering for customer data",
        path: "input_output_controls.output_filtering_customer_data"
      },
      { label: "Rollback plan", path: "recovery.rollback_plan_exists" },
      { label: "Kill switch", path: "recovery.kill_switch_exists" },
      { label: "Risk assessment done", path: "governance.risk_assessment_done" },
      { label: "Incident response plan", path: "governance.incident_response_plan_exists" },
      { label: "Human owner", path: "governance.human_owner_defined" },
      { label: "AI-BOM exists", path: "supply_chain.ai_bom_exists" },
      { label: "Model source verified", path: "supply_chain.model_source_verified" }
    ]
  }
];

const apiBase = import.meta.env.VITE_API_BASE ?? "";
const categoryWeights: Record<string, number> = {
  identity_authentication: 15,
  tools_mcp: 15,
  authorization: 15,
  logging_traceability: 15,
  memory_rag: 10,
  sandboxing: 10,
  input_output_controls: 8,
  recovery: 5,
  governance: 5,
  supply_chain: 2
};

function readPath(config: AssessmentConfig, path: FieldPath): boolean {
  return path.split(".").reduce<unknown>((value, segment) => {
    if (typeof value !== "object" || value === null) return undefined;
    return (value as Record<string, unknown>)[segment];
  }, config) as boolean;
}

function writePath(config: AssessmentConfig, path: FieldPath, value: boolean): AssessmentConfig {
  const copy = structuredClone(config);
  const segments = path.split(".");
  let target = copy as unknown as Record<string, unknown>;
  for (const segment of segments.slice(0, -1)) {
    target = target[segment] as Record<string, unknown>;
  }
  target[segments[segments.length - 1]] = value;
  return copy;
}

function downloadFile(filename: string, content: string, type: string) {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}

function severityClass(severity: string) {
  return `severity severity-${severity.toLowerCase()}`;
}

export default function App() {
  const [config, setConfig] = useState<AssessmentConfig>(defaultConfig);
  const [stepIndex, setStepIndex] = useState(0);
  const [result, setResult] = useState<ScanResult | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const currentStep = steps[stepIndex];
  const isLastStep = stepIndex === steps.length - 1;
  const yamlPreview = useMemo(() => yaml.dump(config, { noRefs: true }), [config]);

  async function runScan() {
    setBusy(true);
    setError(null);
    try {
      const response = await fetch(`${apiBase}/scan`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(config)
      });
      if (!response.ok) {
        throw new Error(await response.text());
      }
      setResult((await response.json()) as ScanResult);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Scan failed");
    } finally {
      setBusy(false);
    }
  }

  async function exportMarkdown() {
    const response = await fetch(`${apiBase}/reports/markdown`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(config)
    });
    const payload = (await response.json()) as { content: string };
    downloadFile("agent-zero-trust-report.md", payload.content, "text/markdown");
  }

  function updateAgentField<K extends keyof AssessmentConfig["agent"]>(
    key: K,
    value: AssessmentConfig["agent"][K]
  ) {
    setConfig({ ...config, agent: { ...config.agent, [key]: value } });
  }

  return (
    <main className="app-shell">
      <aside className="sidebar" aria-label="Assessment sections">
        <div className="brand">
          <ShieldCheck size={28} />
          <div>
            <h1>Agent Zero Trust</h1>
            <p>v2 assessment</p>
          </div>
        </div>
        <nav className="step-list">
          {steps.map((step, index) => (
            <button
              className={index === stepIndex ? "step active" : "step"}
              key={step.title}
              onClick={() => setStepIndex(index)}
              type="button"
            >
              <span>{index + 1}</span>
              {step.title}
            </button>
          ))}
        </nav>
      </aside>

      <section className="workspace">
        <header className="topbar">
          <div>
            <label htmlFor="agent-name">Agent name</label>
            <input
              id="agent-name"
              value={config.agent.name}
              onChange={(event) => updateAgentField("name", event.target.value)}
            />
          </div>
          <div>
            <label htmlFor="environment">Environment</label>
            <select
              id="environment"
              value={config.agent.environment}
              onChange={(event) =>
                updateAgentField("environment", event.target.value as Environment)
              }
            >
              <option value="development">Development</option>
              <option value="staging">Staging</option>
              <option value="production">Production</option>
            </select>
          </div>
          <div>
            <label htmlFor="autonomy">Autonomy</label>
            <select
              id="autonomy"
              value={config.agent.autonomy_level}
              onChange={(event) =>
                updateAgentField("autonomy_level", event.target.value as AutonomyLevel)
              }
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>
          <button className="primary" disabled={busy} onClick={runScan} type="button">
            <Play size={18} />
            {busy ? "Scanning" : "Run scan"}
          </button>
        </header>

        {error ? (
          <div className="error" role="alert">
            <AlertTriangle size={18} />
            {error}
          </div>
        ) : null}

        <div className="content-grid">
          <section className="questionnaire">
            <div className="section-heading">
              <p>Step {stepIndex + 1} of {steps.length}</p>
              <h2>{currentStep.title}</h2>
            </div>

            <div className="toggle-grid">
              {currentStep.fields.map((field) => (
                <label className="toggle-row" key={field.path}>
                  <span>{field.label}</span>
                  <input
                    checked={readPath(config, field.path)}
                    onChange={(event) =>
                      setConfig(writePath(config, field.path, event.target.checked))
                    }
                    type="checkbox"
                  />
                </label>
              ))}
            </div>

            {stepIndex === 2 ? (
              <div className="number-control">
                <label htmlFor="token-lifetime">Token lifetime minutes</label>
                <input
                  id="token-lifetime"
                  min={1}
                  type="number"
                  value={config.authentication.token_lifetime_minutes}
                  onChange={(event) =>
                    setConfig({
                      ...config,
                      authentication: {
                        ...config.authentication,
                        token_lifetime_minutes: Number(event.target.value)
                      }
                    })
                  }
                />
              </div>
            ) : null}

            <div className="pager">
              <button
                className="secondary"
                disabled={stepIndex === 0}
                onClick={() => setStepIndex(stepIndex - 1)}
                type="button"
              >
                <ArrowLeft size={18} />
                Back
              </button>
              <button
                className="secondary"
                onClick={() => (isLastStep ? runScan() : setStepIndex(stepIndex + 1))}
                type="button"
              >
                {isLastStep ? "Scan" : "Next"}
                <ArrowRight size={18} />
              </button>
            </div>
          </section>

          <section className="results">
            {result ? (
              <>
                <div className="score-row">
                  <div className="score">{result.score}</div>
                  <div>
                    <h2>{result.readiness_level}</h2>
                    <p>Blast radius: {result.blast_radius}</p>
                  </div>
                </div>
                <div className="summary-grid">
                  {["Critical", "High", "Medium", "Low"].map((severity) => (
                    <div key={severity}>
                      <span className={severityClass(severity)}>{severity}</span>
                      <strong>{result.summary[severity] ?? 0}</strong>
                    </div>
                  ))}
                </div>
                <div className="breakdown">
                  {Object.entries(result.category_scores).map(([category, score]) => (
                    <div className="bar-row" key={category}>
                      <span>{category.replaceAll("_", " ")}</span>
                      <div>
                        <i
                          style={{
                            width: `${Math.round((score / categoryWeights[category]) * 100)}%`
                          }}
                        />
                      </div>
                      <b>{score}</b>
                    </div>
                  ))}
                </div>
                <div className="findings">
                  {result.findings.slice(0, 8).map((finding) => (
                    <article key={finding.id}>
                      <div>
                        <span className={severityClass(finding.severity)}>
                          {finding.severity}
                        </span>
                        <code>{finding.id}</code>
                      </div>
                      <h3>{finding.title}</h3>
                      <p>{finding.recommendation}</p>
                    </article>
                  ))}
                </div>
                <div className="export-row">
                  <button
                    className="secondary"
                    onClick={() =>
                      downloadFile(
                        "agent-zero-trust-report.json",
                        JSON.stringify(result, null, 2),
                        "application/json"
                      )
                    }
                    type="button"
                  >
                    <FileJson size={18} />
                    JSON
                  </button>
                  <button className="secondary" onClick={exportMarkdown} type="button">
                    <Download size={18} />
                    Markdown
                  </button>
                </div>
              </>
            ) : (
              <div className="empty-state">
                <ShieldCheck size={44} />
                <h2>Ready to assess</h2>
              </div>
            )}
          </section>
        </div>

        <section className="yaml-panel">
          <div>
            <FileCode2 size={20} />
            <h2>Generated YAML</h2>
          </div>
          <button
            className="secondary"
            onClick={() => navigator.clipboard.writeText(yamlPreview)}
            type="button"
          >
            <Clipboard size={18} />
            Copy YAML
          </button>
          <pre>{yamlPreview}</pre>
        </section>
      </section>
    </main>
  );
}
