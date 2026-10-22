import { useEffect, useState } from "react";

import {
  Globe,
  ShieldCheck,
  Activity,
  Search,
  LockKeyhole,
  AlertTriangle,
  Server,
  FileWarning,
  ArrowUpRight,
  Network,
  Code2,
  Cookie,
  KeyRound,
  Route,
  Database,
  Eye,
  RefreshCw,
  CheckCircle2,
  XCircle,
  Terminal,
} from "lucide-react";


function WebSecurity() {

  const [target, setTarget] = useState("");

  const [status, setStatus] = useState("READY");

  const [scanning, setScanning] = useState(false);

  const [report, setReport] = useState(null);

  const [error, setError] = useState("");

  const [authorized, setAuthorized] = useState(true);

  const [scannerHub, setScannerHub] = useState(null);
  const [externalScan, setExternalScan] = useState(null);
  const [externalLoading, setExternalLoading] = useState("");

  const [scanLines, setScanLines] = useState([
    "[+] Web Security engine ready.",
    "[+] Waiting for target input..."
  ]);

  useEffect(() => {
    fetch("/api/web-security/scanners")
      .then((response) => response.json())
      .then((data) => { if (data.success) setScannerHub(data); })
      .catch(() => setScannerHub(null));
  }, []);


  function addLine(line) {

    setScanLines((oldLines) => [
      ...oldLines,
      line
    ]);

  }


  function getSeverityClass(severity) {

    if (!severity) {
      return "";
    }

    return severity.toLowerCase();

  }


  function startScan(event) {
    if (event) event.preventDefault();

    let cleanTarget = target.trim();
    if (!cleanTarget) {
      setStatus("TARGET REQUIRED");
      setError("Please enter a target URL (e.g., example.com or https://example.com)");
      addLine("[!] Target URL is required.");
      return;
    }

    if (!cleanTarget.startsWith("http://") && !cleanTarget.startsWith("https://")) {
      cleanTarget = "https://" + cleanTarget;
    }

    setScanning(true);
    setStatus("SCANNING");
    setReport(null);
    setError("");

    setScanLines([
      "[+] NIGHT HUNTER Web Security scan started.",
      `[>] Target: ${cleanTarget}`,
      "[>] Connecting to Python security engine...",
      "[*] Resolving DNS & inspecting host reachability..."
    ]);

    // Live progress ticks so user sees active work in real-time
    const progressTicks = [
      "[*] Probing common web ports (80, 443, 8080, 8443)...",
      "[*] Auditing HTTP security headers (CSP, HSTS, X-Frame-Options)...",
      "[*] Inspecting SSL/TLS configuration & cipher suites...",
      "[*] Discovering public endpoints, sitemaps, and API routes...",
      "[*] Testing for exposed configuration files & misconfigurations...",
      "[*] Testing HTTP request methods & access permissions...",
      "[*] Compiling vulnerability findings & generating reports..."
    ];
    let tickIdx = 0;
    const intervalId = setInterval(() => {
      if (tickIdx < progressTicks.length) {
        addLine(progressTicks[tickIdx]);
        tickIdx++;
      }
    }, 2200);

    fetch("/api/web-security", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        target: cleanTarget,
        authorized: true
      })
    })
      .then(async (response) => {
        clearInterval(intervalId);
        const data = await response.json();
        if (!response.ok || !data.success) {
          throw new Error(
            data.error || "Web Security scan failed."
          );
        }
        return data;
      })
      .then((data) => {
        const realReport = data.report;
        setReport(realReport);
        setStatus("SCAN COMPLETE");
        setScanning(false);
        addLine("[+] Python security engine connected.");
        addLine("[+] Reconnaissance completed.");
        addLine(
          `[+] ${realReport.ports?.length || 0} open port(s) detected.`
        );
        addLine(
          `[+] ${realReport.endpoints?.length || 0} endpoint(s) analyzed.`
        );
        addLine(
          `[+] ${realReport.technology?.length || 0} technology indicator(s) detected.`
        );
        addLine(
          `[+] ${realReport.report_summary?.total || 0} finding(s) generated.`
        );
        addLine("[+] Security report completed.");
      })
      .catch((scanError) => {
        clearInterval(intervalId);
        console.error(scanError);
        setStatus("SCAN FAILED");
        setScanning(false);
        setError(scanError.message);
        addLine(`[!] ${scanError.message}`);
      });
  }


  function clearScan() {

    setTarget("");

    setStatus("READY");

    setReport(null);

    setError("");

    setScanning(false);

    setScanLines([
      "[+] Web Security engine ready.",
      "[+] Waiting for target input..."
    ]);

  }

  async function runExternalScanner(scanner) {
    const cleanTarget = target.trim();
    if (!cleanTarget) {
      setError("Enter a target URL before selecting a scanner.");
      return;
    }
    let normalizedTarget = cleanTarget;
    if (!normalizedTarget.startsWith("http://") && !normalizedTarget.startsWith("https://")) {
      normalizedTarget = "https://" + normalizedTarget;
    }
    setExternalLoading(scanner);
    setExternalScan(null);
    setError("");
    try {
      const response = await fetch(`/api/web-security/scanners/${scanner}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ target: normalizedTarget, authorized: true })
      });
      const data = await response.json();
      if (!response.ok || !data.success) throw new Error(data.error || `${scanner} did not complete.`);
      setExternalScan(data.result);
    } catch (scanError) {
      setError(scanError.message);
    } finally {
      setExternalLoading("");
    }
  }


  const summary = report?.report_summary || {

    total: 0,
    critical: 0,
    high: 0,
    medium: 0,
    low: 0,
    info: 0

  };


  const recon = report?.recon || {};

  const tls = report?.tls || {};

  const authentication = report?.authentication || {};

  const securityContact = report?.security_contact || {};


  const allFindings = [

    ...(report?.security_headers || []).map((item) => ({
      severity: item.severity,
      title: item.header || "Security Header",
      description: item.description || "Security header requires review.",
      category: item.category || "Security Headers",
      icon: ShieldCheck
    })),

    ...(report?.sql_injection || []).map((item) => ({
      severity: item.severity || "High",
      title: item.title || item.description || "SQL Injection Indicator",
      description: item.description || "SQL injection indicator detected.",
      category: "SQL Injection",
      icon: Database
    })),

    ...(report?.xss || []).map((item) => ({
      severity: item.severity || "Medium",
      title: item.title || item.description || "XSS Indicator",
      description: item.description || "Possible XSS reflection detected.",
      category: "Cross-Site Scripting",
      icon: Code2
    })),

    ...(report?.misconfiguration || []).map((item) => ({
      severity: item.severity || "High",
      title: item.title || item.name || "Misconfiguration",
      description:
        item.description ||
        "A possible security misconfiguration was detected.",
      category: "Misconfiguration",
      icon: AlertTriangle
    })),

    ...(report?.directory_listing || []).map((item) => ({
      severity: item.severity || "Medium",
      title: item.title || "Directory Listing",
      description:
        item.description ||
        "Possible directory listing detected.",
      category: "Directory Listing",
      icon: Eye
    }))

  ];


  report?.ports
    ?.filter((port) =>
      [21, 23, 445, 3389].includes(port.port)
    )
    .forEach((port) => {

      allFindings.push({

        severity: "Medium",

        title: `Risky port ${port.port} open`,

        description:
          `${port.service || "Unknown service"} is exposed on TCP port ${port.port}.`,

        category: "Network Exposure",

        icon: Network

      });

    });


  report?.cookies
    ?.filter((cookie) =>
      !cookie.secure ||
      !cookie.httponly ||
      !cookie.samesite
    )
    .forEach((cookie) => {

      allFindings.push({

        severity: "Low",

        title: `Cookie security review: ${cookie.name}`,

        description:
          `Cookie attributes should be reviewed for Secure, HttpOnly and SameSite protection.`,

        category: "Cookie Security",

        icon: Cookie

      });

    });


  if (
    tls?.tls_version &&
    ["TLSv1.0", "TLSv1.1"].includes(tls.tls_version)
  ) {

    allFindings.push({

      severity: "High",

      title: "Outdated TLS version",

      description:
        `The target is using ${tls.tls_version}.`,

      category: "TLS Security",

      icon: LockKeyhole

    });

  }


  return (

    <section className="web-security-page">


      {/* HEADER */}

      <div className="web-security-header">

        <div>

          <p className="eyebrow">
            NIGHT HUNTER · AUTHORISED WEB AUDIT
          </p>

          <h2>
            Web Security Inspection
          </h2>

          <p className="subtitle">
            Real checks: headers · TLS · cookies · HTTP methods · public endpoints · technology signals · safe reflection indicators
          </p>

        </div>


        <div
          className={`scan-status ${
            scanning
              ? "scanning"
              : status === "SCAN COMPLETE"
                ? "complete"
                : ""
          }`}
        >

          <span></span>

          {status}

        </div>

      </div>


      {/* TARGET */}

      <form
        className="target-panel"
        onSubmit={startScan}
      >

        <div className="target-label">

          <Globe size={16} />

          <span>
            TARGET URL
          </span>

        </div>


        <div className="target-input-row">

          <input
            type="text"
            value={target}
            onChange={(event) =>
              setTarget(event.target.value)
            }
            placeholder="https://example.com"
            disabled={scanning}
          />


          <button
            className="scan-button"
            type="submit"
            disabled={scanning}
          >

            {scanning ? (
              <RefreshCw
                size={16}
                className="spin-icon"
              />
            ) : (
              <Search size={16} />
            )}

            {scanning
              ? "SCANNING..."
              : "START SCAN"
            }

          </button>

        </div>


        <div className="target-hint">
          <label style={{ display: "inline-flex", gap: "8px", alignItems: "center", cursor: "pointer" }}>
            <input
              type="checkbox"
              checked={authorized}
              onChange={(event) => setAuthorized(event.target.checked)}
              disabled={scanning}
            />
            <span>I own this target or have explicit permission to audit it</span>
          </label>

          {target && !scanning && (

            <button
              type="button"
              className="clear-button"
              onClick={clearScan}
            >

              Clear

            </button>

          )}

        </div>

      </form>

      <section style={{ marginTop: "18px", padding: "18px", border: "1px solid rgba(112, 127, 255, 0.2)", borderRadius: "12px", background: "rgba(8, 10, 25, 0.78)" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: "16px", flexWrap: "wrap" }}>
          <div>
            <p className="eyebrow" style={{ margin: 0 }}>ADVANCED SCANNER HUB</p>
            <h3 style={{ margin: "5px 0", color: "#edf0ff" }}>Use installed tools — never simulated results</h3>
            <p style={{ margin: 0, color: "#8e9ab8", fontSize: "12px", lineHeight: 1.5 }}>Nikto and Nuclei run only from your local Windows/Linux/Termux installation. Nessus and Acunetix require your own licensed server and API connector.</p>
          </div>
          <span className="scan-status"><span />{scannerHub?.runtime === "cloud" ? "CLOUD: LOCAL TOOLS OFF" : "LOCAL TOOL CHECK"}</span>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(210px, 1fr))", gap: "10px", marginTop: "16px" }}>
          {["night_hunter", "nikto", "nuclei", "openvas"].map((id) => {
            const item = scannerHub?.scanners?.[id];
            const launchable = id === "nikto" || id === "nuclei" || id === "openvas";
            return <article key={id} style={{ padding: "13px", borderRadius: "9px", border: "1px solid rgba(255,255,255,0.09)", background: "rgba(0,0,0,0.22)" }}>
              <strong style={{ color: "#e9edff", display: "block", fontSize: "13px" }}>{item?.name || id}</strong>
              <small style={{ color: item?.available ? "#7ff0ca" : "#94a3b8", display: "block", margin: "5px 0" }}>{item?.available ? "AVAILABLE ON THIS DEVICE" : item?.kind === "licensed-connector" ? "LICENSED CONNECTOR REQUIRED" : "NOT INSTALLED / CLOUD MODE"}</small>
              <p style={{ color: "#9da7c5", fontSize: "11px", lineHeight: 1.45, minHeight: "32px", margin: "5px 0 10px" }}>{item?.description || "Checking scanner availability…"}</p>
              {launchable ? <button type="button" className="clear-button" disabled={!item?.available || Boolean(externalLoading)} onClick={() => runExternalScanner(id)}>
                {externalLoading === id ? "RUNNING…" : `RUN ${id.toUpperCase()}`}
              </button> : <small style={{ color: "#6f7894", fontSize: "10px" }}>{item?.setup || (id === "night_hunter" ? "Use Start Scan above." : "Connector setup is intentionally separate.")}</small>}
            </article>;
          })}
        </div>

        {externalScan && <div style={{ marginTop: "14px", padding: "13px", borderRadius: "8px", background: "rgba(5, 8, 20, 0.8)", border: "1px solid rgba(118, 229, 188, 0.25)" }}>
          <strong style={{ color: "#7ff0ca", fontSize: "13px" }}>{externalScan.scanner?.toUpperCase()} · {externalScan.summary}</strong>
          {externalScan.findings?.length > 0 && <div style={{ marginTop: "9px", display: "grid", gap: "6px" }}>{externalScan.findings.map((finding, index) => <div key={index} style={{ color: "#d7dcf6", fontSize: "12px" }}><b>{finding.severity?.toUpperCase()}</b> · {finding.name} <span style={{ color: "#8e9ab8" }}>({finding.matched_at})</span></div>)}</div>}
          {!!externalScan.output && <pre style={{ margin: "10px 0 0", maxHeight: "260px", overflow: "auto", whiteSpace: "pre-wrap", color: "#cdd5f5", fontSize: "11px" }}>{externalScan.output}</pre>}
          {!!externalScan.warnings && <pre style={{ margin: "10px 0 0", maxHeight: "120px", overflow: "auto", whiteSpace: "pre-wrap", color: "#f9c7a5", fontSize: "11px" }}>{externalScan.warnings}</pre>}
        </div>}
      </section>


      {/* ERROR */}

      {error && (

        <div className="empty-findings">

          <AlertTriangle size={22} />

          <div>

            <strong>
              Scan failed
            </strong>

            <p>
              {error}
            </p>

          </div>

        </div>

      )}


      {/* STAT CARDS */}

      <div className="web-stats">


        <div className="web-stat-card">

          <div className="web-stat-icon purple">

            <Activity size={19} />

          </div>

          <div>

            <span>
              SCAN STATUS
            </span>

            <strong>
              {status}
            </strong>

          </div>

        </div>


        <div className="web-stat-card">

          <div className="web-stat-icon pink">

            <AlertTriangle size={19} />

          </div>

          <div>

            <span>
              FINDINGS
            </span>

            <strong>
              {summary.total}
            </strong>

          </div>

        </div>


        <div className="web-stat-card">

          <div className="web-stat-icon blue">

            <LockKeyhole size={19} />

          </div>

          <div>

            <span>
              TLS
            </span>

            <strong>
              {tls.tls_version || "—"}
            </strong>

          </div>

        </div>


        <div className="web-stat-card">

          <div className="web-stat-icon green">

            <Server size={19} />

          </div>

          <div>

            <span>
              ENGINE
            </span>

            <strong>
              ONLINE
            </strong>

          </div>

        </div>

      </div>


      {/* RISK SUMMARY */}

      {report && (

        <div className="web-main-grid">


          <div className="scan-overview">

            <div className="web-panel-header">

              <div>

                <span>
                  RISK SUMMARY
                </span>

                <h3>
                  Security Findings
                </h3>

              </div>

              <ShieldCheck size={18} />

            </div>


            <div className="overview-body">

              <div className="overview-item">

                <span>
                  CRITICAL
                </span>

                <strong>
                  {summary.critical}
                </strong>

              </div>


              <div className="overview-item">

                <span>
                  HIGH
                </span>

                <strong>
                  {summary.high}
                </strong>

              </div>


              <div className="overview-item">

                <span>
                  MEDIUM
                </span>

                <strong>
                  {summary.medium}
                </strong>

              </div>


              <div className="overview-item">

                <span>
                  LOW
                </span>

                <strong>
                  {summary.low}
                </strong>

              </div>

            </div>

          </div>


          <div className="scan-overview">

            <div className="web-panel-header">

              <div>

                <span>
                  RECON
                </span>

                <h3>
                  Target Intelligence
                </h3>

              </div>

              <Globe size={18} />

            </div>


            <div className="overview-body">

              <div className="overview-item">

                <span>
                  HOSTNAME
                </span>

                <strong>
                  {recon.hostname || "—"}
                </strong>

              </div>


              <div className="overview-item">

                <span>
                  IP ADDRESS
                </span>

                <strong>
                  {recon.ip_address || "—"}
                </strong>

              </div>


              <div className="overview-item">

                <span>
                  HTTP STATUS
                </span>

                <strong>
                  {recon.status_code || "—"}
                </strong>

              </div>


              <div className="overview-item">

                <span>
                  SERVER
                </span>

                <strong>
                  {recon.server || "—"}
                </strong>

              </div>

            </div>

          </div>

        </div>

      )}


      {/* LIVE TERMINAL */}

      <div className="web-main-grid">


        <div className="web-terminal">

          <div className="web-panel-header">

            <div>

              <span>
                LIVE SCAN
              </span>

              <h3>
                Security Engine
              </h3>

            </div>

            <div className="terminal-indicator">

              <span></span>

              LIVE

            </div>

          </div>


          <div className="web-terminal-body">

            {scanLines.map((line, index) => (

              <p key={`${line}-${index}`}>

                <span className="terminal-prefix">
                  &gt;
                </span>

                {line}

              </p>

            ))}


            {scanning && (

              <p className="terminal-running">

                <span className="terminal-prefix">
                  &gt;
                </span>

                <span className="typing-dots">

                  Processing

                  <i>.</i>

                  <i>.</i>

                  <i>.</i>

                </span>

              </p>

            )}


            <span className="terminal-cursor">
              _
            </span>

          </div>

        </div>


        <div className="scan-overview">

          <div className="web-panel-header">

            <div>

              <span>
                TARGET
              </span>

              <h3>
                Scan Details
              </h3>

            </div>

            <Terminal size={18} />

          </div>


          <div className="overview-body">

            <div className="overview-item">

              <span>
                TARGET
              </span>

              <strong>
                {report?.target || target || "No target"}
              </strong>

            </div>


            <div className="overview-item">

              <span>
                FINAL URL
              </span>

              <strong>
                {recon.final_url || "—"}
              </strong>

            </div>


            <div className="overview-item">

              <span>
                OPEN PORTS
              </span>

              <strong>
                {report?.ports?.length || 0}
              </strong>

            </div>


            <div className="overview-item">

              <span>
                ENDPOINTS
              </span>

              <strong>
                {report?.endpoints?.length || 0}
              </strong>

            </div>

          </div>

        </div>

      </div>


      {/* FINDINGS */}

      <div className="findings-section">

        <div className="findings-heading">

          <div>

            <p className="eyebrow">
              SECURITY RESULTS
            </p>

            <h3>
              Findings
            </h3>

          </div>

          <span>
            {summary.total} detected
          </span>

        </div>


        {allFindings.length === 0 ? (

          <div className="empty-findings">

            <CheckCircle2 size={22} />

            <div>

              <strong>
                No security findings
              </strong>

              <p>
                The current checks did not generate any findings.
              </p>

            </div>

          </div>

        ) : (

          <div className="findings-list">

            {allFindings.map((finding, index) => {

              const FindingIcon =
                finding.icon || AlertTriangle;

              return (

                <div
                  className="finding-card"
                  key={`${finding.title}-${index}`}
                >

                  <div className="finding-icon">

                    <FindingIcon size={19} />

                  </div>


                  <div className="finding-content">

                    <div className="finding-title-row">

                      <strong>
                        {finding.title}
                      </strong>

                      <span
                        className={`severity ${getSeverityClass(
                          finding.severity
                        )}`}
                      >
                        {finding.severity}
                      </span>

                    </div>

                    <p>
                      {finding.description}
                    </p>

                    <small>
                      {finding.category}
                    </small>

                  </div>


                  <ArrowUpRight
                    className="finding-arrow"
                    size={17}
                  />

                </div>

              );

            })}

          </div>

        )}

      </div>


      {/* TECHNICAL DETAILS */}

      {report && (

        <>

          {/* PORTS */}

          <div className="findings-section">

            <div className="findings-heading">

              <div>

                <p className="eyebrow">
                  NETWORK
                </p>

                <h3>
                  Open Ports
                </h3>

              </div>

              <span>
                {report.ports?.length || 0}
              </span>

            </div>


            <div className="findings-list">

              {report.ports?.length ? (

                report.ports.map((port) => (

                  <div
                    className="finding-card"
                    key={`${port.protocol}-${port.port}`}
                  >

                    <div className="finding-icon">

                      <Network size={19} />

                    </div>


                    <div className="finding-content">

                      <div className="finding-title-row">

                        <strong>
                          Port {port.port}
                        </strong>

                        <span className="severity low">
                          {port.state}
                        </span>

                      </div>

                      <p>
                        {port.protocol} · {port.service}
                      </p>

                    </div>

                  </div>

                ))

              ) : (

                <div className="empty-findings">

                  <Network size={22} />

                  <div>

                    <strong>
                      No open ports returned
                    </strong>

                  </div>

                </div>

              )}

            </div>

          </div>


          {/* ENDPOINTS */}

          <div className="findings-section">

            <div className="findings-heading">

              <div>

                <p className="eyebrow">
                  DISCOVERY
                </p>

                <h3>
                  Endpoints
                </h3>

              </div>

              <span>
                {report.endpoints?.length || 0}
              </span>

            </div>


            <div className="findings-list">

              {report.endpoints?.map((endpoint) => (

                <div
                  className="finding-card"
                  key={endpoint.url}
                >

                  <div className="finding-icon">

                    <Route size={19} />

                  </div>


                  <div className="finding-content">

                    <div className="finding-title-row">

                      <strong>
                        /{endpoint.endpoint}
                      </strong>

                      <span className="severity low">
                        HTTP {endpoint.status_code}
                      </span>

                    </div>

                    <p>
                      {endpoint.location
                        ? `Redirect → ${endpoint.location}`
                        : `${endpoint.content_length || 0} bytes`
                      }
                    </p>

                  </div>

                </div>

              ))}

            </div>

          </div>


          {/* TLS */}

          <div className="findings-section">

            <div className="findings-heading">

              <div>

                <p className="eyebrow">
                  ENCRYPTION
                </p>

                <h3>
                  TLS Configuration
                </h3>

              </div>

              <LockKeyhole size={18} />

            </div>


            <div className="findings-list">

              <div className="finding-card">

                <div className="finding-icon">

                  <LockKeyhole size={19} />

                </div>


                <div className="finding-content">

                  <div className="finding-title-row">

                    <strong>
                      {tls.tls_version || "Unknown TLS"}
                    </strong>

                    <span className="severity low">
                      ENCRYPTED
                    </span>

                  </div>

                  <p>
                    Cipher: {tls.cipher || "Unknown"}
                  </p>

                  <small>
                    Certificate expires:{" "}
                    {tls.certificate_expiry || "Unknown"}
                  </small>

                </div>

              </div>

            </div>

          </div>


          {/* TECHNOLOGY */}

          <div className="findings-section">

            <div className="findings-heading">

              <div>

                <p className="eyebrow">
                  FINGERPRINTING
                </p>

                <h3>
                  Technologies
                </h3>

              </div>

              <span>
                {report.technology?.length || 0}
              </span>

            </div>


            <div className="findings-list">

              {report.technology?.map((technology, index) => (

                <div
                  className="finding-card"
                  key={`${technology.name}-${index}`}
                >

                  <div className="finding-icon">

                    <Code2 size={19} />

                  </div>


                  <div className="finding-content">

                    <div className="finding-title-row">

                      <strong>
                        {technology.name}
                      </strong>

                      <span className="severity low">
                        {technology.type}
                      </span>

                    </div>

                    <p>
                      Detected from {technology.source}.
                    </p>

                  </div>

                </div>

              ))}

            </div>

          </div>


          {/* COOKIES */}

          <div className="findings-section">

            <div className="findings-heading">

              <div>

                <p className="eyebrow">
                  SESSION
                </p>

                <h3>
                  Cookies
                </h3>

              </div>

              <span>
                {report.cookies?.length || 0}
              </span>

            </div>


            <div className="findings-list">

              {report.cookies?.map((cookie) => (

                <div
                  className="finding-card"
                  key={cookie.name}
                >

                  <div className="finding-icon">

                    <Cookie size={19} />

                  </div>


                  <div className="finding-content">

                    <div className="finding-title-row">

                      <strong>
                        {cookie.name}
                      </strong>

                    </div>

                    <p>

                      Secure:{" "}
                      {cookie.secure ? "Yes" : "No"}

                      {" · "}

                      HttpOnly:{" "}
                      {cookie.httponly ? "Yes" : "No"}

                      {" · "}

                      SameSite:{" "}
                      {cookie.samesite || "Not set"}

                    </p>

                  </div>

                </div>

              ))}

            </div>

          </div>


          {/* HTTP METHODS */}

          <div className="findings-section">

            <div className="findings-heading">

              <div>

                <p className="eyebrow">
                  HTTP
                </p>

                <h3>
                  HTTP Methods
                </h3>

              </div>

              <span>
                {report.http_methods?.length || 0}
              </span>

            </div>


            <div className="findings-list">

              {report.http_methods?.map((method) => (

                <div
                  className="finding-card"
                  key={method.method}
                >

                  <div className="finding-icon">

                    {method.allowed ? (
                      <CheckCircle2 size={19} />
                    ) : (
                      <XCircle size={19} />
                    )}

                  </div>


                  <div className="finding-content">

                    <div className="finding-title-row">

                      <strong>
                        {method.method}
                      </strong>

                      <span
                        className={`severity ${
                          method.allowed
                            ? "low"
                            : "medium"
                        }`}
                      >
                        HTTP {method.status_code}
                      </span>

                    </div>

                    <p>
                      {method.allowed
                        ? "Method accepted by the target."
                        : "Method was rejected by the target."
                      }
                    </p>

                  </div>

                </div>

              ))}

            </div>

          </div>


          {/* AUTHENTICATION */}

          <div className="findings-section">

            <div className="findings-heading">

              <div>

                <p className="eyebrow">
                  AUTHENTICATION
                </p>

                <h3>
                  Authentication Indicators
                </h3>

              </div>

              <KeyRound size={18} />

            </div>


            <div className="findings-list">

              <div className="finding-card">

                <div className="finding-icon">

                  <KeyRound size={19} />

                </div>


                <div className="finding-content">

                  <div className="finding-title-row">

                    <strong>
                      HTTPS
                    </strong>

                    <span className="severity low">

                      {authentication.https
                        ? "ENABLED"
                        : "NOT DETECTED"
                      }

                    </span>

                  </div>

                  <p>

                    Cache-Control:{" "}
                    {authentication.cache_control
                      ? "Present"
                      : "Not detected"
                    }

                  </p>

                </div>

              </div>

            </div>

          </div>


          {/* SECURITY CONTACT */}

          <div className="findings-section">

            <div className="findings-heading">

              <div>

                <p className="eyebrow">
                  RESPONSIBLE DISCLOSURE
                </p>

                <h3>
                  Security Contact
                </h3>

              </div>

              <ShieldCheck size={18} />

            </div>


            <div className="finding-card">

              <div className="finding-icon">

                {securityContact.security_txt ? (
                  <CheckCircle2 size={19} />
                ) : (
                  <FileWarning size={19} />
                )}

              </div>


              <div className="finding-content">

                <div className="finding-title-row">

                  <strong>
                    security.txt
                  </strong>

                  <span
                    className={`severity ${
                      securityContact.security_txt
                        ? "low"
                        : "medium"
                    }`}
                  >

                    {securityContact.security_txt
                      ? "FOUND"
                      : "NOT FOUND"
                    }

                  </span>

                </div>

                <p>
                  {securityContact.url}
                </p>

              </div>

            </div>

          </div>


          {/* API */}

          <div className="findings-section">

            <div className="findings-heading">

              <div>

                <p className="eyebrow">
                  API DISCOVERY
                </p>

                <h3>
                  API Endpoints
                </h3>

              </div>

              <span>
                {report.api?.length || 0}
              </span>

            </div>


            <div className="findings-list">

              {report.api?.map((apiEndpoint) => (

                <div
                  className="finding-card"
                  key={apiEndpoint.url}
                >

                  <div className="finding-icon">

                    <Code2 size={19} />

                  </div>


                  <div className="finding-content">

                    <div className="finding-title-row">

                      <strong>
                        {apiEndpoint.path}
                      </strong>

                      <span className="severity low">
                        HTTP {apiEndpoint.status_code}
                      </span>

                    </div>

                    <p>
                      {apiEndpoint.content_type}
                    </p>

                  </div>

                </div>

              ))}

            </div>

          </div>


        </>

      )}


    </section>

  );

}


export default WebSecurity;
