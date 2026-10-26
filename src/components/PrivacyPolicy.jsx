import React from "react";
import { Shield, Lock, EyeOff, Server, HardDrive, FileCheck, ArrowLeft } from "lucide-react";

export default function PrivacyPolicy({ onBack }) {
  return (
    <div style={{
      maxWidth: "960px",
      margin: "0 auto",
      padding: "40px 24px 80px",
      color: "#e2e8f0",
      fontFamily: "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
      lineHeight: "1.7"
    }}>
      {onBack && (
        <button
          onClick={onBack}
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: "8px",
            background: "#1e293b",
            border: "1px solid #334155",
            color: "#f8fafc",
            padding: "8px 16px",
            borderRadius: "4px",
            fontSize: "13px",
            fontWeight: "600",
            cursor: "pointer",
            marginBottom: "32px"
          }}
        >
          <ArrowLeft size={16} /> Back to Dashboard
        </button>
      )}

      <div style={{ borderBottom: "1px solid #334155", paddingBottom: "24px", marginBottom: "36px" }}>
        <p style={{
          color: "#0ea5e9",
          fontSize: "11px",
          fontWeight: "700",
          letterSpacing: "0.15em",
          textTransform: "uppercase",
          margin: "0 0 8px 0"
        }}>
          LEGAL & COMPLIANCE
        </p>
        <h1 style={{ fontSize: "32px", fontWeight: "700", color: "#ffffff", margin: "0 0 12px 0" }}>
          Privacy Policy
        </h1>
        <p style={{ color: "#94a3b8", fontSize: "14px", margin: 0 }}>
          Effective Date: October 26, 2026 | Night Hunter Security Platform
        </p>
      </div>

      <div style={{ display: "grid", gap: "32px" }}>
        <section>
          <h2 style={{ fontSize: "20px", fontWeight: "600", color: "#f8fafc", marginBottom: "12px", display: "flex", alignItems: "center", gap: "10px" }}>
            <Server size={20} color="#0ea5e9" /> 1. Architecture & Local Execution Principle
          </h2>
          <p style={{ color: "#cbd5e1", fontSize: "14px" }}>
            Night Hunter is architected as an open-source, defensive cybersecurity workbench. By default, the software executes directly on your host operating system or isolated container. It does not harvest, collect, or transmit telemetry, user metrics, or background tracking to third-party endpoints.
          </p>
        </section>

        <section>
          <h2 style={{ fontSize: "20px", fontWeight: "600", color: "#f8fafc", marginBottom: "12px", display: "flex", alignItems: "center", gap: "10px" }}>
            <EyeOff size={20} color="#0ea5e9" /> 2. Data You Inspect & Analyze
          </h2>
          <p style={{ color: "#cbd5e1", fontSize: "14px" }}>
            When analyzing domains, hosts, IP addresses, credentials, or text samples:
          </p>
          <ul style={{ color: "#94a3b8", fontSize: "14px", paddingLeft: "24px" }}>
            <li><strong>Target Inputs:</strong> Target URLs, domain names, and IP addresses are queried directly from your runtime environment against public network protocols (DNS, HTTP/S, SSL/TLS).</li>
            <li><strong>Password Checks:</strong> Passwords tested in the Password Security module are evaluated using local heuristic algorithms in-memory. They are never transmitted over the internet or written to disk.</li>
            <li><strong>Cryptographic Digests:</strong> Plaintext input into the Cryptography Lab is transformed locally using standard hash functions. Source text is never stored in persistent audit logs.</li>
            <li><strong>Phishing Triage:</strong> Email and message text submitted for triage is parsed locally for lexical anomalies, link patterns, and brand impersonation.</li>
          </ul>
        </section>

        <section>
          <h2 style={{ fontSize: "20px", fontWeight: "600", color: "#f8fafc", marginBottom: "12px", display: "flex", alignItems: "center", gap: "10px" }}>
            <HardDrive size={20} color="#0ea5e9" /> 3. Local Audit Trail & History
          </h2>
          <p style={{ color: "#cbd5e1", fontSize: "14px" }}>
            Completed scan summaries are recorded in a local SQLite / JSON log file on your device to power the Activity History view. This data remains exclusively on your machine and can be cleared at any time via the Reports or Settings tab.
          </p>
        </section>

        <section>
          <h2 style={{ fontSize: "20px", fontWeight: "600", color: "#f8fafc", marginBottom: "12px", display: "flex", alignItems: "center", gap: "10px" }}>
            <Lock size={20} color="#0ea5e9" /> 4. Cloud Deployment (Render / Docker)
          </h2>
          <p style={{ color: "#cbd5e1", fontSize: "14px" }}>
            When running Night Hunter as a cloud service on hosting providers such as Render:
          </p>
          <ul style={{ color: "#94a3b8", fontSize: "14px", paddingLeft: "24px" }}>
            <li>HTTP requests pass through standard reverse-proxy logs provided by the cloud infrastructure (IP, timestamp, user agent).</li>
            <li>No persistent database or cross-user profile tracking is maintained by Night Hunter.</li>
            <li>Connections are encrypted in transit via standard TLS / HTTPS certificates.</li>
          </ul>
        </section>

        <section>
          <h2 style={{ fontSize: "20px", fontWeight: "600", color: "#f8fafc", marginBottom: "12px", display: "flex", alignItems: "center", gap: "10px" }}>
            <FileCheck size={20} color="#0ea5e9" /> 5. Changes & Contact
          </h2>
          <p style={{ color: "#cbd5e1", fontSize: "14px" }}>
            Any modifications to this privacy policy will be documented directly in the public GitHub repository at <code>https://github.com/ArnabHalder-CS/Night-Hunter</code>.
          </p>
        </section>
      </div>
    </div>
  );
}
