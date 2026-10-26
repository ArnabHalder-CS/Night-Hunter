import { useState, useEffect } from "react";
import {
  Activity,
  AlertTriangle,
  ArrowRight,
  CheckCircle2,
  ChevronDown,
  ChevronUp,
  Cpu,
  Globe,
  Laptop,
  Play,
  Radio,
  RefreshCw,
  RotateCcw,
  Router,
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

export default function NetworkSecurity() {
  const [scanning, setScanning] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const [customHost, setCustomHost] = useState("");
  const [showAdvanced, setShowAdvanced] = useState(false);

  // Auto-run recon audit on initial load
  useEffect(() => {
    runReconAudit();
  }, []);

  async function runReconAudit(targetHost = "") {
    if (scanning) return;
    setScanning(true);
    setError("");

    try {
      const resp = await fetch("/api/network-security", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ target: targetHost.trim() }),
      });

      const res = await resp.json();
      if (!resp.ok || !res.success) {
        throw new Error(res.error || "Failed to complete network perimeter recon.");
      }

      setData(res.result);
    } catch (err) {
      console.error("Recon error:", err);
      setError(err.message || "Unable to contact local network diagnostic engine.");
    } finally {
      setScanning(false);
    }
  }

  const localNet = data?.local_network || {};
  const publicNet = data?.public_network || {};
  const telemetry = data?.latency_telemetry || {};
  const egressList = data?.egress_firewall || [];
  const posture = data?.security_posture || {};
  const riskFlags = posture.risk_flags || [];

  return (
    <div className="recon-page">
      {/* COMMAND HEADER */}
      <header className="recon-header">
        <div className="recon-header-left">
          <div className="recon-icon-badge">
            <Router size={28} />
          </div>
          <div>
            <h2>Network Perimeter &amp; Gateway Recon</h2>
            <p>Local Gateway Mapping • Outbound Firewall Egress Audit • Network Exposure Score</p>
          </div>
        </div>

        <button
          type="button"
          className="recon-run-btn"
          onClick={() => runReconAudit(customHost)}
          disabled={scanning}
        >
          {scanning ? (
            <>
              <RefreshCw size={17} className="network-spin" />
              <span>SCANNING PERIMETER...</span>
            </>
          ) : (
            <>
              <ShieldCheck size={17} />
              <span>RUN PERIMETER RECON</span>
            </>
          )}
        </button>
      </header>

      {/* ERROR NOTICE */}
      {error && (
        <div
          style={{
            marginBottom: "20px",
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

      {/* SECURITY POSTURE BANNER */}
      {data && (
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
                {posture.posture_grade || "SECURE / HARDENED"}
              </span>
              <p className="posture-detail-text" style={{ marginTop: "4px" }}>
                Defense Posture Score based on egress filters and gateway exposure
              </p>
            </div>
          </div>

          <div style={{ display: "flex", gap: "12px", alignItems: "center" }}>
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
                Active Interface
              </span>
              <strong style={{ fontSize: "13px", color: "#fff" }}>
                {localNet.interface_type || "Wi-Fi / Ethernet"}
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
                Platform Host
              </span>
              <strong style={{ fontSize: "13px", color: "#38bdf8" }}>
                {localNet.os_platform || "Universal OS"}
              </strong>
            </div>
          </div>
        </section>
      )}

      {/* CORE FOUR-PANEL RECON GRID */}
      {data && (
        <section className="recon-grid">
          {/* PANEL 1: LOCAL DEVICE IP */}
          <article className="recon-card">
            <div className="recon-card-header">
              <span>LOCAL INTERFACE</span>
              <Laptop size={16} color="#00f2fe" />
            </div>
            <div className="recon-card-val" style={{ color: "#00f2fe" }}>
              {localNet.local_ip || "127.0.0.1"}
            </div>
            <p className="recon-card-sub">
              Subnet: <strong>{localNet.subnet || "255.255.255.0"}</strong>
            </p>
          </article>

          {/* PANEL 2: DEFAULT GATEWAY */}
          <article className="recon-card">
            <div className="recon-card-header">
              <span>DEFAULT GATEWAY</span>
              <Router size={16} color="#4ade80" />
            </div>
            <div className="recon-card-val" style={{ color: "#4ade80" }}>
              {localNet.gateway_ip || "192.168.1.1"}
            </div>
            <p className="recon-card-sub">
              Gateway Ping: <strong>{telemetry.gateway_latency_ms || 1.2} ms</strong> • {telemetry.gateway_reachable ? "Reachable" : "Filtered"}
            </p>
          </article>

          {/* PANEL 3: PUBLIC PERIMETER IP */}
          <article className="recon-card">
            <div className="recon-card-header">
              <span>EXTERNAL PERIMETER</span>
              <Globe size={16} color="#c084fc" />
            </div>
            <div className="recon-card-val" style={{ color: "#c084fc", fontSize: "20px" }}>
              {publicNet.public_ip || "Dynamic External"}
            </div>
            <p className="recon-card-sub">
              ISP / Network: <strong>{publicNet.isp || "Active Carrier"}</strong>
            </p>
          </article>

          {/* PANEL 4: EDGE LATENCY & JITTER */}
          <article className="recon-card">
            <div className="recon-card-header">
              <span>LATENCY &amp; STABILITY</span>
              <Activity size={16} color="#fa37c3" />
            </div>
            <div className="recon-card-val" style={{ color: "#fa37c3" }}>
              {telemetry.edge_latency_ms || "14"} <small style={{ fontSize: "14px" }}>ms</small>
            </div>
            <p className="recon-card-sub">
              Jitter: <strong>{telemetry.jitter_ms || 2} ms</strong> • Loss: <strong>{telemetry.packet_loss || "0%"}</strong>
            </p>
          </article>
        </section>
      )}

      {/* OUTBOUND FIREWALL & EGRESS PORT FILTERING AUDIT */}
      {data && egressList.length > 0 && (
        <section className="recon-section-card">
          <h3>
            <Shield size={18} color="#00f2fe" />
            Outbound Firewall &amp; Egress Port Audit
          </h3>
          <p style={{ color: "#8c9ac2", fontSize: "13px", margin: "0 0 16px" }}>
            Tests whether the local router or ISP firewall blocks or permits outbound traffic on critical protocols.
          </p>

          <table className="egress-table">
            <thead>
              <tr>
                <th>Port</th>
                <th>Protocol / Service</th>
                <th>Egress Policy</th>
                <th>Risk Profile</th>
                <th>Security Purpose</th>
                <th>Round-Trip</th>
              </tr>
            </thead>
            <tbody>
              {egressList.map((item) => (
                <tr key={item.port}>
                  <td><strong>{item.port}</strong></td>
                  <td>{item.service}</td>
                  <td>
                    <span className={`status-tag ${item.state.includes("ALLOW") ? "open" : "blocked"}`}>
                      {item.state.includes("ALLOW") ? (
                        <>
                          <CheckCircle2 size={12} /> ALLOW / OPEN
                        </>
                      ) : (
                        <>
                          <XCircle size={12} /> BLOCKED / FILTERED
                        </>
                      )}
                    </span>
                  </td>
                  <td>
                    <span className={`risk-tag ${item.risk}`}>
                      {item.risk}
                    </span>
                  </td>
                  <td style={{ color: "#aaa" }}>{item.desc}</td>
                  <td>{item.latency_ms > 0 ? `${item.latency_ms} ms` : "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      )}

      {/* ACTIONABLE SECURITY FINDINGS & DEFENSIVE ADVISORY */}
      {data && riskFlags.length > 0 && (
        <section className="recon-section-card">
          <h3>
            <ShieldAlert size={18} color="#f97316" />
            Actionable Perimeter Findings &amp; Risk Advisory
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

      {/* ADVANCED CUSTOM TARGET PROBE (OPTIONAL) */}
      <div style={{ marginTop: "16px" }}>
        <button
          type="button"
          onClick={() => setShowAdvanced(!showAdvanced)}
          style={{
            background: "transparent",
            border: "none",
            color: "#8c9ac2",
            font: "600 12px 'DM Mono', monospace",
            cursor: "pointer",
            display: "flex",
            alignItems: "center",
            gap: "6px",
          }}
        >
          {showAdvanced ? <ChevronUp size={15} /> : <ChevronDown size={15} />}
          <span>Target Specific Gateway or Host (Optional)</span>
        </button>

        {showAdvanced && (
          <form
            onSubmit={(e) => {
              e.preventDefault();
              runReconAudit(customHost);
            }}
            style={{ display: "flex", gap: "10px", marginTop: "12px", flexWrap: "wrap" }}
          >
            <input
              type="text"
              placeholder="e.g. 192.168.1.1, 10.0.0.1, or corporate gateway"
              value={customHost}
              onChange={(e) => setCustomHost(e.target.value)}
              disabled={scanning}
              style={{
                flex: "1 1 280px",
                background: "rgba(10, 14, 28, 0.8)",
                border: "1px solid rgba(255,255,255,0.15)",
                borderRadius: "8px",
                padding: "10px 14px",
                color: "#fff",
                fontSize: "13px",
              }}
            />
            <button
              type="submit"
              disabled={scanning}
              style={{
                background: "linear-gradient(105deg, #00f2fe, #784bff)",
                border: "none",
                borderRadius: "8px",
                color: "#fff",
                font: "700 12px 'DM Mono', monospace",
                padding: "10px 18px",
                cursor: "pointer",
              }}
            >
              Audit Target Host
            </button>
            {customHost && (
              <button
                type="button"
                onClick={() => {
                  setCustomHost("");
                  runReconAudit("");
                }}
                style={{
                  background: "transparent",
                  border: "1px solid rgba(255,255,255,0.15)",
                  color: "#aaa",
                  borderRadius: "8px",
                  padding: "0 14px",
                  cursor: "pointer",
                }}
              >
                Reset to Default Gateway
              </button>
            )}
          </form>
        )}
      </div>
    </div>
  );
}
