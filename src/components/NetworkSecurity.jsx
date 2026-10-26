import { useState } from "react";

import {
  Network,
  Search,
  Activity,
  Server,
  Radio,
  ShieldCheck,
  Globe,
  Clock3,
  AlertTriangle,
  CheckCircle2,
  XCircle,
  RefreshCw,
  Wifi,
  Router,
  Terminal,
} from "lucide-react";


function NetworkSecurity() {

  const [target, setTarget] = useState("");

  const [status, setStatus] = useState("READY");

  const [scanning, setScanning] = useState(false);

  const [result, setResult] = useState(null);

  const [error, setError] = useState("");


  // =========================================================
  // REAL NETWORK SECURITY API
  // =========================================================

  async function runNetworkCheck(event) {

    event.preventDefault();

    const cleanTarget = target.trim();


    if (!cleanTarget) {

      setStatus("TARGET REQUIRED");

      setError("Enter a hostname or IP address.");

      setResult(null);

      return;
    }


    setScanning(true);

    setStatus("SCANNING");

    setError("");

    setResult(null);


    try {

      const response = await fetch(
        "/api/network-security",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            target: cleanTarget,
          }),
        }
      );


      const data = await response.json();


      if (!response.ok || !data.success) {

        throw new Error(
          data.error || "Network security check failed."
        );

      }


      setResult(data.result);

      setStatus("COMPLETED");


    } catch (requestError) {

      console.error(
        "Network Security API error:",
        requestError
      );

      setError(
        requestError.message ||
        "Unable to connect to NIGHT HUNTER API."
      );

      setStatus("API ERROR");

      setResult(null);


    } finally {

      setScanning(false);

    }

  }


  // =========================================================
  // CLEAR
  // =========================================================

  function clearResult() {

    setTarget("");

    setResult(null);

    setError("");

    setStatus("READY");

    setScanning(false);

  }


  // =========================================================
  // RESULT VALUES
  // =========================================================

  const resolution =
    result?.resolution || {};

  const hostCheck =
    result?.host_check || {};

  const openPorts =
    Array.isArray(result?.open_ports)
      ? result.open_ports
      : [];

  const openServices =
    Array.isArray(result?.open_services)
      ? result.open_services
      : [];

  const addresses =
    Array.isArray(resolution.addresses)
      ? resolution.addresses
      : [];


  return (

    <section className="network-security-page">


      {/* =====================================================
          HEADER
      ===================================================== */}

      <div className="network-command-header">

        <div className="network-title-area">

          <div className="network-main-icon">

            <Network size={25} />

          </div>


          <div>

            <p className="eyebrow">
              NIGHT HUNTER · NETWORK SECURITY
            </p>

            <h2>
              Network Speed & Health Monitor
            </h2>

            <p className="subtitle">
              Discover · Inspect · Monitor
            </p>

          </div>

        </div>


        <div
          className={`network-status ${
            scanning
              ? "scanning"
              : status === "READY"
                ? ""
                : "active"
          }`}
        >

          <span></span>

          {status}

        </div>

      </div>


      {/* =====================================================
          TARGET WORKSPACE
      ===================================================== */}

      <div className="network-target-workspace">


        <div className="network-target-header">

          <div>

            <span>
              TARGET / HOST
            </span>

            <h3>
              Network Speed & Connectivity Check
            </h3>

          </div>

          <Terminal size={19} />

        </div>


        <form
          className="network-target-form"
          onSubmit={runNetworkCheck}
        >

          <div className="network-target-input">

            <Globe size={18} />

            <input
              type="text"
              value={target}
              onChange={(event) =>
                setTarget(event.target.value)
              }
              placeholder="Enter hostname or IP address"
              disabled={scanning}
            />

          </div>


          <button
            type="submit"
            className="network-scan-button"
            disabled={scanning}
          >

            {scanning ? (

              <RefreshCw
                size={17}
                className="network-spin"
              />

            ) : (

              <Search size={17} />

            )}

            {scanning
              ? "SCANNING..."
              : "SCAN NETWORK"
            }

          </button>


          {target && !scanning && (

            <button
              type="button"
              className="network-clear-button"
              onClick={clearResult}
            >
              Clear
            </button>

          )}

        </form>


        {error && (

          <div className="network-error">

            <AlertTriangle size={17} />

            <span>
              {error}
            </span>

          </div>

        )}


        <div className="network-target-note">

          <ShieldCheck size={15} />

          <span>
            Use only on systems and networks you own or are authorized to test.
          </span>

        </div>

      </div>


      {/* =====================================================
          NETWORK STATUS CARDS
      ===================================================== */}

      <div className="network-metrics">


        <div className="network-metric-card">

          <div className="network-metric-icon blue">

            <Server size={19} />

          </div>


          <div>

            <span>
              HOST STATUS
            </span>

            <strong>

              {result
                ? hostCheck.reachable
                  ? "REACHABLE"
                  : "UNREACHABLE"
                : "—"}

            </strong>

          </div>

        </div>


        <div className="network-metric-card">

          <div className="network-metric-icon violet">

            <Radio size={19} />

          </div>


          <div>

            <span>
              OPEN PORTS
            </span>

            <strong>
              {result
                ? result.total_open_ports
                : "—"}
            </strong>

          </div>

        </div>


        <div className="network-metric-card">

          <div className="network-metric-icon pink">

            <Network size={19} />

          </div>


          <div>

            <span>
              ADDRESSES
            </span>

            <strong>
              {result
                ? addresses.length
                : "—"}
            </strong>

          </div>

        </div>


        <div className="network-metric-card">

          <div className="network-metric-icon green">

            <Activity size={19} />

          </div>


          <div>

            <span>
              SERVICES
            </span>

            <strong>
              {result
                ? openServices.length
                : "—"}
            </strong>

          </div>

        </div>


      </div>


      {/* =====================================================
          NETWORK TOPOLOGY
      ===================================================== */}

      <div className="network-topology-panel">


        <div className="network-panel-header">

          <div>

            <span>
              NETWORK ACTIVITY
            </span>

            <h3>
              Connection Overview
            </h3>

          </div>

          <Wifi size={19} />

        </div>


        <div className="network-topology">


          <div className="network-node">

            <div className="network-node-icon">

              <Server size={22} />

            </div>

            <strong>
              LOCAL
            </strong>

            <span>
              NIGHT HUNTER
            </span>

          </div>


          <div className="network-connection">

            <span></span>

          </div>


          <div className="network-node">

            <div className="network-node-icon">

              <Router size={22} />

            </div>

            <strong>
              NETWORK
            </strong>

            <span>
              CONNECTION
            </span>

          </div>


          <div className="network-connection">

            <span></span>

          </div>


          <div className="network-node">

            <div className="network-node-icon">

              <Globe size={22} />

            </div>

            <strong>
              TARGET
            </strong>

            <span>
              {result?.target || "WAITING"}
            </span>

          </div>


        </div>

      </div>


      {/* =====================================================
          RESOLUTION + PORTS
      ===================================================== */}

      <div className="network-analysis-grid">


        {/* HOST INFORMATION */}

        <div className="network-analysis-panel">


          <div className="network-panel-header">

            <div>

              <span>
                HOST INFORMATION
              </span>

              <h3>
                Resolution
              </h3>

            </div>

            <Globe size={18} />

          </div>


          {!result ? (

            <div className="network-empty-state">

              <Globe size={25} />

              <strong>
                Awaiting Network Scan
              </strong>

              <p>
                Enter a host or IP address to begin.
              </p>

            </div>

          ) : (

            <div className="network-info-list">


              <div className="network-info-row">

                <div>

                  <strong>
                    Target
                  </strong>

                  <span>
                    Requested host
                  </span>

                </div>

                <b>
                  {result.target || "—"}
                </b>

              </div>


              <div className="network-info-row">

                <div>

                  <strong>
                    Resolution
                  </strong>

                  <span>
                    DNS / host resolution
                  </span>

                </div>

                {resolution.resolved ? (

                  <div className="network-success">

                    <CheckCircle2 size={17} />

                    Resolved

                  </div>

                ) : (

                  <div className="network-danger">

                    <XCircle size={17} />

                    Failed

                  </div>

                )}

              </div>


              <div className="network-info-row">

                <div>

                  <strong>
                    Addresses
                  </strong>

                  <span>
                    Resolved IP addresses
                  </span>

                </div>

                <b>
                  {addresses.length}
                </b>

              </div>


                            {result?.speed_test && (
                <div style={{ marginTop: '15px', padding: '12px', background: 'rgba(56, 189, 248, 0.08)', borderRadius: '6px', border: '1px solid rgba(56, 189, 248, 0.2)' }}>
                  <div style={{ fontSize: '11px', color: '#38bdf8', fontWeight: 'bold', textTransform: 'uppercase', marginBottom: '8px' }}>
                    Speed & Latency Telemetry
                  </div>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', fontSize: '13px' }}>
                    <div>Throughput: <b style={{ color: '#4ade80' }}>{result.speed_test.speed_label}</b></div>
                    <div>Latency (RTT): <b style={{ color: '#facc15' }}>{hostCheck.response_time_ms} ms</b></div>
                    <div>Jitter / Delta: <b>{hostCheck.jitter_ms} ms</b></div>
                    <div>Packet Loss: <b style={{ color: hostCheck.reachable ? '#4ade80' : '#f87171' }}>{hostCheck.packet_loss}</b></div>
                  </div>
                </div>
              )}
<div className="network-address-list">

                {addresses.length > 0 ? (

                  addresses.map(
                    (address, index) => (

                      <div
                        key={`${address}-${index}`}
                        className="network-address"
                      >

                        <Radio size={14} />

                        {address}

                      </div>

                    )
                  )

                ) : (

                  <span className="network-muted">
                    No addresses returned.
                  </span>

                )}

              </div>


            </div>

          )}

        </div>


        {/* OPEN PORTS */}

        <div className="network-analysis-panel">


          <div className="network-panel-header">

            <div>

              <span>
                BASIC SERVICES
              </span>

              <h3>
                Standard Services (HTTP/DNS)
              </h3>

            </div>

            <Activity size={18} />

          </div>


          {!result ? (

            <div className="network-empty-state">

              <Activity size={25} />

              <strong>
                No Scan Results
              </strong>

              <p>
                Common TCP ports will appear here.
              </p>

            </div>

          ) : openPorts.length === 0 ? (

            <div className="network-empty-state">

              <CheckCircle2 size={25} />

              <strong>
                No Open Common Ports
              </strong>

              <p>
                No open ports were found in the common-port scan.
              </p>

            </div>

          ) : (

            <div className="network-port-list">

              {openPorts.map(
                (port, index) => (

                  <div
                    key={`${port.port}-${index}`}
                    className="network-port-row"
                  >

                    <div className="network-port-number">

                      {port.port}

                    </div>


                    <div className="network-port-service">

                      <strong>
                        {port.service}
                      </strong>

                      <span>
                        TCP
                      </span>

                    </div>


                    <div className="network-port-response">

                      <Clock3 size={14} />

                      {port.response_time !== null
                        ? `${port.response_time} ms`
                        : "—"}

                    </div>


                    <div className="network-open-badge">

                      <span></span>

                      OPEN

                    </div>

                  </div>

                )
              )}

            </div>

          )}

        </div>


      </div>


      {/* =====================================================
          SERVICE SUMMARY
      ===================================================== */}

      <div className="network-services-panel">


        <div className="network-panel-header">

          <div>

            <span>
              SERVICE IDENTIFICATION
            </span>

            <h3>
              Detected Services
            </h3>

          </div>

          <Server size={18} />

        </div>


        {!result ? (

          <div className="network-services-empty">

            <Server size={22} />

            <span>
              Service information will appear after scanning.
            </span>

          </div>

        ) : openServices.length === 0 ? (

          <div className="network-services-empty">

            <CheckCircle2 size={22} />

            <span>
              No responding common services detected.
            </span>

          </div>

        ) : (

          <div className="network-service-grid">

            {openServices.map(
              (service, index) => (

                <div
                  key={`${service.port}-${index}`}
                  className="network-service-card"
                >

                  <div className="network-service-top">

                    <div className="network-service-port">

                      {service.port}

                    </div>

                    <span className="network-service-open">
                      OPEN
                    </span>

                  </div>


                  <strong>
                    {service.service}
                  </strong>


                  <span>

                    Response:

                    {" "}

                    {service.response_time !== null
                      ? `${service.response_time} ms`
                      : "—"}

                  </span>

                </div>

              )
            )}

          </div>

        )}

      </div>


      {/* =====================================================
          FOOTER
      ===================================================== */}

      <div className="network-footer">

        <div>

          <ShieldCheck size={16} />

          <span>
            NIGHT HUNTER NETWORK SECURITY
          </span>

        </div>


        <span>
          Defensive network inspection
        </span>

      </div>


    </section>

  );

}


export default NetworkSecurity;
