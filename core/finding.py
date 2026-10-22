# NIGHT HUNTER - Security Finding

from datetime import datetime


class Finding:

    def __init__(
        self,
        target,
        category,
        severity,
        description,
        evidence="",
        recommendation=""
    ):
        self.target = target
        self.category = category
        self.severity = severity
        self.description = description
        self.evidence = evidence
        self.recommendation = recommendation
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def display(self):
        print()
        print("----- SECURITY FINDING -----")
        print(f"Target: {self.target}")
        print(f"Category: {self.category}")
        print(f"Severity: {self.severity}")
        print(f"Description: {self.description}")
        print(f"Evidence: {self.evidence}")
        print(f"Recommendation: {self.recommendation}")
        print(f"Timestamp: {self.timestamp}")
        print("----------------------------")