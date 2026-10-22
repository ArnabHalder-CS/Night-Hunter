import { useEffect, useState } from "react";
import { AlertTriangle, CheckCircle2, Cpu, Network, Radar, RefreshCw, Server, ShieldCheck, Terminal } from "lucide-react";

export default function NmapWorkspace() {
  const [status, setStatus] = useState(null);
  const [target, setTarget] = useState("");
  const [profile, setProfile] = useState("inventory");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [running, setRunning] = useState(false);

  useEffect(() => {
    fetch("/api/network-security/nmap/status")
      .then((response) => response.json())
      .then((data) => setStatus(data.nmap))
      .catch(() => setStatus({ available: false, reason: "Unable to check local Nmap availability.", profiles: [] }));
  }, []);

  async function scan(event) {
    event.preventDefault();
    if (!target.trim()) { setError("Enter a host or IP address you are authorized to scan."); return; }
    setRunning(true); setError(""); setResult(null);
    try {
      const response = await fetch("/api/network-security/nmap", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ target: target.trim(), profile }) });
      const data = await response.json();
      if (!response.ok || !data.success) throw new Error(data.error || "Nmap scan failed.");
      setResult(data);
    } catch (scanError) { setError(scanError.message); } finally { setRunning(false); }
  }

  const profiles = status?.profiles || [];
  const selected = profiles.find((item) => item.id === profile);
  const host = result?.hosts?.[0];
  const openPorts = host?.ports?.filter((port) => port.state === "OPEN") || [];

  return <section className="nmap-workspace">
    <header className="module-header network-module-header"><div className="module-heading"><div className="module-heading-icon"><Radar size={24} /></div><div><p className="eyebrow">NIGHT HUNTER · LOCAL NMAP</p><h2>Verified Nmap Workspace</h2><p className="subtitle">Named profiles · XML evidence · no simulated findings</p></div></div><div className={`module-state ${running ? "busy" : status?.available ? "success" : ""}`}><span />{running ? "SCANNING" : status?.available ? "NMAP READY" : "NMAP UNAVAILABLE"}</div></header>

    {status?.runtime === "cloud" && <section className="cloud-network-summary"><Server size={20} /><div><span>PUBLIC DASHBOARD</span><h3>Network scans run from the installed Night Hunter app</h3><p>The public site does not initiate scans. Open the downloaded Windows, Linux, or Termux application to use your device’s local Nmap engine and receive the complete evidence report.</p></div></section>}
    {status?.runtime !== "cloud" && <div className="network-caution-banner"><div className="caution-icon-box"><AlertTriangle size={18} /></div><div><strong>AUTHORIZED USE:</strong> Local Nmap scans run from this computer. Use only with systems and networks you own or are authorized to assess.</div></div>}

    {status?.runtime !== "cloud" && <form className="nmap-form" onSubmit={scan}>
      <label>AUTHORIZED TARGET<input value={target} onChange={(event) => setTarget(event.target.value)} disabled={running || !status?.available} placeholder="192.168.1.20 or host.local" /></label>
      <label>NMAP PROFILE<select value={profile} onChange={(event) => setProfile(event.target.value)} disabled={running || !status?.available}>{profiles.map((item) => <option key={item.id} value={item.id}>{item.label}</option>)}</select></label>
      <button className="advanced-network-run" disabled={running || !status?.available} type="submit">{running ? <RefreshCw className="spin-icon" size={17} /> : <Radar size={17} />}{running ? "RUNNING NMAP..." : "RUN LOCAL NMAP"}</button>
      {error && <p className="advanced-network-error"><AlertTriangle size={16} />{error}</p>}
      <p className="advanced-network-note"><ShieldCheck size={15} />{status?.reason || "Checking local Nmap…"}</p>
    </form>}

    {selected && <section className="nmap-profile-note"><Terminal size={18} /><div><strong>{selected.label}</strong><p>{selected.description}</p>{selected.requires_admin && <small>OS or UDP features may require Administrator/root privileges.</small>}</div></section>}

    {result && <><section className="nmap-results-heading"><div><span>VERIFIED NMAP REPORT</span><h3>{host?.hostname || host?.addresses?.[0] || result.target}</h3><code>{result.engine} · {result.command}</code></div><Network size={22} /></section>
      <div className="advanced-network-metrics"><Metric icon={Server} label="HOST STATUS" value={host?.status?.toUpperCase() || "UNKNOWN"} tone="blue" /><Metric icon={Cpu} label="OS RESULT" value={host?.os || "INCONCLUSIVE"} tone="violet" /><Metric icon={Terminal} label="OPEN PORTS" value={openPorts.length} tone="green" /><Metric icon={Network} label="PROFILE" value={result.profile.label} tone="pink" /></div>
      <section className="network-result-card"><div className="result-card-heading"><div><span>MEASURED PORT RESULTS</span><h3>Open services ({openPorts.length})</h3></div><Server size={19} /></div>{openPorts.length ? <div className="advanced-port-list">{openPorts.map((port) => <article key={`${port.protocol}-${port.port}`}><b>{port.port}</b><div><strong>{port.service}</strong><span>{port.protocol} {port.product ? `· ${port.product} ${port.version}` : ""}</span></div><em>OPEN</em></article>)}</div> : <div className="result-empty"><CheckCircle2 size={21} /><p>No open ports were reported by this Nmap profile.</p></div>}</section>
      <p className="nmap-evidence-note">{result.warning}</p></>}
  </section>;
}

function Metric({ icon: Icon, label, value, tone }) { return <article className="network-metric-card"><div className={`network-metric-icon ${tone}`}><Icon size={19} /></div><div><span>{label}</span><strong>{value}</strong></div></article>; }
