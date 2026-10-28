import React from "react";
import { ShieldAlert, Scale, AlertOctagon, CheckSquare, BookOpen, ArrowLeft, Gavel } from "lucide-react";

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
          Terms and Conditions & Legal Disclaimer
        </h1>
        <p style={{ color: "#94a3b8", fontSize: "14px", margin: 0 }}>
          Effective Date: October 2026 | Night Hunter Defensive Security Platform
        </p>
      </div>

      <div style={{ display: "grid", gap: "32px" }}>
        <section>
          <h2 style={{ fontSize: "20px", fontWeight: "600", color: "#f8fafc", marginBottom: "12px", display: "flex", alignItems: "center", gap: "10px" }}>
            <CheckSquare size={20} color="#0ea5e9" /> 1. Acceptance of Terms
          </h2>
          <p style={{ color: "#cbd5e1", fontSize: "14px" }}>
            By downloading, installing, accessing, or running the Night Hunter software, executable files, or hosted cloud interface, you acknowledge that you have read, understood, and agreed to be legally bound by these Terms and Conditions.
          </p>
        </section>

        <section>
          <h2 style={{ fontSize: "20px", fontWeight: "600", color: "#f8fafc", marginBottom: "12px", display: "flex", alignItems: "center", gap: "10px" }}>
            <Gavel size={20} color="#ef4444" /> 2. Complete User Liability & Statutory Compliance (IT Act & International Law)
          </h2>
          <div style={{
            background: "rgba(239, 68, 68, 0.08)",
            border: "1px solid rgba(239, 68, 68, 0.3)",
            borderRadius: "6px",
            padding: "16px 20px",
            marginBottom: "16px"
          }}>
            <p style={{ color: "#fca5a5", fontSize: "14px", fontWeight: "600", margin: "0 0 8px 0" }}>
              IMPORTANT STATUTORY WARNING FOR OPERATORS & USERS:
            </p>
            <p style={{ color: "#cbd5e1", fontSize: "13px", margin: 0, lineHeight: "1.6" }}>
              The developer, author, and maintainers of Night Hunter are <strong>NOT LIABLE</strong> for any misuse, unauthorized scanning, network disruption, or illegal activity conducted by third parties or end users. The operator who initiates any scan assumes <strong>100% EXCLUSIVE LEGAL, CIVIL, AND CRIMINAL RESPONSIBILITY</strong> under all applicable domestic and international laws.
            </p>
          </div>
          <ul style={{ color: "#cbd5e1", fontSize: "14px", paddingLeft: "24px", lineHeight: "1.8" }}>
            <li>
              <strong>Information Technology Act, 2000 (India):</strong> Any unauthorized scanning, port intrusion, denial of service, or unauthorized access into any computer system, network, or data without express written permission constitutes a cognizable criminal offense punishable under <strong>Section 43 (penalty for damage to computer systems)</strong> and <strong>Section 66 / 66C / 66D (computer related offences, hacking, and identity theft)</strong> of the Indian Information Technology Act, 2000 and the Indian Penal Code (IPC / BNS).
            </li>
            <li>
              <strong>Computer Fraud and Abuse Act (CFAA - United States):</strong> Unauthorized scanning or access to protected computers is strictly prohibited under 18 U.S.C. § 1030.
            </li>
            <li>
              <strong>International Law & Cybercrime Treaties:</strong> The user warrants that their actions comply with the Budapest Convention on Cybercrime and all local statutes in their jurisdiction.
            </li>
            <li>
              <strong>Sole Operator Culpability:</strong> If any target, domain, IP owner, ISP, or law enforcement agency initiates legal, civil, or penal action regarding a scan, <strong>the user who executed the scan shall be the sole accused party</strong>. The developers bear zero culpability or co-liability.
            </li>
          </ul>
        </section>

        <section>
          <h2 style={{ fontSize: "20px", fontWeight: "600", color: "#f8fafc", marginBottom: "12px", display: "flex", alignItems: "center", gap: "10px" }}>
            <ShieldAlert size={20} color="#0ea5e9" /> 3. Authorized Testing & Lawful Defensive Purpose
          </h2>
          <p style={{ color: "#cbd5e1", fontSize: "14px" }}>
            Night Hunter is provided exclusively for authorized cybersecurity auditing, system diagnostics, educational research, and defensive threat analysis.
          </p>
          <ul style={{ color: "#94a3b8", fontSize: "14px", paddingLeft: "24px" }}>
            <li>You may only scan, probe, or analyze targets, domains, networks, and hosts that you legally own or for which you have received express, written, verifiable authorization from the owner.</li>
            <li>You must not use this software for unauthorized network intrusion, service denial, exploitation, credential harvesting, or harassment.</li>
            <li>Passive phishing links and scam text analysis must be used for defensive awareness, threat verification, and educational demonstrations only.</li>
          </ul>
        </section>

        <section>
          <h2 style={{ fontSize: "20px", fontWeight: "600", color: "#f8fafc", marginBottom: "12px", display: "flex", alignItems: "center", gap: "10px" }}>
            <BookOpen size={20} color="#0ea5e9" /> 4. Open Source License (MIT)
          </h2>
          <p style={{ color: "#cbd5e1", fontSize: "14px" }}>
            The source code of Night Hunter is licensed under the MIT License. You are permitted to inspect, modify, and distribute the code, provided that the original copyright notice and disclaimer remain intact.
          </p>
        </section>

        <section>
          <h2 style={{ fontSize: "20px", fontWeight: "600", color: "#f8fafc", marginBottom: "12px", display: "flex", alignItems: "center", gap: "10px" }}>
            <AlertOctagon size={20} color="#0ea5e9" /> 5. Disclaimer of Warranties
          </h2>
          <p style={{ color: "#cbd5e1", fontSize: "14px" }}>
            THE SOFTWARE IS PROVIDED &quot;AS IS&quot;, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY ARISING FROM THE USE OF THE SOFTWARE.
          </p>
        </section>

        <section>
          <h2 style={{ fontSize: "20px", fontWeight: "600", color: "#f8fafc", marginBottom: "12px", display: "flex", alignItems: "center", gap: "10px" }}>
            <Scale size={20} color="#0ea5e9" /> 6. Complete Developer Indemnification & Hold Harmless
          </h2>
          <p style={{ color: "#cbd5e1", fontSize: "14px" }}>
            By running or downloading this software, the user agrees to indemnify, defend, and hold harmless the developer, contributors, educational institutions, and hosting service providers against any and all claims, lawsuits, damages, fines, legal defense fees, or investigations arising from or relating to the user&apos;s operation or misuse of the tool.
          </p>
        </section>
      </div>
    </div>
  );
}
