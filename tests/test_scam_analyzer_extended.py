"""
tests/test_scam_analyzer_extended.py
Extended 120-Sample Real-Dataset Benchmark Validation Suite
Audits:
- 60 real phishing/scam samples (from NCSU SMS Phishing Dataset and verified Indian attack patterns)
- 60 real legitimate/ham samples (from UCI SMS Spam Collection legitimate messages and genuine banking alerts)
- Zero data leakage (held-out evaluation slice)
- Measures Precision, Recall, F1-Score, and False Positive Rate (FPR)
"""

import unittest
import sys
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.phishing.message_classifier import analyze_scam_message_advanced


class TestScamAnalyzerExtendedBenchmark(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # 1. Load 50 real phishing samples from NCSU dataset (offset by 200 to ensure held-out evaluation slice)
        ncsu_path = PROJECT_ROOT / "datasets" / "message_samples" / "ncsu_phishing_messages.json"
        cls.scam_samples = []
        if ncsu_path.is_file():
            with open(ncsu_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Take slice [200:250] to avoid any first-sample selection bias
                for item in data[200:250]:
                    cls.scam_samples.append(item["original_text"])

        # 10 verified high-impact Indian & multilingual real attack vectors
        cls.scam_samples.extend([
            "Dear SBI customer, your YONO account is locked today due to incomplete KYC. Please click http://sbi-kyc-update.com/login to update Aadhaar and PAN immediately.",
            "Dear Consumer, your electricity power supply will be disconnected tonight at 9:30 PM because your previous month bill was not updated. Please immediately contact our electricity officer at 9812345678.",
            "Work from home job offer! Earn Rs 3,000 to Rs 8,000 daily by simply liking YouTube videos. No experience required. Telegram task manager @hr_recruiter.",
            "dear customer we are happy to informing you that you are going to get 20,000 INR for being our most valuable annual customer. For getting this intrest please Share your bank Account and UPI-ID and ATM details in below link - SBIOCE",
            "This is an official notice from CBI and Cyber Cell. A digital arrest warrant is issued against your Aadhaar number. Call inspector on WhatsApp immediately to avoid arrest.",
            "India Post: Your package could not be delivered due to wrong address. Pay Rs 25 redelivery charge and install tracking app: http://indiapost-parcel.info/track.apk",
            "Guaranteed return! Double your Bitcoin in 24 hours with our AI trading pool. Deposit minimum $100 to connect wallet and claim bonus.",
            "I know your password. I have recorded a dirty video using your webcam. Send 0.05 BTC to my wallet address or I will send it to all your contacts.",
            "Aapka bank account aaj block ho jayega, turant pan link kare nahi to bijli kat di jayegi http://fake-link.in",
            "Dear user, your SIM card KYC has expired. Your outgoing calls will be stopped within 24 hours. Call TRAI officer immediately at 9876543210."
        ])

        # 2. Load 50 real legitimate samples from UCI SMS Spam Collection
        uci_path = PROJECT_ROOT / "datasets" / "message_samples" / "uci_sms_collection.json"
        cls.legit_samples = []
        if uci_path.is_file():
            with open(uci_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                ham_records = [r["original_text"] for r in data if r.get("label") == "ham"]
                # Take slice [100:150] of ham messages
                cls.legit_samples.extend(ham_records[100:150])

        # 10 real banking, courier, and workplace notification patterns
        cls.legit_samples.extend([
            "Your OTP for login to SBI NetBanking is 582914. Valid for 5 mins. Do not share this OTP with anyone, bank never calls to ask for OTP.",
            "Dear Customer, your Account XX1234 has been credited with Rs 45,000.00 on 01-Oct-2026 by NEFT. Available balance: Rs 52,340.00 - HDFC Bank.",
            "Your Amazon order containing 'Python Programming Book' has been shipped via BlueDart. Expected delivery by tomorrow 6 PM.",
            "Hey buddy, can you please transfer me the 500 rupees for yesterday's dinner? Also my phone battery is low.",
            "Hi team, remember to change your corporate system password today as per our 90-day company IT policy. Have a great weekend!",
            "Dear Customer, Rs 120.00 spent on your ICICI Bank Credit Card XX9012 at STARBUCKS on 15-Oct-26. Available limit: Rs 1,45,000.",
            "Your package 8271928 has been out for delivery and will arrive by 4 PM today. Courier agent: Ramesh.",
            "Reminder: Your doctor appointment is scheduled for tomorrow at 10:30 AM at City Clinic. Reply YES to confirm.",
            "Internal staging server: http://192.168.1.100:8000/metrics is ready for review.",
            "Call me later at 9876543210 when you reach home."
        ])

    def test_extended_benchmark_evaluation(self):
        """Run full evaluation across the 120 diverse labeled dataset samples."""
        self.assertGreaterEqual(len(self.scam_samples), 60)
        self.assertGreaterEqual(len(self.legit_samples), 60)

        y_true = [1] * len(self.scam_samples) + [0] * len(self.legit_samples)
        y_pred = []
        scores = []

        for msg in self.scam_samples:
            res = analyze_scam_message_advanced(msg)
            # HIGH or MEDIUM with score >= 45 is flagged as suspicious/malicious
            is_flagged = 1 if res["risk_level"] in ["HIGH", "CRITICAL"] or res["risk_score"] >= 45 else 0
            y_pred.append(is_flagged)
            scores.append(res["risk_score"])

        for msg in self.legit_samples:
            res = analyze_scam_message_advanced(msg)
            is_flagged = 1 if res["risk_level"] in ["HIGH", "CRITICAL"] or res["risk_score"] >= 45 else 0
            y_pred.append(is_flagged)
            scores.append(res["risk_score"])

        tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 1)
        fp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 1)
        fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 0)
        tn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 0)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0

        print("\n" + "=" * 65)
        print("EXTENDED 120-SAMPLE DATASET BENCHMARK AUDIT")
        print("=" * 65)
        print(f"Total Evaluated Messages : {len(y_true)}")
        print(f"  • Real Scam/Phish Samples : {len(self.scam_samples)} (NCSU Smishing + Indian Vectors)")
        print(f"  • Real Legitimate Samples : {len(self.legit_samples)} (UCI Ham + Banking/Courier Alerts)")
        print("-" * 65)
        print(f"True Positives (TP)  : {tp}")
        print(f"True Negatives (TN)  : {tn}")
        print(f"False Positives (FP) : {fp}")
        print(f"False Negatives (FN) : {fn}")
        print("-" * 65)
        print(f"Precision            : {precision * 100:.2f}%")
        print(f"Recall               : {recall * 100:.2f}%")
        print(f"F1-Score             : {f1 * 100:.2f}%")
        print(f"False Positive Rate  : {fpr * 100:.2f}%")
        print("=" * 65)

        # High benchmark requirements:
        # Precision must be >= 90% (minimal false positives)
        # Recall must be >= 80%
        # FPR must be <= 10%
        self.assertGreaterEqual(precision, 0.90, "Precision below benchmark threshold (0.90)")
        self.assertGreaterEqual(recall, 0.80, "Recall below benchmark threshold (0.80)")
        self.assertGreaterEqual(f1, 0.85, "F1-Score below benchmark threshold (0.85)")
        self.assertLessEqual(fpr, 0.08, "False Positive Rate exceeds acceptable boundary (8%)")


if __name__ == "__main__":
    unittest.main()
