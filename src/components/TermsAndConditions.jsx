import React from "react";
import { ShieldAlert, Scale, AlertOctagon, CheckSquare, BookOpen, ArrowLeft } from "lucide-react";

export default function TermsAndConditions({ onBack }) {
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
          Terms and Conditions
        </h1>
        <p style={{ color: "#94a3b8", fontSize: "14px", margin: 0 }}>
          Effective Date: October 26, 2026 | Night Hunter Security Platform
        </p>
      </div>

      <div style={{ display: "grid", gap: "32px" }}>
        <section>
          <h2 style={{ fontSize: "20px", fontWeight: "600", color: "#f8fafc", marginBottom: "12px", display: "flex", alignItems: "center", gap: "10px" }}>
            <CheckSquare size={20} color="#0ea5e9" /> 1. Acceptance of Terms
          </h2>
          <p style={{ color: "#cbd5e1", fontSize: "14px" }}>
            By downloading, installing, accessing, or running the Night Hunter software or hosted cloud interface, you acknowledge that you have read, understood, and agreed to be bound by these Terms and Conditions.
          </p>
        </section>

        <section>
          <h2 style={{ fontSize: "20px", fontWeight: "600", color: "#f8fafc", marginBottom: "12px", display: "flex", alignItems: "center", gap: "10px" }}>
            <ShieldAlert size={20} color="#0ea5e9" /> 2. Authorized Testing & Lawful Purpose
          </h2>
          <p style={{ color: "#cbd5e1", fontSize: "14px" }}>
            Night Hunter is provided exclusively for authorized cybersecurity auditing, system diagnostics, educational research, and defensive threat analysis.
          </p>
          <ul style={{ color: "#94a3b8", fontSize: "14px", paddingLeft: "24px" }}>
            <li>You may only scan, probe, or analyze targets, domains, networks, and hosts that you legally own or for which you have received express, written authorization from the owner.</li>
            <li>You must not use this software for unauthorized network intrusion, service denial, exploitation, credential harvesting, or any action that violates regional or international computer fraud statutes.</li>
            <li>You are solely responsible for ensuring your use complies with all applicable laws, including the Computer Fraud and Abuse Act (CFAA) and relevant national regulations.</li>
          </ul>
        </section>

        <section>
          <h2 style={{ fontSize: "20px", fontWeight: "600", color: "#f8fafc", marginBottom: "12px", display: "flex", alignItems: "center", gap: "10px" }}>
            <BookOpen size={20} color="#0ea5e9" /> 3. Open Source License (MIT)
          </h2>
          <p style={{ color: "#cbd5e1", fontSize: "14px" }}>
            The source code of Night Hunter is licensed under the MIT License. You are permitted to inspect, modify, and distribute the code, provided that the copyright notice and license text remain intact.
          </p>
        </section>

        <section>
          <h2 style={{ fontSize: "20px", fontWeight: "600", color: "#f8fafc", marginBottom: "12px", display: "flex", alignItems: "center", gap: "10px" }}>
            <AlertOctagon size={20} color="#0ea5e9" /> 4. Disclaimer of Warranties
          </h2>
          <p style={{ color: "#cbd5e1", fontSize: "14px" }}>
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY ARISING FROM THE USE OF THE SOFTWARE.
          </p>
        </section>

        <section>
          <h2 style={{ fontSize: "20px", fontWeight: "600", color: "#f8fafc", marginBottom: "12px", display: "flex", alignItems: "center", gap: "10px" }}>
            <Scale size={20} color="#0ea5e9" /> 5. Limitation of Liability
          </h2>
          <p style={{ color: "#cbd5e1", fontSize: "14px" }}>
            Under no circumstances shall the authors, maintainers, or hosting operators be held responsible for network disruptions, data loss, misconfiguration, or legal consequences arising from the operation or misuse of this tool.
          </p>
        </section>
      </div>
    </div>
  );
}
