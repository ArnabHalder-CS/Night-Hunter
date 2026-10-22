import { useState } from "react";

import {
  LockKeyhole,
  Eye,
  EyeOff,
  ShieldCheck,
  Activity,
  KeyRound,
  Sparkles,
  AlertTriangle,
  CheckCircle2,
  XCircle,
  RefreshCw,
} from "lucide-react";


function PasswordSecurity() {

  const [password, setPassword] = useState("");

  const [showPassword, setShowPassword] = useState(false);

  const [status, setStatus] = useState("READY");

  const [analyzing, setAnalyzing] = useState(false);

  const [analysis, setAnalysis] = useState(null);

  const [error, setError] = useState("");


  // =========================================================
  // REAL PASSWORD ANALYSIS
  // =========================================================

  async function analyzePassword(event) {

    event.preventDefault();

    const cleanPassword = password;


    if (!cleanPassword) {

      setStatus("PASSWORD REQUIRED");

      setError("Enter a password to begin analysis.");

      setAnalysis(null);

      return;
    }


    setAnalyzing(true);

    setStatus("ANALYZING");

    setError("");

    setAnalysis(null);


    try {

      const response = await fetch(
        "/api/password-security",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            password: cleanPassword,
          }),
        }
      );


      const data = await response.json();


      if (!response.ok || !data.success) {

        throw new Error(
          data.error || "Password analysis failed."
        );

      }


      setAnalysis(data.analysis);

      setStatus(data.analysis.rating || "ANALYZED");

    } catch (requestError) {

      console.error(
        "Password Security API error:",
        requestError
      );

      setError(
        requestError.message ||
        "Unable to connect to NIGHT HUNTER API."
      );

      setStatus("API ERROR");

      setAnalysis(null);

    } finally {

      setAnalyzing(false);

    }

  }


  // =========================================================
  // CLEAR
  // =========================================================

  function clearPassword() {

    setPassword("");

    setAnalysis(null);

    setError("");

    setStatus("READY");

    setAnalyzing(false);

  }


  const hasPassword = password.length > 0;


  // =========================================================
  // HELPER VALUES
  // =========================================================

  const checks = analysis?.checks || {};

  const score = analysis?.score;

  const maximumScore = analysis?.maximum_score || 10;

  const scorePercentage =
    typeof score === "number"
      ? Math.max(
          0,
          Math.min(
            100,
            (score / maximumScore) * 100
          )
        )
      : 0;


  const patterns = Array.isArray(checks.patterns)
    ? checks.patterns
    : [];


  function checkIcon(value) {

    if (value === true) {

      return (
        <div className="check-success">
          <CheckCircle2 size={18} />
        </div>
      );

    }


    if (value === false) {

      return (
        <div className="check-danger">
          <XCircle size={18} />
        </div>
      );

    }


    return (
      <div className="check-pending">
        —
      </div>
    );

  }


  function patternDisplay() {

    if (!analysis) {

      return (
        <div className="check-pending">
          —
        </div>
      );

    }


    if (patterns.length === 0) {

      return (
        <div className="check-success">
          <CheckCircle2 size={18} />
        </div>
      );

    }


    return (
      <div className="check-danger">
        <AlertTriangle size={18} />
      </div>
    );

  }


  return (

    <section className="password-security-page">


      {/* =====================================================
          HEADER
      ===================================================== */}

      <div className="password-lab-header">

        <div className="password-title-area">

          <div className="password-lab-icon">

            <LockKeyhole size={25} />

          </div>


          <div>

            <p className="eyebrow">
              NIGHT HUNTER · PASSWORD SECURITY
            </p>

            <h2>
              Password Lab
            </h2>

            <p className="subtitle">
              Analyze · Strengthen · Audit
            </p>

          </div>

        </div>


        <div
          className={`password-status ${
            analyzing
              ? "analyzing"
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
          MAIN PASSWORD WORKSPACE
      ===================================================== */}

      <div className="password-workspace">


        {/* ===================================================
            INPUT PANEL
        =================================================== */}

        <div className="password-input-panel">


          <div className="password-panel-label">

            <div>

              <span>
                PASSWORD INPUT
              </span>

              <h3>
                Test a Password
              </h3>

            </div>

            <KeyRound size={19} />

          </div>


          <form onSubmit={analyzePassword}>


            <div className="password-input-wrapper">

              <input
                type={
                  showPassword
                    ? "text"
                    : "password"
                }
                value={password}
                onChange={(event) =>
                  setPassword(event.target.value)
                }
                placeholder="Enter password to analyze"
                disabled={analyzing}
              />


              <button
                type="button"
                className="password-eye-button"
                onClick={() =>
                  setShowPassword(
                    (current) => !current
                  )
                }
                aria-label={
                  showPassword
                    ? "Hide password"
                    : "Show password"
                }
              >

                {showPassword ? (
                  <EyeOff size={18} />
                ) : (
                  <Eye size={18} />
                )}

              </button>

            </div>


            <div className="password-input-footer">

              <span>
                {password.length} characters
              </span>


              {hasPassword && !analyzing && (

                <button
                  type="button"
                  className="password-clear-button"
                  onClick={clearPassword}
                >
                  Clear
                </button>

              )}

            </div>


            <button
              type="submit"
              className="password-analyze-button"
              disabled={analyzing}
            >

              {analyzing ? (

                <RefreshCw
                  size={17}
                  className="spin-icon"
                />

              ) : (

                <ShieldCheck size={17} />

              )}


              {analyzing
                ? "ANALYZING..."
                : "ANALYZE PASSWORD"
              }

            </button>


          </form>


          {error && (

            <div className="password-error">

              <AlertTriangle size={17} />

              <span>
                {error}
              </span>

            </div>

          )}


          <div className="password-notice">

            <LockKeyhole size={16} />

            <span>
              The password is analyzed in memory by the current Night Hunter runtime and is not saved in reports. Do not submit a real password to a shared cloud deployment.
            </span>

          </div>


        </div>


        {/* ===================================================
            STRENGTH PANEL
        =================================================== */}

        <div className="password-strength-panel">


          <div className="password-panel-label">

            <div>

              <span>
                SECURITY LEVEL
              </span>

              <h3>
                Strength Analysis
              </h3>

            </div>

            <Activity size={19} />

          </div>


          {analysis ? (

            <div className="password-strength-result">


              <div className="strength-lock">

                <ShieldCheck size={28} />

              </div>


              <strong>
                {analysis.rating}
              </strong>


              <p>
                Password security score
              </p>


              <div className="strength-bar">

                <span
                  style={{
                    width: `${scorePercentage}%`,
                  }}
                ></span>

              </div>


              <small>
                {score} / {maximumScore} security score
              </small>


            </div>

          ) : (

            <div className="password-strength-empty">


              <div className="strength-lock">

                <LockKeyhole size={28} />

              </div>


              <strong>
                Awaiting Analysis
              </strong>


              <p>
                Enter a password and start the security analysis.
              </p>


              <div className="strength-bar">

                <span></span>

              </div>


              <small>
                No strength score available
              </small>


            </div>

          )}

        </div>


      </div>


      {/* =====================================================
          METRICS
      ===================================================== */}

      <div className="password-metrics">


        <div className="password-metric-card">

          <div className="password-metric-icon purple">

            <Activity size={18} />

          </div>


          <div>

            <span>
              SCORE
            </span>

            <strong>
              {analysis
                ? `${score}/${maximumScore}`
                : "—"}
            </strong>

          </div>

        </div>


        <div className="password-metric-card">

          <div className="password-metric-icon gold">

            <KeyRound size={18} />

          </div>


          <div>

            <span>
              LENGTH
            </span>

            <strong>
              {analysis?.password_length ?? "—"}
            </strong>

          </div>

        </div>


        <div className="password-metric-card">

          <div className="password-metric-icon pink">

            <Sparkles size={18} />

          </div>


          <div>

            <span>
              RATING
            </span>

            <strong>
              {analysis?.rating ?? "—"}
            </strong>

          </div>

        </div>


        <div className="password-metric-card">

          <div className="password-metric-icon green">

            <ShieldCheck size={18} />

          </div>


          <div>

            <span>
              MAX SCORE
            </span>

            <strong>
              {analysis?.maximum_score ?? "—"}
            </strong>

          </div>

        </div>


      </div>


      {/* =====================================================
          ANALYSIS GRID
      ===================================================== */}

      <div className="password-analysis-grid">


        {/* CHARACTER ANALYSIS */}

        <div className="password-analysis-panel">


          <div className="password-panel-label">

            <div>

              <span>
                CHARACTER ANALYSIS
              </span>

              <h3>
                Password Composition
              </h3>

            </div>

            <KeyRound size={18} />

          </div>


          <div className="password-check-list">


            <div className="password-check-row">

              <div>

                <strong>
                  Length
                </strong>

                <span>
                  {checks.length || "No result"}
                </span>

              </div>


              {checks.length ? (
                <div className="check-success">
                  <CheckCircle2 size={18} />
                </div>
              ) : (
                <div className="check-pending">
                  —
                </div>
              )}

            </div>


            <div className="password-check-row">

              <div>

                <strong>
                  Uppercase letters
                </strong>

                <span>
                  A-Z characters
                </span>

              </div>


              {checkIcon(checks.uppercase)}

            </div>


            <div className="password-check-row">

              <div>

                <strong>
                  Lowercase letters
                </strong>

                <span>
                  a-z characters
                </span>

              </div>


              {checkIcon(checks.lowercase)}

            </div>


            <div className="password-check-row">

              <div>

                <strong>
                  Numbers
                </strong>

                <span>
                  0-9 characters
                </span>

              </div>


              {checkIcon(checks.numbers)}

            </div>


            <div className="password-check-row">

              <div>

                <strong>
                  Special characters
                </strong>

                <span>
                  Symbols and punctuation
                </span>

              </div>


              {checkIcon(
                checks.special_character
              )}

            </div>


          </div>

        </div>


        {/* SECURITY CHECKS */}

        <div className="password-analysis-panel">


          <div className="password-panel-label">

            <div>

              <span>
                SECURITY CHECKS
              </span>

              <h3>
                Threat Indicators
              </h3>

            </div>

            <AlertTriangle size={18} />

          </div>


          <div className="password-check-list">


            <div className="password-check-row">

              <div>

                <strong>
                  Common password
                </strong>

                <span>
                  Known weak-password check
                </span>

              </div>


              {analysis
                ? checkIcon(
                    !checks.common_password
                  )
                : (
                  <div className="check-pending">
                    —
                  </div>
                )}

            </div>


            <div className="password-check-row">

              <div>

                <strong>
                  Pattern detection
                </strong>

                <span>
                  Predictable patterns
                </span>

              </div>


              {patternDisplay()}

            </div>


            <div className="password-check-row">

              <div>

                <strong>
                  Repetition
                </strong>

                <span>
                  Repeated character sequences
                </span>

              </div>


              {analysis ? (

                patterns.length === 0 ? (

                  <div className="check-success">
                    <CheckCircle2 size={18} />
                  </div>

                ) : (

                  <div className="check-danger">
                    <AlertTriangle size={18} />
                  </div>

                )

              ) : (

                <div className="check-pending">
                  —
                </div>

              )}

            </div>


            <div className="password-check-row">

              <div>

                <strong>
                  Dictionary indicators
                </strong>

                <span>
                  Common word detection
                </span>

              </div>


              <div className="check-pending">
                —
              </div>

            </div>


          </div>


          {analysis && patterns.length > 0 && (

            <div className="password-pattern-list">

              <span>
                Detected patterns
              </span>

              {patterns.map(
                (pattern, index) => (

                  <div
                    key={`${pattern}-${index}`}
                    className="password-pattern-item"
                  >

                    <AlertTriangle size={14} />

                    {pattern}

                  </div>

                )
              )}

            </div>

          )}

        </div>


      </div>


      {/* =====================================================
          SUGGESTIONS
      ===================================================== */}

      <div className="password-suggestions-panel">


        <div className="password-panel-label">

          <div>

            <span>
              PASSWORD IMPROVEMENT
            </span>

            <h3>
              Suggestions
            </h3>

          </div>

          <Sparkles size={18} />

        </div>


        {analysis ? (

          <div className="password-suggestions-list">

            {analysis.suggestions &&
            analysis.suggestions.length > 0 ? (

              analysis.suggestions.map(
                (suggestion, index) => (

                  <div
                    key={`${suggestion}-${index}`}
                    className="password-suggestion-item"
                  >

                    <Sparkles size={17} />

                    <span>
                      {suggestion}
                    </span>

                  </div>

                )
              )

            ) : (

              <div className="password-suggestions-empty">

                <CheckCircle2 size={21} />

                <div>

                  <strong>
                    No additional suggestions
                  </strong>

                  <p>
                    The analyzer did not return any improvement suggestions.
                  </p>

                </div>

              </div>

            )}

          </div>

        ) : (

          <div className="password-suggestions-empty">

            <Sparkles size={21} />

            <div>

              <strong>
                Suggestions will appear here
              </strong>

              <p>
                Run an analysis to receive password-strength recommendations.
              </p>

            </div>

          </div>

        )}

      </div>


      {/* =====================================================
          FOOTER
      ===================================================== */}

      <div className="password-lab-footer">

        <div>

          <ShieldCheck size={16} />

          <span>
            NIGHT HUNTER PASSWORD SECURITY
          </span>

        </div>


        <span>
          Defensive password auditing
        </span>

      </div>


    </section>

  );

}


export default PasswordSecurity;
