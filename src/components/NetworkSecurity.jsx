import { useState } from "react";
import {
  Activity,
  AlertTriangle,
  ArrowRight,
  CheckCircle2,
  ChevronDown,
  Cpu,
  Globe,
  Hash,
  Laptop,
  Play,
  Radar,
  Radio,
  RefreshCw,
  RotateCcw,
  Router,
  Search,
  Server,
  Shield,
  ShieldAlert,
  ShieldCheck,
  Signal,
  Terminal,
  User,
  Wifi,
  XCircle,
  Zap,
} from "lucide-react";
import "./NetworkSpeed.css";

const QUICK_TARGETS = [
  { label: "Default Gateway", value: "192.168.1.1" },
  { label: "Cloudflare Edge", value: "1.1.1.1" },
  { label: "Google Public DNS", value: "8.8.8.8" },
  { label: "Localhost", value: "127.0.0.1" },
];

export default function NetworkSecurity() {
  const [target, setTarget] = useState("");
  const [scanning, setScanning] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [activeFilter, setActiveFilter] = useState("all"); // 'all', 'open', 'filtered'

  async function handleScan(e) {
    if (e && e.preventDefault) e.preventDefault();
    const cleanTarget = target.trim();

    if (!cleanTarget) {
      setError("Please enter a target IP address or hostname to initiate scan.");
      setResult(null);
      return;
    }

    setScanning(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("/api/network-security", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ target: cleanTarget }),
      });

      const data = await response.json();
      if (!response.ok || !data.success) {
        throw new Error(data.error || "Network reconnaissance scan failed.");
      }

      setResult(data.result);
    } catch (err) {
      console.error("Scan error:", err);
      setError(err.message || "Failed to connect to network scan engine.");
    } finally {
      setScanning(false);
    }
  }

  function setQuickTarget(val) {
    setTarget(val);
    setError("");
  }

  const portsList = result?.ports_list || [];
  const openPorts = result?.open_ports || [];
  const filteredPorts = result?.filtered_ports || [];
  const posture = result?.security_posture || {};
  const telemetry = result?.latency_telemetry || {};
  const riskFlags = posture.risk_flags || [];

  const displayedPorts =
    activeFilter === "open"
      ? openPorts
      : activeFilter === "filtered"
      ? filteredPorts
      : portsList;

  return (
    <div className="recon-page">
      {/* HEADER */}
      <header className="recon-header">
        <div className="recon-header-left">
          <div className="recon-icon-badge">
            <Radar size={28} />
          </div>
          <div>
            <h2>Target Network Reconnaissance (0 – 65535)</h2>
            <p>Nmap -T5 Fast Turbo Scan • Showing only OPEN or FILTERED ports • Zero clutter</p>
          </div>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <span
            style={{
              font: "700 11px 'DM Mono', monospace",
              padding: "6px 14px",
              borderRadius: "999px",
              background: scanning ? "rgba(250, 55, 195, 0.15)" : result ? "rgba(74, 222, 128, 0.15)" : "rgba(255,255,255,0.06)",
              border: `1px solid ${scanning ? "#fa37c3" : result ? "#4ade80" : "rgba(255,255,255,0.15)"}`,
              color: scanning ? "#ff7be2" : result ? "#4ade80" : "#a8b0c8",
              textTransform: "uppercase",
              display: "flex",
              alignItems: "center",
              gap: "6px",
            }}
          >
            <Zap size={13} color={scanning ? "#fa37c3" : "#00f2fe"} />
            {scanning ? "T5 SCANNING 65,535 PORTS..." : result ? `COMPLETED IN ${result.scan_duration_sec}s` : "NMAP T5 TURBO"}
          </span>
        </div>
      </header>

      {/* TARGET INPUT WORKSPACE */}
      <section
        style={{
          background: "linear-gradient(135deg, rgba(17, 24, 48, 0.95), rgba(10, 11, 24, 0.95))",
          border: "1px solid rgba(0, 242, 254, 0.25)",
          borderRadius: "16px",
          padding: "26px 28px",
          marginBottom: "26px",
          boxShadow: "0 10px 30px rgba(0,0,0,0.4)",
        }}
      >
        <form onSubmit={handleScan}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "10px" }}>
            <label
              style={{
                font: "700 12px 'DM Mono', monospace",
                color: "#00f2fe",
                letterSpacing: "0.08em",
                textTransform: "uppercase",
              }}
            >
              Target IP Address or Hostname:
            </label>
            <span style={{ font: "600 11px 'DM Mono', monospace", color: "#a8b0c8" }}>
              Range: <strong>0 – 65535</strong> (Fast T5 Parallel Sockets)
            </span>
          </div>

          <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" }}>
            <div style={{ flex: "1 1 340px", position: "relative" }}>
              <input
                type="text"
                placeholder="Enter IP (e.g. 192.168.1.1, 8.8.8.8, 1.1.1.1, or domain)"
                value={target}
                onChange={(e) => {
                  setTarget(e.target.value);
                  if (error) setError("");
                }}
                disabled={scanning}
                style={{
                  width: "100%",
                  boxSizing: "border-box",
                  background: "rgba(6, 8, 18, 0.85)",
                  border: "1px solid rgba(0, 242, 254, 0.3)",
                  borderRadius: "8px",
                  padding: "13px 18px",
                  color: "#fff",
                  font: "600 14px 'DM Mono', monospace",
                  outline: "none",
                }}
              />
            </div>
            <button
              type="submit"
              disabled={scanning}
              className="recon-run-btn"
              style={{ padding: "13px 28px", fontSize: "14px" }}
            >
              {scanning ? (
                <>
                  <RefreshCw size={17} className="network-spin" />
                  <span>T5 PARALLEL SCANNING...</span>
                </>
              ) : (
                <>
                  <Search size={17} />
                  <span>SCAN PORTS (0 - 65535)</span>
                </>
              )}
            </button>
          </div>
        </form>

        {/* QUICK PRESET PILLS */}
        <div style={{ marginTop: "14px", display: "flex", alignItems: "center", gap: "10px", flexWrap: "wrap" }}>
          <span style={{ font: "600 11px 'DM Mono', monospace", color: "#8c9ac2" }}>Presets:</span>
          {QUICK_TARGETS.map((q) => (
            <button
              key={q.value}
              type="button"
              onClick={() => setQuickTarget(q.value)}
              style={{
                background: target === q.value ? "rgba(0, 242, 254, 0.18)" : "rgba(255, 255, 255, 0.04)",
                border: `1px solid ${target === q.value ? "#00f2fe" : "rgba(255, 255, 255, 0.12)"}`,
                color: target === q.value ? "#00f2fe" : "#a8b0c8",
                padding: "4px 12px",
                borderRadius: "6px",
                font: "600 11px 'DM Mono', monospace",
                cursor: "pointer",
                transition: "all 0.2s ease",
              }}
            >
              {q.label} (<code>{q.value}</code>)
            </button>
          ))}
        </div>
      </section>

      {/* ERROR BANNER */}
      {error && (
        <div
          style={{
            marginBottom: "24px",
            padding: "14px 20px",
            borderRadius: "10px",
            background: "rgba(239, 68, 68, 0.15)",
            border: "1px solid rgba(239, 68, 68, 0.35)",
            color: "#fca5a5",
            fontSize: "13px",
            display: "flex",
            alignItems: "center",
            gap: "10px",
          }}
        >
          <AlertTriangle size={18} />
          <span>{error}</span>
        </div>
      )}

      {/* IDLE PLACEHOLDER */}
      {!result && !scanning && !error && (
        <div
          style={{
            textAlign: "center",
            padding: "70px 24px",
            background: "radial-gradient(circle at 50% 50%, rgba(154, 85, 255, 0.06), rgba(9, 11, 22, 0.98))",
            border: "1px dashed rgba(255, 255, 255, 0.12)",
            borderRadius: "18px",
          }}
        >
          <Radar size={48} color="#8c9ac2" style={{ margin: "0 auto 16px", opacity: 0.6 }} />
          <h3 style={{ fontSize: "19px", color: "#fff", margin: "0 0 8px" }}>Awaiting Target Specification</h3>
          <p style={{ color: "#8c9ac2", fontSize: "14px", maxWidth: "560px", margin: "0 auto", lineHeight: "1.6" }}>
            Enter a target IP or host to execute an <strong>Nmap -T5 style fast parallel scan across ports 0 – 65,535</strong>. Only ports confirmed <strong>OPEN</strong> or <strong>FILTERED by firewall</strong> will be displayed.
          </p>
        </div>
      )}

      {/* ACTIVE SCANNING PROGRESS */}
      {scanning && (
        <div
          style={{
            textAlign: "center",
            padding: "50px 24px",
            background: "rgba(16, 22, 44, 0.7)",
            border: "1px solid rgba(250, 55, 195, 0.3)",
            borderRadius: "16px",
            marginBottom: "24px",
          }}
        >
          <RefreshCw size={36} color="#fa37c3" className="network-spin" style={{ margin: "0 auto 14px" }} />
          <h3 style={{ fontSize: "18px", color: "#fff", margin: "0 0 6px" }}>Scanning All Ports (0 – 65535)...</h3>
          <p style={{ color: "#c9c3d5", fontSize: "13px", fontFamily: "'DM Mono', monospace" }}>
            Dispatching 120 concurrent worker sockets • Timing Template: T5 Insane • Filtering closed ports
          </p>
        </div>
      )}

      {/* SCAN RESULTS DASHBOARD */}
      {result && (
        <>
          {/* TARGET OVERVIEW BANNER */}
          <section className="recon-posture-banner">
            <div className="posture-score-box">
              <div className="posture-score-number" style={{ color: posture.grade_color || "#4ade80" }}>
                {posture.defense_score ?? 85}
                <small style={{ fontSize: "16px", color: "#8c9ac2" }}>/100</small>
              </div>
              <div>
                <span
                  className="posture-grade-badge"
                  style={{
                    background: `${posture.grade_color || "#4ade80"}22`,
                    border: `1px solid ${posture.grade_color || "#4ade80"}66`,
                    color: posture.grade_color || "#4ade80",
                  }}
                >
                  {posture.posture_grade || "HARDENED"}
                </span>
                <p className="posture-detail-text" style={{ marginTop: "4px" }}>
                  Scan finished in <strong>{result.scan_duration_sec}s</strong> • Found <strong>{result.total_open_ports} open</strong>, <strong>{result.total_filtered_ports} filtered</strong>
                </p>
              </div>
            </div>

            <div style={{ display: "flex", gap: "12px", alignItems: "center", flexWrap: "wrap" }}>
              <div
                style={{
                  padding: "8px 16px",
                  borderRadius: "8px",
                  background: "rgba(255, 255, 255, 0.04)",
                  border: "1px solid rgba(255, 255, 255, 0.1)",
                  textAlign: "right",
                }}
              >
                <span style={{ display: "block", font: "700 10px 'DM Mono', monospace", color: "#8c9ac2", textTransform: "uppercase" }}>
                  Resolved Target
                </span>
                <strong style={{ fontSize: "14px", color: "#00f2fe", fontFamily: "'DM Mono', monospace" }}>
                  {result.target_ip}
                </strong>
              </div>

              <div
                style={{
                  padding: "8px 16px",
                  borderRadius: "8px",
                  background: "rgba(255, 255, 255, 0.04)",
                  border: "1px solid rgba(255, 255, 255, 0.1)",
                  textAlign: "right",
                }}
              >
                <span style={{ display: "block", font: "700 10px 'DM Mono', monospace", color: "#8c9ac2", textTransform: "uppercase" }}>
                  Reverse DNS (PTR)
                </span>
                <strong style={{ fontSize: "13px", color: "#c084fc", fontFamily: "'DM Mono', monospace" }}>
                  {result.ptr_record}
                </strong>
              </div>
            </div>
          </section>

          {/* FOUR METRICS CARDS */}
          <section className="recon-grid">
            <article className="recon-card">
              <div className="recon-card-header">
                <span>SCANNED RANGE</span>
                <Zap size={16} color="#00f2fe" />
              </div>
              <div className="recon-card-val" style={{ color: "#00f2fe" }}>
                0 – 65,535
              </div>
              <p className="recon-card-sub">
                Execution speed: <strong>{result.scan_duration_sec}s</strong> (Nmap T5)
              </p>
            </article>

            <article className="recon-card">
              <div className="recon-card-header">
                <span>OPEN PORTS</span>
                <CheckCircle2 size={16} color="#4ade80" />
              </div>
              <div className="recon-card-val" style={{ color: "#4ade80" }}>
                {result.total_open_ports}
              </div>
              <p className="recon-card-sub">
                Reachable active services
              </p>
            </article>

            <article className="recon-card">
              <div className="recon-card-header">
                <span>FILTERED BY FIREWALL</span>
                <Shield size={16} color="#fbbf24" />
              </div>
              <div className="recon-card-val" style={{ color: "#fbbf24" }}>
                {result.total_filtered_ports}
              </div>
              <p className="recon-card-sub">
                Packets dropped / firewall filtered
              </p>
            </article>

            <article className="recon-card">
              <div className="recon-card-header">
                <span>CLOSED (HIDDEN)</span>
                <ShieldAlert size={16} color="#8c9ac2" />
              </div>
              <div className="recon-card-val" style={{ color: "#8c9ac2" }}>
                {result.closed_ports_hidden.toLocaleString()}
              </div>
              <p className="recon-card-sub">
                Omitted from table to prevent clutter
              </p>
            </article>
          </section>

          {/* OPEN & FILTERED PORTS RESULTS TABLE */}
          <section className="recon-section-card">
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px", flexWrap: "wrap", gap: "12px" }}>
              <div>
                <h3 style={{ margin: "0 0 4px" }}>
                  <ShieldCheck size={18} color="#00f2fe" />
                  Open &amp; Filtered Ports Table ({result.target_ip})
                </h3>
                <small style={{ color: "#8c9ac2", fontSize: "12px", fontFamily: "'DM Mono', monospace" }}>
                  Showing only OPEN or FILTERED ports • {result.closed_ports_hidden.toLocaleString()} closed ports hidden
                </small>
              </div>

              <div style={{ display: "flex", gap: "8px" }}>
                <button
                  type="button"
                  onClick={() => setActiveFilter("all")}
                  style={{
                    background: activeFilter === "all" ? "rgba(0,242,254,0.18)" : "transparent",
                    border: `1px solid ${activeFilter === "all" ? "#00f2fe" : "rgba(255,255,255,0.12)"}`,
                    color: activeFilter === "all" ? "#00f2fe" : "#a8b0c8",
                    padding: "4px 12px",
                    borderRadius: "6px",
                    font: "700 11px 'DM Mono', monospace",
                    cursor: "pointer",
                  }}
                >
                  All Active ({portsList.length})
                </button>
                <button
                  type="button"
                  onClick={() => setActiveFilter("open")}
                  style={{
                    background: activeFilter === "open" ? "rgba(74,222,128,0.18)" : "transparent",
                    border: `1px solid ${activeFilter === "open" ? "#4ade80" : "rgba(255,255,255,0.12)"}`,
                    color: activeFilter === "open" ? "#4ade80" : "#a8b0c8",
                    padding: "4px 12px",
                    borderRadius: "6px",
                    font: "700 11px 'DM Mono', monospace",
                    cursor: "pointer",
                  }}
                >
                  Open Only ({openPorts.length})
                </button>
                {filteredPorts.length > 0 && (
                  <button
                    type="button"
                    onClick={() => setActiveFilter("filtered")}
                    style={{
                      background: activeFilter === "filtered" ? "rgba(251,191,36,0.18)" : "transparent",
                      border: `1px solid ${activeFilter === "filtered" ? "#fbbf24" : "rgba(255,255,255,0.12)"}`,
                      color: activeFilter === "filtered" ? "#fbbf24" : "#a8b0c8",
                      padding: "4px 12px",
                      borderRadius: "6px",
                      font: "700 11px 'DM Mono', monospace",
                      cursor: "pointer",
                    }}
                  >
                    Filtered ({filteredPorts.length})
                  </button>
                )}
              </div>
            </div>

            {displayedPorts.length === 0 ? (
              <div style={{ padding: "30px", textAlign: "center", color: "#8c9ac2", fontSize: "13px" }}>
                No ports matching the selected filter.
              </div>
            ) : (
              <table className="egress-table">
                <thead>
                  <tr>
                    <th>Port</th>
                    <th>Service Protocol</th>
                    <th>State</th>
                    <th>Risk Profile</th>
                    <th>Service Banner / Response</th>
                    <th>Round-Trip</th>
                  </tr>
                </thead>
                <tbody>
                  {displayedPorts.map((item) => (
                    <tr key={item.port}>
                      <td><strong>{item.port}</strong></td>
                      <td>{item.service}</td>
                      <td>
                        <span className={`status-tag ${item.state === "OPEN" ? "open" : "blocked"}`}>
                          {item.state === "OPEN" ? (
                            <>
                              <CheckCircle2 size={12} /> OPEN
                            </>
                          ) : (
                            <>
                              <Shield size={12} /> FILTERED
                            </>
                          )}
                        </span>
                      </td>
                      <td>
                        <span className={`risk-tag ${item.risk}`}>
                          {item.risk}
                        </span>
                      </td>
                      <td style={{ color: item.banner && !item.banner.includes("Firewall") ? "#79ffa8" : "#8c9ac2", fontFamily: item.banner ? "'DM Mono', monospace" : "inherit" }}>
                        {item.banner ? item.banner : item.desc}
                      </td>
                      <td>{item.latency_ms > 0 ? `${item.latency_ms} ms` : "—"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </section>

          {/* ATTACK SURFACE RISK ADVISORY */}
          {riskFlags.length > 0 && (
            <section className="recon-section-card">
              <h3>
                <ShieldAlert size={18} color="#f97316" />
                Vulnerability Exposure &amp; Threat Findings
              </h3>
              <div className="findings-list">
                {riskFlags.map((flag, idx) => (
                  <div key={idx} className={`finding-card ${flag.severity}`}>
                    <div>
                      <strong>{flag.title}</strong>
                      <p>{flag.detail}</p>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          )}
        </>
      )}
    </div>
  );
}
