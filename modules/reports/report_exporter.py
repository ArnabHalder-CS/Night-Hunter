# NIGHT HUNTER - Report Exporter

import sys
import json
import html
from pathlib import Path
from datetime import datetime


# ---------------------------------------------------------
# PROJECT ROOT
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

REPORTS_DIRECTORY = PROJECT_ROOT / "reports"

REPORTS_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)


# ---------------------------------------------------------
# BASIC HELPERS
# ---------------------------------------------------------

def create_timestamp():
    """
    Create a timestamp suitable for filenames.
    """

    return datetime.now().strftime("%Y%m%d_%H%M%S")


def safe_filename(name):
    """
    Remove characters that are unsafe for filenames.
    """

    if not name:
        return "night_hunter_report"

    allowed = (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"
        "_-"
    )

    cleaned = ""

    for character in str(name):

        if character in allowed:
            cleaned += character

        elif character in (" ", ".", "/"):
            cleaned += "_"

    cleaned = cleaned.strip("_")

    if not cleaned:
        return "night_hunter_report"

    return cleaned


def create_report_filename(
    target="target",
    extension="json"
):
    """
    Create a timestamped report filename.
    """

    target_name = safe_filename(target)
    timestamp = create_timestamp()

    return (
        f"night_hunter_"
        f"{target_name}_"
        f"{timestamp}."
        f"{extension}"
    )


def get_report_path(
    target="target",
    extension="json"
):
    """
    Return the complete path for a report.
    """

    filename = create_report_filename(
        target,
        extension
    )

    return REPORTS_DIRECTORY / filename


# ---------------------------------------------------------
# REPORT NORMALIZATION
# ---------------------------------------------------------

def normalize_report(report):
    """
    Make sure the report is stored as a dictionary.
    """

    if report is None:
        return {
            "tool": "NIGHT HUNTER",
            "generated": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "summary": {},
            "findings": []
        }

    if isinstance(report, dict):
        normalized = dict(report)

    else:
        normalized = {
            "tool": "NIGHT HUNTER",
            "data": report
        }

    if "tool" not in normalized:
        normalized["tool"] = "NIGHT HUNTER"

    if "generated" not in normalized:
        normalized["generated"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    if "findings" not in normalized:
        normalized["findings"] = []

    if "summary" not in normalized:
        normalized["summary"] = {}

    return normalized


# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------

def calculate_summary(report):
    """
    Calculate finding counts by severity.
    """

    report = normalize_report(report)

    findings = report.get("findings", [])

    summary = {
        "total": 0,
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
        "info": 0
    }

    if not isinstance(findings, list):
        findings = []

    for finding in findings:

        if not isinstance(finding, dict):
            continue

        summary["total"] += 1

        severity = str(
            finding.get("severity", "info")
        ).lower().strip()

        if severity == "critical":
            summary["critical"] += 1

        elif severity == "high":
            summary["high"] += 1

        elif severity == "medium":
            summary["medium"] += 1

        elif severity == "low":
            summary["low"] += 1

        else:
            summary["info"] += 1

    return summary


def update_summary(report):
    """
    Update the report with calculated severity totals.
    """

    report = normalize_report(report)

    report["summary"] = calculate_summary(report)

    return report


# ---------------------------------------------------------
# JSON EXPORT
# ---------------------------------------------------------

def export_json(
    report,
    target="target",
    output_path=None
):
    """
    Export the report as JSON.
    """

    report = update_summary(report)

    if output_path is None:
        output_path = get_report_path(
            target,
            "json"
        )

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    try:

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                report,
                file,
                indent=4,
                ensure_ascii=False,
                default=str
            )

        print()
        print("[+] JSON report created.")
        print(f"[+] Location: {output_path}")

        return str(output_path)

    except OSError as error:

        print(
            f"[!] Failed to create JSON report: {error}"
        )

        return None


# ---------------------------------------------------------
# TEXT EXPORT
# ---------------------------------------------------------

def finding_to_text(finding, number):
    """
    Convert one finding into readable text.
    """

    if not isinstance(finding, dict):
        return (
            f"Finding #{number}\n"
            f"Data: {finding}\n"
        )

    category = finding.get(
        "category",
        "Unknown"
    )

    severity = finding.get(
        "severity",
        "Info"
    )

    description = finding.get(
        "description",
        ""
    )

    evidence = finding.get(
        "evidence",
        ""
    )

    recommendation = finding.get(
        "recommendation",
        ""
    )

    timestamp = finding.get(
        "timestamp",
        ""
    )

    target = finding.get(
        "target",
        ""
    )

    text = []

    text.append(
        f"Finding #{number}"
    )

    text.append(
        f"Category: {category}"
    )

    text.append(
        f"Severity: {severity}"
    )

    if target:
        text.append(
            f"Target: {target}"
        )

    text.append(
        f"Description: {description}"
    )

    if evidence:
        text.append(
            f"Evidence: {evidence}"
        )

    if recommendation:
        text.append(
            f"Recommendation: {recommendation}"
        )

    if timestamp:
        text.append(
            f"Timestamp: {timestamp}"
        )

    text.append(
        "-" * 60
    )

    return "\n".join(text)


def export_text(
    report,
    target="target",
    output_path=None
):
    """
    Export the report as a TXT file.
    """

    report = update_summary(report)

    if output_path is None:
        output_path = get_report_path(
            target,
            "txt"
        )

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    summary = report.get(
        "summary",
        {}
    )

    findings = report.get(
        "findings",
        []
    )

    lines = []

    lines.append("=" * 70)
    lines.append("NIGHT HUNTER SECURITY REPORT")
    lines.append("=" * 70)

    lines.append(
        f"Generated: {report.get('generated', '')}"
    )

    lines.append(
        f"Target: {report.get('target', target)}"
    )

    lines.append(
        f"Module: {report.get('module', 'N/A')}"
    )

    lines.append("")

    lines.append("-" * 70)
    lines.append("SUMMARY")
    lines.append("-" * 70)

    lines.append(
        f"Total Findings : {summary.get('total', 0)}"
    )

    lines.append(
        f"Critical       : {summary.get('critical', 0)}"
    )

    lines.append(
        f"High           : {summary.get('high', 0)}"
    )

    lines.append(
        f"Medium         : {summary.get('medium', 0)}"
    )

    lines.append(
        f"Low            : {summary.get('low', 0)}"
    )

    lines.append(
        f"Info           : {summary.get('info', 0)}"
    )

    lines.append("")

    lines.append("-" * 70)
    lines.append("FINDINGS")
    lines.append("-" * 70)

    if not findings:

        lines.append(
            "No findings were recorded."
        )

    else:

        for index, finding in enumerate(
            findings,
            start=1
        ):

            lines.append(
                finding_to_text(
                    finding,
                    index
                )
            )

    lines.append("")
    lines.append("=" * 70)
    lines.append(
        "Generated by NIGHT HUNTER"
    )
    lines.append("=" * 70)

    try:

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                "\n".join(lines)
            )

        print()
        print("[+] TXT report created.")
        print(f"[+] Location: {output_path}")

        return str(output_path)

    except OSError as error:

        print(
            f"[!] Failed to create TXT report: {error}"
        )

        return None


# ---------------------------------------------------------
# HTML HELPERS
# ---------------------------------------------------------

def html_escape(value):
    """
    Safely convert data into HTML text.
    """

    if value is None:
        return ""

    return html.escape(
        str(value)
    )


def severity_class(severity):
    """
    Return a CSS class based on severity.
    """

    severity = str(
        severity or "info"
    ).lower()

    if severity == "critical":
        return "critical"

    if severity == "high":
        return "high"

    if severity == "medium":
        return "medium"

    if severity == "low":
        return "low"

    return "info"


# ---------------------------------------------------------
# HTML EXPORT
# ---------------------------------------------------------

def build_html(report):
    """
    Build a complete HTML security report.
    """

    report = update_summary(report)

    summary = report.get(
        "summary",
        {}
    )

    findings = report.get(
        "findings",
        []
    )

    target = report.get(
        "target",
        "Unknown"
    )

    module = report.get(
        "module",
        "N/A"
    )

    generated = report.get(
        "generated",
        ""
    )

    finding_rows = []

    for index, finding in enumerate(
        findings,
        start=1
    ):

        if not isinstance(finding, dict):
            continue

        severity = finding.get(
            "severity",
            "Info"
        )

        finding_rows.append(
            f"""
            <div class="finding">
                <div class="finding-header">
                    <span class="finding-number">
                        #{index}
                    </span>

                    <span class="severity {severity_class(severity)}">
                        {html_escape(severity)}
                    </span>
                </div>

                <h3>
                    {html_escape(
                        finding.get(
                            "category",
                            "Unknown"
                        )
                    )}
                </h3>

                <p>
                    {html_escape(
                        finding.get(
                            "description",
                            ""
                        )
                    )}
                </p>

                <div class="section">
                    <strong>Evidence</strong>
                    <p>
                        {html_escape(
                            finding.get(
                                "evidence",
                                ""
                            )
                        )}
                    </p>
                </div>

                <div class="section">
                    <strong>Recommendation</strong>
                    <p>
                        {html_escape(
                            finding.get(
                                "recommendation",
                                ""
                            )
                        )}
                    </p>
                </div>

                <div class="timestamp">
                    {html_escape(
                        finding.get(
                            "timestamp",
                            ""
                        )
                    )}
                </div>
            </div>
            """
        )

    if not finding_rows:

        finding_rows.append(
            """
            <div class="no-findings">
                No findings were recorded.
            </div>
            """
        )

    return f"""<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>
NIGHT HUNTER Security Report
</title>

<style>

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    padding: 0;
    background: #080808;
    color: #eeeeee;
    font-family: Arial, Helvetica, sans-serif;
}}

.container {{
    width: 92%;
    max-width: 1100px;
    margin: 40px auto;
}}

.header {{
    background: #111111;
    border: 1px solid #292929;
    padding: 30px;
    border-radius: 12px;
    margin-bottom: 25px;
}}

.logo {{
    color: #ff1744;
    font-size: 32px;
    font-weight: bold;
    letter-spacing: 2px;
}}

.subtitle {{
    color: #999999;
    margin-top: 8px;
}}

.info {{
    margin-top: 25px;
    display: grid;
    grid-template-columns:
        repeat(auto-fit, minmax(220px, 1fr));
    gap: 12px;
}}

.info-box {{
    background: #181818;
    padding: 15px;
    border-radius: 8px;
}}

.label {{
    color: #888888;
    font-size: 12px;
    text-transform: uppercase;
}}

.value {{
    margin-top: 5px;
    font-size: 15px;
    word-break: break-word;
}}

.summary {{
    display: grid;
    grid-template-columns:
        repeat(auto-fit, minmax(130px, 1fr));
    gap: 12px;
    margin-bottom: 25px;
}}

.summary-box {{
    background: #111111;
    border: 1px solid #292929;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
}}

.summary-number {{
    font-size: 28px;
    font-weight: bold;
}}

.summary-label {{
    color: #888888;
    margin-top: 6px;
    font-size: 13px;
}}

.critical {{
    color: #ff1744;
}}

.high {{
    color: #ff6b6b;
}}

.medium {{
    color: #ffb74d;
}}

.low {{
    color: #64b5f6;
}}

.info {{
    color: #90a4ae;
}}

.finding {{
    background: #111111;
    border: 1px solid #292929;
    border-radius: 10px;
    padding: 22px;
    margin-bottom: 16px;
}}

.finding-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
}}

.finding-number {{
    color: #777777;
}}

.severity {{
    font-weight: bold;
    text-transform: uppercase;
}}

.finding h3 {{
    margin-top: 18px;
}}

.finding p {{
    color: #cccccc;
    line-height: 1.6;
}}

.section {{
    margin-top: 18px;
    padding: 15px;
    background: #181818;
    border-radius: 8px;
}}

.section strong {{
    color: #ff1744;
}}

.timestamp {{
    margin-top: 15px;
    color: #666666;
    font-size: 12px;
}}

.no-findings {{
    background: #111111;
    border: 1px solid #292929;
    padding: 25px;
    border-radius: 10px;
    color: #888888;
}}

.footer {{
    text-align: center;
    margin-top: 35px;
    color: #555555;
    font-size: 13px;
}}

</style>

</head>

<body>

<div class="container">

    <div class="header">

        <div class="logo">
            NIGHT HUNTER
        </div>

        <div class="subtitle">
            Security Assessment Report
        </div>

        <div class="info">

            <div class="info-box">
                <div class="label">Target</div>
                <div class="value">
                    {html_escape(target)}
                </div>
            </div>

            <div class="info-box">
                <div class="label">Module</div>
                <div class="value">
                    {html_escape(module)}
                </div>
            </div>

            <div class="info-box">
                <div class="label">Generated</div>
                <div class="value">
                    {html_escape(generated)}
                </div>
            </div>

        </div>

    </div>


    <div class="summary">

        <div class="summary-box">
            <div class="summary-number">
                {summary.get("total", 0)}
            </div>
            <div class="summary-label">
                Total
            </div>
        </div>

        <div class="summary-box">
            <div class="summary-number critical">
                {summary.get("critical", 0)}
            </div>
            <div class="summary-label">
                Critical
            </div>
        </div>

        <div class="summary-box">
            <div class="summary-number high">
                {summary.get("high", 0)}
            </div>
            <div class="summary-label">
                High
            </div>
        </div>

        <div class="summary-box">
            <div class="summary-number medium">
                {summary.get("medium", 0)}
            </div>
            <div class="summary-label">
                Medium
            </div>
        </div>

        <div class="summary-box">
            <div class="summary-number low">
                {summary.get("low", 0)}
            </div>
            <div class="summary-label">
                Low
            </div>
        </div>

        <div class="summary-box">
            <div class="summary-number info">
                {summary.get("info", 0)}
            </div>
            <div class="summary-label">
                Info
            </div>
        </div>

    </div>


    <h2>
        Findings
    </h2>

    {''.join(finding_rows)}


    <div class="footer">
        Generated by NIGHT HUNTER
    </div>

</div>

</body>

</html>
"""


def export_html(
    report,
    target="target",
    output_path=None
):
    """
    Export the report as an HTML file.
    """

    report = update_summary(report)

    if output_path is None:
        output_path = get_report_path(
            target,
            "html"
        )

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    document = build_html(report)

    try:

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(document)

        print()
        print("[+] HTML report created.")
        print(f"[+] Location: {output_path}")

        return str(output_path)

    except OSError as error:

        print(
            f"[!] Failed to create HTML report: {error}"
        )

        return None


# ---------------------------------------------------------
# EXPORT ALL FORMATS
# ---------------------------------------------------------

def export_all(
    report,
    target="target"
):
    """
    Export JSON, TXT and HTML versions.
    """

    print()
    print("=" * 60)
    print("EXPORTING NIGHT HUNTER REPORTS")
    print("=" * 60)

    json_file = export_json(
        report,
        target
    )

    text_file = export_text(
        report,
        target
    )

    html_file = export_html(
        report,
        target
    )

    print()
    print("=" * 60)
    print("EXPORT COMPLETE")
    print("=" * 60)

    return {
        "json": json_file,
        "txt": text_file,
        "html": html_file
    }


# ---------------------------------------------------------
# TEST REPORT
# ---------------------------------------------------------

def create_test_report():
    """
    Create sample data for testing the exporter.
    """

    return {
        "tool": "NIGHT HUNTER",
        "target": "test.example.com",
        "module": "Web Security",
        "generated": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "findings": [

            {
                "target": "test.example.com",
                "category": "Security Headers",
                "severity": "Medium",
                "description": (
                    "Content Security Policy header "
                    "was not detected."
                ),
                "evidence": (
                    "CSP header missing from HTTP response."
                ),
                "recommendation": (
                    "Configure an appropriate Content "
                    "Security Policy."
                ),
                "timestamp": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            },

            {
                "target": "test.example.com",
                "category": "Cookie Security",
                "severity": "Low",
                "description": (
                    "A cookie did not contain "
                    "the expected security attributes."
                ),
                "evidence": (
                    "Security attribute check."
                ),
                "recommendation": (
                    "Review Secure, HttpOnly and "
                    "SameSite cookie settings."
                ),
                "timestamp": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            },

            {
                "target": "test.example.com",
                "category": "Example Finding",
                "severity": "High",
                "description": (
                    "This is a test finding."
                ),
                "evidence": (
                    "Exporter test data."
                ),
                "recommendation": (
                    "Remove this test finding "
                    "from production reports."
                ),
                "timestamp": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            }
        ]
    }


# ---------------------------------------------------------
# DIRECT TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    print()
    print("=" * 64)
    print("NIGHT HUNTER - REPORT EXPORTER TEST")
    print("=" * 64)

    test_report = create_test_report()

    print()
    print("[*] Creating test report...")

    results = export_all(
        test_report,
        "export_test"
    )

    print()
    print("=" * 64)
    print("CREATED FILES")
    print("=" * 64)

    for report_type, path in results.items():

        print(
            f"{report_type.upper():6} : {path}"
        )

    print()
    print("[+] Report exporter test completed.")