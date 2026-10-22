import sys
from pathlib import Path
from datetime import datetime


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# REPORT ENGINE
# ============================================================

class ReportEngine:
    """
    Central report engine for NIGHT HUNTER.

    This class collects security findings from different
    modules and prepares them for report exporting.
    """

    def __init__(
        self,
        target="Unknown",
        module="NIGHT HUNTER"
    ):
        self.target = target
        self.module = module
        self.findings = []

        self.created_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    # ========================================================
    # ADD FINDING
    # ========================================================

    def add_finding(self, finding):
        """
        Add a Finding object or dictionary to the report.
        """

        if finding is None:
            return False

        if hasattr(finding, "to_dict"):

            finding_data = finding.to_dict()

        elif isinstance(finding, dict):

            finding_data = dict(finding)

        else:

            print(
                "[!] Invalid finding. "
                "Expected Finding object or dictionary."
            )

            return False

        self.findings.append(finding_data)

        return True

    # ========================================================
    # ADD MULTIPLE FINDINGS
    # ========================================================

    def add_findings(self, findings):
        """
        Add multiple findings at once.
        """

        if findings is None:
            return 0

        if not isinstance(findings, (list, tuple)):

            print(
                "[!] Findings must be a list or tuple."
            )

            return 0

        added = 0

        for finding in findings:

            if self.add_finding(finding):
                added += 1

        return added

    # ========================================================
    # CLEAR FINDINGS
    # ========================================================

    def clear_findings(self):
        """
        Remove all findings from the current report.
        """

        self.findings.clear()

    # ========================================================
    # SEVERITY SUMMARY
    # ========================================================

    def get_summary(self):
        """
        Calculate the number of findings by severity.
        """

        summary = {
            "total": 0,
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "info": 0
        }

        for finding in self.findings:

            if not isinstance(finding, dict):
                continue

            summary["total"] += 1

            severity = str(
                finding.get(
                    "severity",
                    "info"
                )
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

    # ========================================================
    # BUILD REPORT
    # ========================================================

    def build_report(self):
        """
        Build the complete report dictionary.
        """

        return {
            "tool": "NIGHT HUNTER",
            "target": self.target,
            "module": self.module,
            "generated": self.created_at,
            "summary": self.get_summary(),
            "findings": list(self.findings)
        }

    # ========================================================
    # GET FINDINGS
    # ========================================================

    def get_findings(self):
        """
        Return a copy of all findings.
        """

        return list(self.findings)

    # ========================================================
    # FINDING COUNT
    # ========================================================

    def count(self):
        """
        Return total number of findings.
        """

        return len(self.findings)

    # ========================================================
    # DISPLAY SUMMARY
    # ========================================================

    def display_summary(self):
        """
        Display a simple report summary.
        """

        summary = self.get_summary()

        print()
        print("=" * 55)
        print("NIGHT HUNTER REPORT SUMMARY")
        print("=" * 55)

        print(f"Target   : {self.target}")
        print(f"Module   : {self.module}")
        print(f"Generated: {self.created_at}")

        print()
        print(f"Total Findings : {summary['total']}")
        print(f"Critical       : {summary['critical']}")
        print(f"High           : {summary['high']}")
        print(f"Medium         : {summary['medium']}")
        print(f"Low            : {summary['low']}")
        print(f"Info           : {summary['info']}")

        print("=" * 55)

    # ========================================================
    # DISPLAY FINDINGS
    # ========================================================

    def display_findings(self):
        """
        Display all findings stored in the report.
        """

        if not self.findings:

            print()
            print("[*] No findings recorded.")
            return

        print()
        print("=" * 55)
        print("NIGHT HUNTER FINDINGS")
        print("=" * 55)

        for index, finding in enumerate(
            self.findings,
            start=1
        ):

            print()
            print(f"Finding #{index}")
            print("-" * 40)

            print(
                f"Category: "
                f"{finding.get('category', 'Unknown')}"
            )

            print(
                f"Severity: "
                f"{finding.get('severity', 'Info')}"
            )

            print(
                f"Description: "
                f"{finding.get('description', '')}"
            )

            if finding.get("evidence"):

                print(
                    f"Evidence: "
                    f"{finding.get('evidence')}"
                )

            if finding.get("recommendation"):

                print(
                    f"Recommendation: "
                    f"{finding.get('recommendation')}"
                )

        print()
        print("=" * 55)

    # ========================================================
    # EXPORT
    # ========================================================

    def export(self, target=None):
        """
        Send the completed report to the existing
        NIGHT HUNTER report exporter.
        """

        from modules.reports.report_exporter import export_all

        export_target = target or self.target

        report = self.build_report()

        return export_all(
            report,
            export_target
        )


# ============================================================
# CREATE REPORT ENGINE
# ============================================================

def create_report_engine(
    target="Unknown",
    module="NIGHT HUNTER"
):
    """
    Helper function to create a ReportEngine.
    """

    return ReportEngine(
        target=target,
        module=module
    )


# ============================================================
# TEST REPORT ENGINE
# ============================================================

def test_report_engine():
    """
    Test the report engine using simple sample findings.
    """

    print()
    print("=" * 60)
    print("NIGHT HUNTER - REPORT ENGINE TEST")
    print("=" * 60)

    engine = ReportEngine(
        target="test.example.com",
        module="Web Security"
    )

    finding_one = {
        "target": "test.example.com",
        "module": "Web Security",
        "category": "Security Headers",
        "severity": "Medium",
        "description": "CSP header was not detected.",
        "evidence": "Content-Security-Policy header missing.",
        "recommendation": "Configure an appropriate CSP.",
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }

    finding_two = {
        "target": "test.example.com",
        "module": "Web Security",
        "category": "Cookie Security",
        "severity": "Low",
        "description": "Cookie security attributes should be reviewed.",
        "evidence": "Cookie attribute check.",
        "recommendation": "Review Secure, HttpOnly and SameSite.",
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }

    engine.add_finding(finding_one)
    engine.add_finding(finding_two)

    print()
    print("[+] Findings added successfully.")

    engine.display_summary()

    engine.display_findings()

    print()
    print("[*] Building report...")

    report = engine.build_report()

    print()
    print("[+] Report created successfully.")

    print()
    print("Report keys:")

    for key in report:

        print(f"  - {key}")

    print()
    print("[+] Report engine test completed.")


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    test_report_engine()