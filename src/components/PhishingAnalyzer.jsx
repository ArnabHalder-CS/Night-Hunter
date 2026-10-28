import { useState } from "react";
import {
  AlertTriangle,
  CheckCircle2,
  Terminal,
  Shield,
  CircleGauge,
  Link as LinkIcon,
  RefreshCw,
  Search,
  ShieldAlert,
  ShieldCheck,
  Mail,
  BookOpen,
  ExternalLink,
  ChevronRight,
  Copy,
  Check,
  Globe,
  Radio,
  FileWarning
} from "lucide-react";

function Metric({ label, value, tone }) {
  return (
    <article className={`phishing-metric ${tone}`}>
      <span>{label}</span>
      <strong>{value}</strong>
    </article>
  );
}

export default function PhishingAnalyzer() {
  const [activeTab, setActiveTab] = useState("url"); // "url" | "homoglyph" | "triage" | "playbook"
  
  // Tab 1: URL Inspector State
  const [target, setTarget] = useState("");
  const [report, setReport] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
// Tab 3: Email Triage State
  const [emailText, setEmailText] = useState("");
  const [triageReport, setTriageReport] = useState(null);
  const [triageLoading, setTriageLoading] = useState(false);
  const [triageError, setTriageError] = useState("");

  const [copied, setCopied] = useState(false);

  async function analyzeUrl(event) {
    if (event) event.preventDefault();
    if (!target.trim()) {
      setError("Please enter a target URL to analyze.");
      return;
    }
    setLoading(true);
    setError("");
    setReport(null);
    try {
      const response = await fetch("/api/phishing", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ target: target.trim() })
      });
      const data = await response.json();
      if (!response.ok || !data.success) {
        throw new Error(data.error || "Analysis failed.");
      }
      setReport(data.report);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  }

  async function runEmailTriage(event) {
    if (event) event.preventDefault();
    if (!emailText.trim()) {
      setTriageError("Paste an email body or message text to triage.");
      return;
    }
    setTriageLoading(true);
    setTriageError("");
    setTriageReport(null);
    try {
      const response = await fetch("/api/phishing", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mode: "email_triage", text: emailText })
      });
      const data = await response.json();
      if (!response.ok || !data.success) {
        throw new Error(data.error || "Email triage failed.");
      }
      setTriageReport(data.report);
    } catch (err) {
      setTriageError(err.message);
    } finally {
      setTriageLoading(false);
    }
  }

  const metrics = report?.metrics || {};
  const findings = report?.findings || [];

  return (
    <section className="phishing-page">
      {/* Header */}
      <header className="module-header phishing-header">
        <div className="module-heading">
          <div className="module-heading-icon">
            <ShieldAlert size={26} />
          </div>
          <div>
            <p className="eyebrow">FLAGSHIP DEFENSIVE SUITE</p>
            <h2>Phishing Threat Intelligence & Spoofing Station</h2>
            <p className="subtitle">
              Heuristic Risk Scoring | Unicode Homoglyph Detection | Link Triage | Response Playbooks
            </p>
          </div>
        </div>
        <div className={`module-state ${loading || triageLoading ? "busy" : "success"}`}>
          <span />
          {loading || triageLoading ? "ANALYZING" : "DEFENSE READY"}
        </div>
      </header>

      {/* Mode Navigation Tabs */}
      <nav className="phishing-subnav" style={{ display: "flex", gap: "10px", marginBottom: "22px" }}>
        {[
          { id: "url", label: "URL Risk Inspector", icon: LinkIcon },
          { id: "triage", label: "Scam Message Analyzer", icon: Mail },
          { id: "playbook", label: "Mitigation Playbook", icon: BookOpen }
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              type="button"
              onClick={() => setActiveTab(tab.id)}
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "8px",
                padding: "10px 18px",
                borderRadius: "10px",
                border: isActive ? "1px solid rgba(255, 130, 222, 0.5)" : "1px solid rgba(120, 135, 190, 0.2)",
                background: isActive ? "linear-gradient(135deg, rgba(255, 60, 180, 0.2), rgba(120, 60, 255, 0.15))" : "rgba(10, 14, 32, 0.6)",
                color: isActive ? "#ff9ee5" : "#8e9ab8",
                fontWeight: isActive ? "700" : "500",
                fontSize: "13px",
                cursor: "pointer",
                transition: "all 0.2s ease"
              }}
            >
              <Icon size={16} />
              {tab.label}
            </button>
          );
        })}
      </nav>

      {/* TAB 1: URL Risk Inspector */}
      {activeTab === "url" && (
        <>
          <div className="phishing-workspace">
            <form className="phishing-scan-card" onSubmit={analyzeUrl}>
              <div className="phishing-card-heading">
                <div>
                  <span>SUSPICIOUS LINK INSPECTION</span>
                  <h3>Analyze URL Risk & Heuristics</h3>
                </div>
                <LinkIcon size={19} />
              </div>
              <label className="phishing-input">
                <LinkIcon size={18} />
                <input
                  value={target}
                  onChange={(event) => setTarget(event.target.value)}
                  placeholder="https://secure-login-update-verify.top/account"
                  disabled={loading}
                />
              </label>
              <button className="phishing-run-button" type="submit" disabled={loading}>
                {loading ? <RefreshCw className="spin-icon" size={17} /> : <Search size={17} />}
                {loading ? "INSPECTING TARGET..." : "INSPECT URL HEURISTICS"}
              </button>
              {error && (
                <p className="phishing-error">
                  <AlertTriangle size={16} />
                  {error}
                </p>
              )}
              <p className="phishing-note">
                100% Passive Evaluation: Night Hunter safely inspects lexical patterns, punycode, entropy, and brand indicators without exposing your machine to hostile payload execution.
              </p>
            </form>

            <aside className="phishing-check-card">
              <CircleGauge size={24} />
              <span>PASSIVE SIGNALS CHECKED</span>
              <h3>Active Heuristic Tests</h3>
              <ul>
                <li><i /> Homoglyphic Unicode characters</li>
                <li><i /> Targeted brand impersonation (30+ brands)</li>
                <li><i /> High-risk TLDs (.xyz, .top, .buzz, .tk, etc.)</li>
                <li><i /> Obfuscated IP addresses & Hex encoding</li>
                <li><i /> Subdomain depth & Shannon entropy</li>
                <li><i /> Credential harvesting triggers</li>
              </ul>
            </aside>
          </div>

          {report ? (
            <>
              <div className="phishing-metrics">
                <Metric label="RISK SCORE" value={`${report.risk_score}/100`} tone={report.risk_score >= 60 ? "pink" : report.risk_score >= 30 ? "violet" : "green"} />
                <Metric label="RISK LEVEL" value={report.risk_level || "UNKNOWN"} tone={report.risk_score >= 60 ? "pink" : "blue"} />
                <Metric label="TOTAL FINDINGS" value={metrics.total_findings || findings.length || 0} tone="violet" />
                <Metric label="ENTROPY" value={metrics.url_entropy ? `${metrics.url_entropy.toFixed(2)}` : "Normal"} tone="blue" />
              </div>

              {/* TARGETED BRAND & SPOOFING ASSESSMENT */}
              {report.is_verified_official ? (
                <div style={{
                  padding: "16px 20px",
                  borderRadius: "12px",
                  background: "rgba(74, 222, 128, 0.12)",
                  border: "1px solid rgba(74, 222, 128, 0.35)",
                  color: "#4ade80",
                  marginBottom: "20px",
                  display: "flex",
                  alignItems: "center",
                  gap: "14px"
                }}>
                  <CheckCircle2 size={24} color="#4ade80" />
                  <div>
                    <strong style={{ fontSize: "14px", display: "block" }}>
                      VERIFIED OFFICIAL BRAND INFRASTRUCTURE
                    </strong>
                    <span style={{ fontSize: "12px", color: "#a7f3d0" }}>
                      This domain matches confirmed, authentic corporate infrastructure. Zero phishing or lookalike indicators detected.
                    </span>
                  </div>
                </div>
              ) : report.ethical_hacking_profile?.targeted_brand ? (
                <div style={{
                  padding: "16px 20px",
                  borderRadius: "12px",
                  background: "rgba(250, 55, 195, 0.15)",
                  border: "1px solid rgba(250, 55, 195, 0.4)",
                  color: "#ff7be2",
                  marginBottom: "20px",
                  display: "flex",
                  alignItems: "center",
                  gap: "14px"
                }}>
                  <ShieldAlert size={24} color="#fa37c3" />
                  <div>
                    <strong style={{ fontSize: "14px", display: "block", textTransform: "uppercase", letterSpacing: "0.05em" }}>
                      TARGETED ENTITY: {report.ethical_hacking_profile.targeted_brand}
                    </strong>
                    <span style={{ fontSize: "12px", color: "#ffd6f4" }}>
                      {report.ethical_hacking_profile.attack_vector}
                    </span>
                  </div>
                </div>
              ) : null}

              {/* MITRE ATT&CK MATRIX & SOC REMEDIATION */}
              {report.ethical_hacking_profile?.mitre_techniques?.length > 0 && (
                <div style={{
                  display: "grid",
                  gridTemplateColumns: "1fr 1fr",
                  gap: "16px",
                  marginBottom: "22px"
                }}>
                  {/* MITRE ATT&CK MATRIX */}
                  <div style={{
                    padding: "18px 20px",
                    borderRadius: "12px",
                    background: "rgba(10, 14, 32, 0.75)",
                    border: "1px solid rgba(154, 85, 255, 0.3)",
                  }}>
                    <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "12px" }}>
                      <Terminal size={17} color="#00f2fe" />
                      <strong style={{ font: "700 12px 'DM Mono', monospace", color: "#00f2fe", textTransform: "uppercase" }}>
                        MITRE ATT&CK Mappings
                      </strong>
                    </div>
                    <div style={{ display: "flex", flexWrap: "wrap", gap: "8px", marginBottom: "12px" }}>
                      {report.ethical_hacking_profile.mitre_tactics.map((tac) => (
                        <span key={tac} style={{
                          padding: "3px 9px",
                          borderRadius: "4px",
                          background: "rgba(0, 242, 254, 0.12)",
                          border: "1px solid rgba(0, 242, 254, 0.25)",
                          color: "#7df9ff",
                          fontSize: "11px",
                          fontFamily: "'DM Mono', monospace",
                          fontWeight: "600"
                        }}>
                          {tac}
                        </span>
                      ))}
                    </div>
                    <ul style={{ margin: 0, paddingLeft: "18px", color: "#d0cce6", fontSize: "12px", lineHeight: "1.7" }}>
                      {report.ethical_hacking_profile.mitre_techniques.map((tech) => (
                        <li key={tech.id}>
                          <strong style={{ color: "#fa37c3", fontFamily: "'DM Mono', monospace" }}>{tech.id}</strong>: {tech.name}
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* SOC INCIDENT RESPONSE PLAYBOOK */}
                  <div style={{
                    padding: "18px 20px",
                    borderRadius: "12px",
                    background: "rgba(10, 14, 32, 0.75)",
                    border: "1px solid rgba(250, 55, 195, 0.3)",
                  }}>
                    <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "12px" }}>
                      <Shield size={17} color="#fa37c3" />
                      <strong style={{ font: "700 12px 'DM Mono', monospace", color: "#fa37c3", textTransform: "uppercase" }}>
                        SOC Incident Response Actions
                      </strong>
                    </div>
                    <ul style={{ margin: 0, paddingLeft: "18px", color: "#d0cce6", fontSize: "12px", lineHeight: "1.7" }}>
                      {report.ethical_hacking_profile.soc_remediation.map((act, i) => (
                        <li key={i}>{act}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}

              <section className="phishing-results">
                <div className="phishing-results-heading">
                  <div>
                    <p className="eyebrow">HEURISTIC REPORT</p>
                    <h3>Risk Breakdown & Evidence</h3>
                    <span>{report.normalized_url}</span>
                  </div>
                  <ShieldCheck size={21} />
                </div>

                {findings.length ? (
                  <div className="phishing-findings">
                    {findings.map((finding, index) => (
                      <article className="phishing-finding" key={`${finding.title}-${index}`}>
                        <div>
                          <AlertTriangle size={19} />
                        </div>
                        <section>
                          <header>
                            <strong>{finding.title}</strong>
                            <b className={finding.severity?.toLowerCase()}>{finding.severity}</b>
                          </header>
                          <p>{finding.description}</p>
                          {finding.evidence && (
                            <code style={{ display: "block", margin: "6px 0", background: "rgba(0,0,0,0.4)", padding: "4px 8px", borderRadius: "4px", fontSize: "11px", color: "#85dfff" }}>
                              Evidence: {finding.evidence}
                            </code>
                          )}
                          <small>{finding.recommendation || finding.category}</small>
                        </section>
                      </article>
                    ))}
                  </div>
                ) : (
                  <div className="phishing-safe">
                    <CheckCircle2 size={23} />
                    <div>
                      <strong>No suspicious phishing indicators flagged</strong>
                      <p>URL lexical checks, brand matching, and structure passed without triggering high-risk rules.</p>
                    </div>
                  </div>
                )}
              </section>
            </>
          ) : (
            <section className="phishing-standby">
              <ShieldCheck size={22} />
              <div>
                <strong>Phishing Engine Ready</strong>
                <p>Paste any suspicious URL above to run the 20+ heuristic threat evaluation suite.</p>
              </div>
            </section>
          )}
        </>
      )}

      {/* TAB 3: Scam Message Triage */}
      {activeTab === "triage" && (
        <div style={{ display: "grid", gridTemplateColumns: "1.1fr 0.9fr", gap: "20px" }}>
          <form className="crypto-tool-card" onSubmit={runEmailTriage} style={{ padding: "24px" }}>
            <div className="crypto-card-heading">
              <div>
                <span>EMAIL · SMS · OTP · SCAM TRIAGE</span>
                <h3>Paste a suspicious message</h3>
              </div>
              <Mail size={20} color="#ff86de" />
            </div>
            <p style={{ color: "#8e9ab8", fontSize: "13px", lineHeight: "1.5", margin: "0 0 14px" }}>
              Paste an email, SMS, WhatsApp message, fake support chat, OTP request, delivery notice, or crypto scam. Analysis stays local; it extracts links and explains the warning signals it finds.
            </p>

            <textarea
              rows={8}
              value={emailText}
              onChange={(e) => setEmailText(e.target.value)}
              placeholder={`Example:
Your bank account will be blocked today. Share the OTP we just sent to verify your identity.
Open https://example-security-check.com now to avoid suspension.`}
              style={{
                width: "100%",
                background: "rgba(5, 8, 20, 0.8)",
                border: "1px solid rgba(120, 135, 190, 0.3)",
                borderRadius: "8px",
                color: "#e2e8f0",
                padding: "12px",
                fontSize: "13px",
                boxSizing: "border-box",
                fontFamily: "monospace"
              }}
            />

            <button
              type="submit"
              disabled={triageLoading}
              className="phishing-run-button"
              style={{ marginTop: "16px", width: "100%" }}
            >
              {triageLoading ? <RefreshCw className="spin-icon" size={16} /> : <Search size={16} />}
              {triageLoading ? "ANALYZING MESSAGE..." : "ANALYZE SCAM SIGNALS"}
            </button>
            {triageError && <p className="phishing-error">{triageError}</p>}
          </form>

          <div className="crypto-side-card" style={{ padding: "24px" }}>
            <span style={{ color: "#8f9abb", fontSize: "10px", fontWeight: "800", letterSpacing: "1px" }}>TRIAGE INTELLIGENCE</span>
            <h3 style={{ color: "#edf0ff", margin: "4px 0 16px", fontSize: "18px" }}>Scam-risk assessment</h3>

            {triageReport ? (
              <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
                <div style={{ padding: "12px", borderRadius: "8px", background: triageReport.risk_score >= 70 ? "rgba(239,68,68,0.16)" : triageReport.risk_score >= 45 ? "rgba(245,158,11,0.14)" : "rgba(34,197,94,0.12)", border: "1px solid rgba(255,255,255,0.09)" }}>
                  <small style={{ color: "#94a3b8", display: "block", letterSpacing: "0.8px" }}>LOCAL HEURISTIC RISK</small>
                  <strong style={{ display: "block", marginTop: "2px", color: triageReport.risk_score >= 70 ? "#fca5a5" : triageReport.risk_score >= 45 ? "#fcd34d" : "#86efac", fontSize: "22px" }}>
                    {triageReport.risk_level || "REVIEW"} · {triageReport.risk_score ?? 0}/100
                  </strong>
                  <small style={{ color: "#94a3b8", display: "block", marginTop: "5px", lineHeight: "1.35" }}>{triageReport.assessment_note || "Signals are warnings, not proof of sender identity."}</small>
                </div>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px" }}>
                  <div style={{ background: "rgba(0,0,0,0.3)", padding: "10px", borderRadius: "8px" }}>
                    <small style={{ color: "#7482a5", display: "block" }}>LINKS FOUND</small>
                    <strong style={{ fontSize: "18px", color: "#38bdf8" }}>{triageReport.total_links}</strong>
                  </div>
                  <div style={{ background: "rgba(0,0,0,0.3)", padding: "10px", borderRadius: "8px" }}>
                    <small style={{ color: "#7482a5", display: "block" }}>SIGNAL GROUPS</small>
                    <strong style={{ fontSize: "18px", color: (triageReport.scam_patterns || triageReport.urgency_triggers || []).length ? "#f87171" : "#4ade80" }}>
                      {(triageReport.scam_patterns || triageReport.urgency_triggers || []).length}
                    </strong>
                  </div>
                </div>

                {(triageReport.scam_patterns || triageReport.urgency_triggers || []).length > 0 && (
                  <div>
                    <strong style={{ fontSize: "12px", color: "#f87171" }}>Warning signals detected:</strong>
                    <div style={{ marginTop: "6px", display: "flex", flexWrap: "wrap", gap: "6px" }}>
                      {(triageReport.scam_patterns || triageReport.urgency_triggers || []).map((trig, i) => (
                        <span key={i} style={{ background: "rgba(239,68,68,0.2)", border: "1px solid rgba(239,68,68,0.4)", color: "#fca5a5", padding: "3px 8px", borderRadius: "6px", fontSize: "11px" }}>
                          {trig.category} ({trig.keywords.join(", ")})
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {triageReport.reasons?.length > 0 && (
                  <div>
                    <strong style={{ fontSize: "12px", color: "#fcd34d" }}>Assessment rationale & evidence:</strong>
                    <ul style={{ margin: "6px 0 0", paddingLeft: "18px", color: "#fef08a", fontSize: "12px", lineHeight: "1.45" }}>
                      {triageReport.reasons.map((r, i) => (
                        <li key={i}>{r}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {triageReport.is_uncertain && (
                  <div style={{ padding: "8px 12px", background: "rgba(234,179,8,0.15)", border: "1px solid rgba(234,179,8,0.4)", borderRadius: "6px", fontSize: "11px", color: "#fef08a" }}>
                    ⚠️ <strong>Uncertain Result:</strong> Mixed signals detected. Some security or banking terms may appear legitimately. Verify through the official institution directly.
                  </div>
                )}

                <div>
                  <strong style={{ fontSize: "12px", color: "#85dfff" }}>Extracted Links:</strong>
                  {triageReport.extracted_urls.length > 0 ? (
                    <div style={{ marginTop: "6px", display: "flex", flexDirection: "column", gap: "6px" }}>
                      {triageReport.extracted_urls.map((u, i) => (
                        <div key={i} style={{ background: "rgba(0,0,0,0.4)", padding: "8px 10px", borderRadius: "6px", fontSize: "12px", wordBreak: "break-all" }}>
                          <code style={{ color: "#ff86de" }}>{u}</code>
                          <button
                            type="button"
                            onClick={() => { setTarget(u); setActiveTab("url"); }}
                            style={{ display: "block", marginTop: "4px", background: "none", border: "none", color: "#38bdf8", cursor: "pointer", fontSize: "11px", padding: 0 }}
                          >
                            Inspect this link in URL Risk Engine &rarr;
                          </button>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p style={{ color: "#7482a5", fontSize: "12px", marginTop: "4px" }}>No web links were detected in the supplied text.</p>
                  )}
                </div>

                {triageReport.recommended_actions?.length > 0 && (
                  <div>
                    <strong style={{ fontSize: "12px", color: "#85dfff" }}>Recommended next steps:</strong>
                    <ul style={{ margin: "6px 0 0", paddingLeft: "18px", color: "#cbd5e1", fontSize: "12px", lineHeight: "1.55" }}>
                      {triageReport.recommended_actions.map((action, i) => <li key={i}>{action}</li>)}
                    </ul>
                  </div>
                )}
              </div>
            ) : (
              <div style={{ color: "#7482a5", fontSize: "13px" }}>
                Paste the message content on the left to extract links, uncover urgent phishing tactics, and review threat scores.
              </div>
            )}
          </div>
        </div>
      )}

      {/* TAB 4: Incident Response Playbook */}
      {activeTab === "playbook" && (
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px" }}>
          <div className="crypto-tool-card" style={{ padding: "24px" }}>
            <span style={{ color: "#ff81df", fontSize: "10px", fontWeight: "800", letterSpacing: "1px" }}>TACTICAL DEFENSE</span>
            <h3 style={{ color: "#fff", margin: "4px 0 16px" }}>Immediate Containment Protocol</h3>
            
            <div style={{ display: "flex", flexDirection: "column", gap: "16px", color: "#cbd5e1", fontSize: "13px" }}>
              <div style={{ background: "rgba(0,0,0,0.3)", padding: "12px", borderRadius: "8px" }}>
                <strong style={{ color: "#38bdf8", display: "block", marginBottom: "4px" }}>Step 1: Network Sinkholing & DNS Blocking</strong>
                Add the offending domain to your local Pi-hole, firewall, or DNS provider blocklist (e.g. Cloudflare Gateway, NextDNS) to block outbound employee resolution.
              </div>
              <div style={{ background: "rgba(0,0,0,0.3)", padding: "12px", borderRadius: "8px" }}>
                <strong style={{ color: "#ff81df", display: "block", marginBottom: "4px" }}>Step 2: Submit to Global Threat Feeds</strong>
                Report the malicious domain to Google Safe Browsing and Microsoft Defender SmartScreen to protect millions of worldwide endpoints.
              </div>
              <div style={{ background: "rgba(0,0,0,0.3)", padding: "12px", borderRadius: "8px" }}>
                <strong style={{ color: "#facc15", display: "block", marginBottom: "4px" }}>Step 3: Domain Takedown & Registrar Abuse</strong>
                Perform WHOIS query to determine the registrar and host, then send an abuse email with evidence to terminate the malicious hosting.
              </div>
              <div style={{ background: "rgba(0,0,0,0.3)", padding: "12px", borderRadius: "8px" }}>
                <strong style={{ color: "#4ade80", display: "block", marginBottom: "4px" }}>Step 4: User Remediation</strong>
                If any user visited the site, force immediate password reset, revoke active OAuth sessions, and verify MFA device registrations.
              </div>
            </div>
          </div>

          <div className="crypto-side-card" style={{ padding: "24px" }}>
            <span style={{ color: "#8f9abb", fontSize: "10px", fontWeight: "800", letterSpacing: "1px" }}>QUICK REPORTING LINKS</span>
            <h3 style={{ color: "#fff", margin: "4px 0 16px" }}>Official Abuse Gateways</h3>
            
            <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
              {[
                { title: "Google Safe Browsing Report", url: "https://safebrowsing.google.com/safebrowsing/report_phish/", note: "Submits to Chrome, Firefox, and Safari blocklists" },
                { title: "Microsoft Defender SmartScreen", url: "https://www.microsoft.com/en-us/wdsi/support/report-unsafe-site", note: "Submits to Edge and Windows Defender" },
                { title: "CISA / US-CERT Phishing Report", url: "https://www.cisa.gov/report", note: "Federal cyber threat notification" },
                { title: "Anti-Phishing Working Group (APWG)", url: "https://apwg.org/reportphishing/", note: "Global clearinghouse for phishing telemetry" }
              ].map((link, i) => (
                <a
                  key={i}
                  href={link.url}
                  target="_blank"
                  rel="noreferrer"
                  style={{
                    display: "block",
                    padding: "12px",
                    borderRadius: "8px",
                    background: "rgba(255, 255, 255, 0.03)",
                    border: "1px solid rgba(120, 135, 190, 0.2)",
                    textDecoration: "none",
                    color: "#f1f5f9"
                  }}
                >
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <strong style={{ color: "#85dfff", fontSize: "13px" }}>{link.title}</strong>
                    <ExternalLink size={14} color="#85dfff" />
                  </div>
                  <small style={{ color: "#7482a5", display: "block", marginTop: "3px" }}>{link.note}</small>
                </a>
              ))}
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
