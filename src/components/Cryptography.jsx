import { useState } from "react";
import {
  Binary,
  Check,
  Copy,
  Fingerprint,
  KeyRound,
  Play,
  RefreshCw,
  ShieldCheck,
  Search,
  Sparkles,
  Lock,
  ArrowRightLeft,
  Key,
  Hash,
  ShieldAlert,
  Code
} from "lucide-react";

function titleForAlgorithm(algorithm) {
  return algorithm.replaceAll("_", "-").toUpperCase();
}

export default function Cryptography() {
  const [activeTab, setActiveTab] = useState("hash"); // "hash" | "identify" | "encode" | "keys" | "hmac"

  // Tab 1: Multi-Hash State
  const [hashText, setHashText] = useState("Night Hunter Security");
  const [hashResults, setHashResults] = useState(null);
  const [hashLoading, setHashLoading] = useState(false);
  const [hashError, setHashError] = useState("");
  const [verifyHash, setVerifyHash] = useState("");

  // Tab 2: Hash Identifier State
  const [unknownHash, setUnknownHash] = useState("5d41402abc4b2a76b9719d911017c592");
  const [analysisResult, setAnalysisResult] = useState(null);
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [analysisError, setAnalysisError] = useState("");

  // Tab 3: Encoders/Decoders State
  const [encodeInput, setEncodeInput] = useState("Hello Night Hunter");
  const [encodeOp, setEncodeOp] = useState("base64_encode");
  const [caesarShift, setCaesarShift] = useState("3");
  const [encodeOutput, setEncodeOutput] = useState("");
  const [encodeLoading, setEncodeLoading] = useState(false);
  const [encodeError, setEncodeError] = useState("");

  // Tab 4: Key Generator State
  const [generatedKeys, setGeneratedKeys] = useState(null);
  const [keysLoading, setKeysLoading] = useState(false);

  // Tab 5: HMAC State
  const [hmacMessage, setHmacMessage] = useState("api_payload_data");
  const [hmacSecret, setHmacSecret] = useState("night_hunter_secret_key");
  const [hmacAlgo, setHmacAlgo] = useState("hmac_sha256");
  const [hmacResult, setHmacResult] = useState("");
  const [hmacLoading, setHmacLoading] = useState(false);

  // Copy state
  const [copiedKey, setCopiedKey] = useState("");

  async function copy(value, label) {
    if (!value) return;
    await navigator.clipboard.writeText(typeof value === "string" ? value : JSON.stringify(value, null, 2));
    setCopiedKey(label);
    window.setTimeout(() => setCopiedKey(""), 1800);
  }

  // --- Run Multi-Hash ---
  async function generateAllHashes(event) {
    if (event) event.preventDefault();
    if (!hashText.trim()) {
      setHashError("Enter text to generate hashes.");
      return;
    }
    setHashLoading(true);
    setHashError("");
    setHashResults(null);
    try {
      const response = await fetch("/api/cryptography", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: hashText, operation: "hash" })
      });
      const data = await response.json();
      if (!response.ok || !data.success) throw new Error(data.error || "Hash generation failed.");
      setHashResults(data.result);
    } catch (err) {
      setHashError(err.message);
    } finally {
      setHashLoading(false);
    }
  }

  // --- Run Hash Identifier ---
  async function runHashIdentifier(event) {
    if (event) event.preventDefault();
    if (!unknownHash.trim()) {
      setAnalysisError("Enter a hash string to identify.");
      return;
    }
    setAnalysisLoading(true);
    setAnalysisError("");
    setAnalysisResult(null);
    try {
      const response = await fetch("/api/cryptography", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: unknownHash.trim(), operation: "identify" })
      });
      const data = await response.json();
      if (!response.ok || !data.success) throw new Error(data.error || "Hash identification failed.");
      setAnalysisResult(data.result);
    } catch (err) {
      setAnalysisError(err.message);
    } finally {
      setAnalysisLoading(false);
    }
  }

  // --- Run Encoder/Decoder ---
  async function runEncoder(event) {
    if (event) event.preventDefault();
    if (!encodeInput.trim()) {
      setEncodeError("Enter text to encode or decode.");
      return;
    }
    setEncodeLoading(true);
    setEncodeError("");
    setEncodeOutput("");
    try {
      const response = await fetch("/api/cryptography", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: encodeInput, operation: encodeOp, shift: caesarShift })
      });
      const data = await response.json();
      if (!response.ok || !data.success) throw new Error(data.error || "Encoding operation failed.");
      setEncodeOutput(data.result);
    } catch (err) {
      setEncodeError(err.message);
    } finally {
      setEncodeLoading(false);
    }
  }

  // --- Run Key Generator ---
  async function fetchKeys() {
    setKeysLoading(true);
    try {
      const response = await fetch("/api/cryptography", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ operation: "generate_keys" })
      });
      const data = await response.json();
      if (response.ok && data.success) {
        setGeneratedKeys(data.result);
      }
    } catch (err) {
      console.error("Key generation error:", err);
    } finally {
      setKeysLoading(false);
    }
  }

  // --- Run HMAC ---
  async function runHmac(event) {
    if (event) event.preventDefault();
    setHmacLoading(true);
    try {
      const response = await fetch("/api/cryptography", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: hmacMessage, key: hmacSecret, operation: hmacAlgo })
      });
      const data = await response.json();
      if (response.ok && data.success) {
        setHmacResult(data.result);
      }
    } catch (err) {
      console.error("HMAC error:", err);
    } finally {
      setHmacLoading(false);
    }
  }

  return (
    <section className="crypto-page">
      {/* Header */}
      <header className="module-header crypto-header">
        <div className="module-heading">
          <div className="module-heading-icon">
            <KeyRound size={26} />
          </div>
          <div>
            <p className="eyebrow">FLAGSHIP CRYPTOGRAPHIC SUITE</p>
            <h2>Cryptographic Analysis & Data Integrity Lab</h2>
            <p className="subtitle">
              Multi-Hash Engine | Format Identifier | Text Encoding | JWT Inspection | CSPRNG Keys
            </p>
          </div>
        </div>
        <div className={`module-state ${hashLoading || analysisLoading ? "busy" : "success"}`}>
          <span />
          {hashLoading || analysisLoading ? "PROCESSING" : "ENGINE READY"}
        </div>
      </header>

      {/* Tabs */}
      <nav style={{ display: "flex", gap: "10px", marginBottom: "22px", flexWrap: "wrap" }}>
        {[
          { id: "hash", label: "Multi-Hash Engine", icon: Hash },
          { id: "identify", label: "Hash Identifier & Analyst", icon: Fingerprint },
          { id: "encode", label: "Transforms & Token Inspector", icon: Code },
          { id: "keys", label: "CSPRNG Key Station", icon: Key },
          { id: "hmac", label: "HMAC Authentication", icon: Lock }
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              type="button"
              onClick={() => {
                setActiveTab(tab.id);
                if (tab.id === "keys" && !generatedKeys) fetchKeys();
              }}
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "8px",
                padding: "10px 18px",
                borderRadius: "10px",
                border: isActive ? "1px solid rgba(61, 238, 177, 0.5)" : "1px solid rgba(120, 135, 190, 0.2)",
                background: isActive ? "linear-gradient(135deg, rgba(30, 214, 156, 0.2), rgba(66, 83, 255, 0.15))" : "rgba(10, 14, 32, 0.6)",
                color: isActive ? "#7ff0ca" : "#8e9ab8",
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

      {/* TAB 1: Multi-Hash Engine */}
      {activeTab === "hash" && (
        <>
          <div className="crypto-layout">
            <form className="crypto-tool-card" onSubmit={generateAllHashes}>
              <div className="crypto-card-heading">
                <div>
                  <span>CRYPTOGRAPHIC MESSAGE DIGESTS</span>
                  <h3>Simultaneous Multi-Hash Generation</h3>
                </div>
                <Binary size={19} color="#72f6c3" />
              </div>
              <p style={{ color: "#8e9ab8", fontSize: "13px", margin: "0 0 12px" }}>
                Generate all industry-standard cryptographic hashes simultaneously from a single input string.
              </p>
              <label className="crypto-label">
                INPUT PLAINTEXT
                <textarea
                  rows={4}
                  value={hashText}
                  onChange={(event) => setHashText(event.target.value)}
                  placeholder="Enter text to hash..."
                  disabled={hashLoading}
                  style={{ width: "100%", background: "rgba(5, 8, 20, 0.8)", border: "1px solid rgba(120, 135, 190, 0.3)", borderRadius: "8px", color: "#e2e8f0", padding: "10px", fontSize: "13px", boxSizing: "border-box" }}
                />
              </label>
              <button className="crypto-run-button" type="submit" disabled={hashLoading} style={{ marginTop: "12px" }}>
                {hashLoading ? <RefreshCw className="spin-icon" size={17} /> : <Play size={17} />}
                {hashLoading ? "GENERATING HASHES..." : "GENERATE ALL 10+ HASHES"}
              </button>
              {hashError && <p className="crypto-error">{hashError}</p>}
            </form>

            <aside className="crypto-side-card">
              <Fingerprint size={25} />
              <span>DIGEST INTEGRITY</span>
              <h3>Algorithms Evaluated</h3>
              <p>Generates digests across all modern and legacy hash standards for direct comparison:</p>
              <div className="crypto-algorithm-pills" style={{ display: "flex", flexWrap: "wrap", gap: "6px", marginTop: "12px" }}>
                <b>MD5 (128b)</b>
                <b>SHA-1 (160b)</b>
                <b>SHA-256 (256b)</b>
                <b>SHA-384 (384b)</b>
                <b>SHA-512 (512b)</b>
                <b>SHA3-256</b>
                <b>SHA3-512</b>
                <b>BLAKE2b</b>
                <b>BLAKE2s</b>
              </div>
              <div style={{ marginTop: "16px", borderTop: "1px solid rgba(255,255,255,0.08)", paddingTop: "12px" }}>
                <span style={{ fontSize: "10px", color: "#7482a5", display: "block" }}>LIVE VERIFICATION (OPTIONAL)</span>
                <input
                  type="text"
                  placeholder="Paste expected hash to compare..."
                  value={verifyHash}
                  onChange={(e) => setVerifyHash(e.target.value)}
                  style={{ width: "100%", height: "36px", background: "rgba(0,0,0,0.4)", border: "1px solid rgba(120, 135, 190, 0.3)", borderRadius: "6px", color: "#7ff0ca", padding: "0 8px", fontSize: "12px", marginTop: "6px", boxSizing: "border-box" }}
                />
              </div>
            </aside>
          </div>

          <section className="crypto-output">
            <div className="crypto-output-heading">
              <div>
                <p className="eyebrow">DIGEST CONSOLE</p>
                <h3>Generated Cryptographic Hashes</h3>
              </div>
              {hashResults && <ShieldCheck size={20} color="#72f6c3" />}
            </div>

            {!hashResults ? (
              <div className="crypto-empty">
                <Fingerprint size={23} />
                <div>
                  <strong>Ready to calculate digests</strong>
                  <p>Click "GENERATE ALL 10+ HASHES" to view side-by-side message digests.</p>
                </div>
              </div>
            ) : (
              <div className="hash-grid">
                {Object.entries(hashResults).map(([algorithm, digest]) => {
                  const isMatch = verifyHash.trim() && verifyHash.trim().toLowerCase() === digest.toLowerCase();
                  return (
                    <article className="hash-row" key={algorithm} style={{ borderLeft: isMatch ? "3px solid #4ade80" : "none", background: isMatch ? "rgba(34, 197, 94, 0.1)" : undefined }}>
                      <div>
                        <span style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                          {titleForAlgorithm(algorithm)}
                          {isMatch && <b style={{ background: "#22c55e", color: "#000", padding: "1px 6px", borderRadius: "4px", fontSize: "10px" }}>MATCH FOUND!</b>}
                        </span>
                        <code>{digest}</code>
                      </div>
                      <button onClick={() => copy(digest, algorithm)} type="button" aria-label={`Copy ${algorithm} hash`}>
                        {copiedKey === algorithm ? <Check size={17} color="#4ade80" /> : <Copy size={17} />}
                      </button>
                    </article>
                  );
                })}
              </div>
            )}
          </section>
        </>
      )}

      {/* TAB 2: Hash Format Identifier & Analyzer */}
      {activeTab === "identify" && (
        <div style={{ display: "grid", gridTemplateColumns: "1.1fr 0.9fr", gap: "20px" }}>
          <form className="crypto-tool-card" onSubmit={runHashIdentifier} style={{ padding: "24px" }}>
            <div className="crypto-card-heading">
              <div>
                <span>CRYPTO ANALYST FORMAT IDENTIFIER</span>
                <h3>Identify Unknown Hash Format</h3>
              </div>
              <Fingerprint size={20} color="#72f6c3" />
            </div>
            <p style={{ color: "#8e9ab8", fontSize: "13px", lineHeight: "1.5", margin: "0 0 14px" }}>
              Encountered an unknown hash in a configuration file, memory dump, or database? Paste it below to identify its algorithm, character set, Shannon entropy, and security rating.
            </p>

            <label className="crypto-label">
              UNKNOWN HASH STRING
              <input
                type="text"
                value={unknownHash}
                onChange={(e) => setUnknownHash(e.target.value)}
                placeholder="e.g. 5d41402abc4b2a76b9719d911017c592 or $2a$12$..."
                style={{ width: "100%", height: "45px", background: "rgba(5, 8, 20, 0.8)", border: "1px solid rgba(120, 135, 190, 0.3)", borderRadius: "8px", color: "#7ff0ca", padding: "0 12px", fontSize: "13px", fontFamily: "monospace", boxSizing: "border-box", marginTop: "6px" }}
              />
            </label>

            <button type="submit" disabled={analysisLoading} className="crypto-run-button" style={{ marginTop: "16px", width: "100%" }}>
              {analysisLoading ? <RefreshCw className="spin-icon" size={16} /> : <Search size={16} />}
              {analysisLoading ? "ANALYZING HASH FORMAT..." : "ANALYZE HASH FORMAT"}
            </button>
            {analysisError && <p className="crypto-error">{analysisError}</p>}

            <div style={{ marginTop: "20px" }}>
              <span style={{ fontSize: "11px", color: "#7482a5", display: "block", marginBottom: "8px" }}>Try sample hash signatures:</span>
              <div style={{ display: "flex", flexWrap: "wrap", gap: "6px" }}>
                {[
                  { label: "MD5 (32 hex)", hash: "5d41402abc4b2a76b9719d911017c592" },
                  { label: "SHA-1 (40 hex)", hash: "2ef7bde608ce5404e97d5f042f95f89f1c232871" },
                  { label: "SHA-256 (64 hex)", hash: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" },
                  { label: "Bcrypt ($2a$...)", hash: "$2a$12$R9h/cIPz0gi.URNNXRkh2OPST9/PgBkqquzi.Ss7KIUgO2t0jWMUW" },
                  { label: "Argon2 ($argon2...)", hash: "$argon2id$v=19$m=65536,t=3,p=4$c29tZXNhbHQ$RdescudvJCsgqlfreSdKJK" }
                ].map((s) => (
                  <button
                    key={s.label}
                    type="button"
                    onClick={() => setUnknownHash(s.hash)}
                    style={{ background: "rgba(61, 238, 177, 0.1)", border: "1px solid rgba(61, 238, 177, 0.25)", color: "#7ff0ca", borderRadius: "6px", padding: "4px 8px", fontSize: "11px", cursor: "pointer" }}
                  >
                    {s.label}
                  </button>
                ))}
              </div>
            </div>
          </form>

          <div className="crypto-side-card" style={{ padding: "24px" }}>
            <span style={{ color: "#8f9abb", fontSize: "10px", fontWeight: "800", letterSpacing: "1px" }}>ANALYST FINDINGS</span>
            <h3 style={{ color: "#edf0ff", margin: "4px 0 16px", fontSize: "18px" }}>Signature Diagnosis</h3>

            {analysisResult ? (
              <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "8px" }}>
                  <div style={{ background: "rgba(0,0,0,0.3)", padding: "10px", borderRadius: "8px" }}>
                    <small style={{ color: "#7482a5", display: "block" }}>LENGTH</small>
                    <strong style={{ fontSize: "16px", color: "#7ff0ca" }}>{analysisResult.length} chars</strong>
                  </div>
                  <div style={{ background: "rgba(0,0,0,0.3)", padding: "10px", borderRadius: "8px" }}>
                    <small style={{ color: "#7482a5", display: "block" }}>ENTROPY</small>
                    <strong style={{ fontSize: "16px", color: "#38bdf8" }}>{analysisResult.entropy}</strong>
                  </div>
                  <div style={{ background: "rgba(0,0,0,0.3)", padding: "10px", borderRadius: "8px" }}>
                    <small style={{ color: "#7482a5", display: "block" }}>CHARSET</small>
                    <strong style={{ fontSize: "11px", color: "#e2e8f0" }}>{analysisResult.hexadecimal ? "Hex (0-9,a-f)" : "Modular/B64"}</strong>
                  </div>
                </div>

                <div style={{ marginTop: "4px" }}>
                  <strong style={{ fontSize: "12px", color: "#fff", display: "block", marginBottom: "8px" }}>Candidate Hash Algorithms:</strong>
                  {analysisResult.candidates && analysisResult.candidates.length > 0 ? (
                    <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                      {analysisResult.candidates.map((cand, i) => (
                        <div key={i} style={{ background: "rgba(0,0,0,0.4)", padding: "12px", borderRadius: "8px", border: "1px solid rgba(255,255,255,0.06)" }}>
                          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                            <strong style={{ color: "#7ff0ca", fontSize: "14px" }}>{cand.algorithm}</strong>
                            <span style={{
                              padding: "2px 8px",
                              borderRadius: "4px",
                              fontSize: "10px",
                              fontWeight: "700",
                              background: cand.status === "SECURE" ? "rgba(34, 197, 94, 0.2)" : cand.status === "VULNERABLE" ? "rgba(239, 68, 68, 0.2)" : "rgba(234, 179, 8, 0.2)",
                              color: cand.status === "SECURE" ? "#4ade80" : cand.status === "VULNERABLE" ? "#f87171" : "#facc15"
                            }}>
                              {cand.status}
                            </span>
                          </div>
                          <small style={{ color: "#94a3b8", display: "block", marginTop: "2px" }}>{cand.category} &bull; {cand.bit_length} bits &bull; Confidence: <b>{cand.confidence}</b></small>
                          <p style={{ color: "#cbd5e1", fontSize: "12px", margin: "6px 0 0" }}>{cand.description}</p>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p style={{ color: "#7482a5", fontSize: "12px" }}>No standard algorithm signatures matched this exact length/prefix combination.</p>
                  )}
                </div>
              </div>
            ) : (
              <div style={{ color: "#7482a5", fontSize: "13px" }}>
                Paste any hash on the left and click "ANALYZE HASH FORMAT" to diagnose candidate algorithms.
              </div>
            )}
          </div>
        </div>
      )}

      {/* TAB 3: Encoders & Decoders */}
      {activeTab === "encode" && (
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px" }}>
          <form className="crypto-tool-card" onSubmit={runEncoder} style={{ padding: "24px" }}>
            <div className="crypto-card-heading">
              <div>
                <span>MULTI-FORMAT TRANSFORM ENGINE</span>
                <h3>Encode or Decode Text</h3>
              </div>
              <Code size={20} color="#72f6c3" />
            </div>

            <label className="crypto-label">
              SELECT OPERATION
              <select
                value={encodeOp}
                onChange={(e) => { setEncodeOp(e.target.value); setEncodeOutput(""); }}
                style={{ width: "100%", height: "42px", background: "rgba(5, 8, 20, 0.8)", border: "1px solid rgba(120, 135, 190, 0.3)", borderRadius: "8px", color: "#7ff0ca", padding: "0 10px", fontSize: "13px", marginTop: "6px" }}
              >
                <option value="base64_encode">Base64 Encode</option>
                <option value="base64_decode">Base64 Decode</option>
                <option value="base32_encode">Base32 Encode</option>
                <option value="base32_decode">Base32 Decode</option>
                <option value="hex_encode">Hexadecimal Encode</option>
                <option value="hex_decode">Hexadecimal Decode</option>
                <option value="binary_encode">Binary (8-bit) Encode</option>
                <option value="binary_decode">Binary (8-bit) Decode</option>
                <option value="url_encode">URL Encode (RFC 3986)</option>
                <option value="url_decode">URL Decode</option>
                <option value="rot13">ROT13 Cipher Transform</option>
                <option value="caesar_encrypt">Caesar Cipher Encode (educational)</option>
                <option value="caesar_decrypt">Caesar Cipher Decode (educational)</option>
                <option value="jwt_inspect">JWT Header & Payload Inspector</option>
              </select>
            </label>

            {(encodeOp === "caesar_encrypt" || encodeOp === "caesar_decrypt") && (
              <label className="crypto-label" style={{ marginTop: "14px", display: "block" }}>
                CAESAR SHIFT (1–25)
                <input
                  type="number"
                  min="1"
                  max="25"
                  value={caesarShift}
                  onChange={(e) => setCaesarShift(e.target.value)}
                  style={{ width: "100%", height: "42px", background: "rgba(5, 8, 20, 0.8)", border: "1px solid rgba(120, 135, 190, 0.3)", borderRadius: "8px", color: "#7ff0ca", padding: "0 10px", fontSize: "13px", marginTop: "6px", boxSizing: "border-box" }}
                />
              </label>
            )}

            <label className="crypto-label" style={{ marginTop: "14px", display: "block" }}>
              {encodeOp === "jwt_inspect" ? "JWT TOKEN" : "INPUT TEXT"}
              <textarea
                rows={6}
                value={encodeInput}
                onChange={(e) => setEncodeInput(e.target.value)}
                placeholder={encodeOp === "jwt_inspect" ? "Paste a three-part JWT token. It will be decoded only; its signature is not verified." : "Enter text to process..."}
                style={{ width: "100%", background: "rgba(5, 8, 20, 0.8)", border: "1px solid rgba(120, 135, 190, 0.3)", borderRadius: "8px", color: "#e2e8f0", padding: "10px", fontSize: "13px", boxSizing: "border-box", marginTop: "6px" }}
              />
            </label>

            <div style={{ display: "flex", gap: "10px", marginTop: "16px" }}>
              <button type="submit" disabled={encodeLoading} className="crypto-run-button" style={{ flex: 1 }}>
                {encodeLoading ? <RefreshCw className="spin-icon" size={16} /> : <Play size={16} />}
                {encodeLoading ? "CONVERTING..." : "RUN CONVERSION"}
              </button>
              {encodeOutput && (
                <button
                  type="button"
                  onClick={() => { setEncodeInput(encodeOutput); setEncodeOutput(""); }}
                  title="Swap output into input"
                  style={{ background: "rgba(255,255,255,0.06)", border: "1px solid rgba(255,255,255,0.15)", borderRadius: "8px", padding: "0 14px", color: "#e2e8f0", cursor: "pointer" }}
                >
                  <ArrowRightLeft size={16} />
                </button>
              )}
            </div>
            {encodeError && <p className="crypto-error">{encodeError}</p>}
          </form>

          <div className="crypto-side-card" style={{ padding: "24px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <span style={{ color: "#8f9abb", fontSize: "10px", fontWeight: "800", letterSpacing: "1px" }}>TRANSFORM RESULT</span>
              {encodeOutput && (
                <button
                  type="button"
                  onClick={() => copy(encodeOutput, "output")}
                  style={{ background: "none", border: "none", color: "#7ff0ca", cursor: "pointer", display: "flex", alignItems: "center", gap: "4px", fontSize: "12px" }}
                >
                  {copiedKey === "output" ? <Check size={14} color="#4ade80" /> : <Copy size={14} />}
                  {copiedKey === "output" ? "COPIED" : "COPY"}
                </button>
              )}
            </div>
            <h3 style={{ color: "#edf0ff", margin: "4px 0 16px", fontSize: "18px" }}>Output String</h3>

            {encodeOutput ? (
              <div style={{ background: "rgba(0,0,0,0.5)", padding: "16px", borderRadius: "8px", border: "1px solid rgba(255,255,255,0.08)" }}>
                <code style={{ color: "#7ff0ca", wordBreak: "break-all", fontSize: "13px", display: "block", whiteSpace: "pre-wrap" }}>
                  {typeof encodeOutput === "string" ? encodeOutput : JSON.stringify(encodeOutput, null, 2)}
                </code>
              </div>
            ) : (
              <div style={{ color: "#7482a5", fontSize: "13px", paddingTop: "20px" }}>
                Select a transformation mode and click "RUN CONVERSION" to inspect the output.
              </div>
            )}
          </div>
        </div>
      )}

      {/* TAB 4: CSPRNG Key Station */}
      {activeTab === "keys" && (
        <div style={{ display: "grid", gridTemplateColumns: "1.2fr 0.8fr", gap: "20px" }}>
          <div className="crypto-tool-card" style={{ padding: "24px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
              <div>
                <span style={{ color: "#7ff0ca", fontSize: "10px", fontWeight: "800", letterSpacing: "1px" }}>CSPRNG SECURITY GENERATOR</span>
                <h3 style={{ color: "#fff", margin: "2px 0 0" }}>High-Entropy Keys & Tokens</h3>
              </div>
              <button
                type="button"
                onClick={fetchKeys}
                disabled={keysLoading}
                style={{ background: "rgba(61, 238, 177, 0.15)", border: "1px solid rgba(61, 238, 177, 0.35)", borderRadius: "8px", padding: "8px 14px", color: "#7ff0ca", cursor: "pointer", display: "flex", alignItems: "center", gap: "6px", fontSize: "12px", fontWeight: "600" }}
              >
                <RefreshCw size={14} className={keysLoading ? "spin-icon" : ""} />
                GENERATE NEW KEYS
              </button>
            </div>

            {generatedKeys ? (
              <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                {[
                  { label: "AES-256 key material (Hex 32-byte)", value: generatedKeys.aes256_hex, key: "aes256" },
                  { label: "AES-128 key material (Hex 16-byte)", value: generatedKeys.aes128_hex, key: "aes128" },
                  { label: "Secure API Bearer Token (Base64URL 48-Byte)", value: generatedKeys.api_token_64, key: "token" },
                  { label: "UUID v4 (RFC 4122 Compliant)", value: generatedKeys.uuid_v4, key: "uuid" },
                  { label: "High-Entropy Passphrase / Secret", value: generatedKeys.secure_passphrase, key: "passphrase" }
                ].map((item) => (
                  <div key={item.key} style={{ background: "rgba(0,0,0,0.35)", padding: "12px", borderRadius: "8px", border: "1px solid rgba(255,255,255,0.05)" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "4px" }}>
                      <small style={{ color: "#94a3b8", fontWeight: "600" }}>{item.label}</small>
                      <button
                        type="button"
                        onClick={() => copy(item.value, item.key)}
                        style={{ background: "none", border: "none", color: "#7ff0ca", cursor: "pointer", fontSize: "11px", display: "flex", alignItems: "center", gap: "4px" }}
                      >
                        {copiedKey === item.key ? <Check size={13} color="#4ade80" /> : <Copy size={13} />}
                        {copiedKey === item.key ? "COPIED" : "COPY"}
                      </button>
                    </div>
                    <code style={{ color: "#7ff0ca", fontSize: "12px", wordBreak: "break-all" }}>{item.value}</code>
                  </div>
                ))}
              </div>
            ) : (
              <div style={{ color: "#7482a5", fontSize: "13px", padding: "20px 0" }}>
                Generating cryptographically secure pseudorandom keys...
              </div>
            )}
          </div>

          <div className="crypto-side-card" style={{ padding: "24px" }}>
            <span style={{ color: "#8f9abb", fontSize: "10px", fontWeight: "800", letterSpacing: "1px" }}>RANDOMNESS ASSURANCE</span>
            <h3 style={{ color: "#fff", margin: "4px 0 16px" }}>Cryptographic Entropy</h3>
            <p style={{ color: "#8e9ab8", fontSize: "13px", lineHeight: "1.5" }}>
              All keys and tokens are derived directly from the operating system's kernel CSPRNG entropy pool (<code>/dev/urandom</code> on Linux / <code>CryptGenRandom</code> via Windows BCrypt API).
            </p>
            <div style={{ marginTop: "16px", display: "flex", flexDirection: "column", gap: "8px", fontSize: "12px", color: "#cbd5e1" }}>
              <div>&bull; <b>No pseudorandom PRNG seeds</b> (unpredictable)</div>
              <div>&bull; Key material for use with a <b>trusted encryption library</b></div>
              <div>&bull; <b>Collision-resistant</b> UUIDv4 space (&gt; 5.3 &times; 10<sup>36</sup>)</div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 5: HMAC Authentication */}
      {activeTab === "hmac" && (
        <div style={{ display: "grid", gridTemplateColumns: "1.1fr 0.9fr", gap: "20px" }}>
          <form className="crypto-tool-card" onSubmit={runHmac} style={{ padding: "24px" }}>
            <div className="crypto-card-heading">
              <div>
                <span>KEYED-HASH MESSAGE AUTHENTICATION</span>
                <h3>Calculate HMAC Signature</h3>
              </div>
              <Lock size={20} color="#72f6c3" />
            </div>

            <label className="crypto-label">
              SECRET KEY
              <input
                type="text"
                value={hmacSecret}
                onChange={(e) => setHmacSecret(e.target.value)}
                style={{ width: "100%", height: "42px", background: "rgba(5, 8, 20, 0.8)", border: "1px solid rgba(120, 135, 190, 0.3)", borderRadius: "8px", color: "#7ff0ca", padding: "0 10px", fontSize: "13px", marginTop: "6px", boxSizing: "border-box" }}
              />
            </label>

            <label className="crypto-label" style={{ marginTop: "12px", display: "block" }}>
              ALGORITHM
              <select
                value={hmacAlgo}
                onChange={(e) => setHmacAlgo(e.target.value)}
                style={{ width: "100%", height: "42px", background: "rgba(5, 8, 20, 0.8)", border: "1px solid rgba(120, 135, 190, 0.3)", borderRadius: "8px", color: "#7ff0ca", padding: "0 10px", fontSize: "13px", marginTop: "6px" }}
              >
                <option value="hmac_sha256">HMAC-SHA256 (NIST Standard)</option>
                <option value="hmac_sha512">HMAC-SHA512 (High Capacity)</option>
              </select>
            </label>

            <label className="crypto-label" style={{ marginTop: "12px", display: "block" }}>
              PAYLOAD / MESSAGE
              <textarea
                rows={4}
                value={hmacMessage}
                onChange={(e) => setHmacMessage(e.target.value)}
                style={{ width: "100%", background: "rgba(5, 8, 20, 0.8)", border: "1px solid rgba(120, 135, 190, 0.3)", borderRadius: "8px", color: "#e2e8f0", padding: "10px", fontSize: "13px", marginTop: "6px", boxSizing: "border-box" }}
              />
            </label>

            <button type="submit" disabled={hmacLoading} className="crypto-run-button" style={{ marginTop: "16px", width: "100%" }}>
              {hmacLoading ? <RefreshCw className="spin-icon" size={16} /> : <Lock size={16} />}
              {hmacLoading ? "SIGNING..." : "COMPUTE HMAC SIGNATURE"}
            </button>
          </form>

          <div className="crypto-side-card" style={{ padding: "24px" }}>
            <span style={{ color: "#8f9abb", fontSize: "10px", fontWeight: "800", letterSpacing: "1px" }}>AUTHENTICATION DIGEST</span>
            <h3 style={{ color: "#fff", margin: "4px 0 16px" }}>HMAC Output</h3>

            {hmacResult ? (
              <div style={{ background: "rgba(0,0,0,0.5)", padding: "16px", borderRadius: "8px", border: "1px solid rgba(255,255,255,0.08)" }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
                  <small style={{ color: "#7ff0ca", fontWeight: "700" }}>{hmacAlgo.toUpperCase()}</small>
                  <button
                    type="button"
                    onClick={() => copy(hmacResult, "hmac")}
                    style={{ background: "none", border: "none", color: "#7ff0ca", cursor: "pointer", display: "flex", alignItems: "center", gap: "4px", fontSize: "12px" }}
                  >
                    {copiedKey === "hmac" ? <Check size={14} color="#4ade80" /> : <Copy size={14} />}
                    {copiedKey === "hmac" ? "COPIED" : "COPY"}
                  </button>
                </div>
                <code style={{ color: "#7ff0ca", fontSize: "12px", wordBreak: "break-all" }}>{hmacResult}</code>
              </div>
            ) : (
              <div style={{ color: "#7482a5", fontSize: "13px" }}>
                Enter message and secret key on the left to compute a cryptographic HMAC signature.
              </div>
            )}
          </div>
        </div>
      )}
    </section>
  );
}
