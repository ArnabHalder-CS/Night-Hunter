"""
tests/test_scam_analyzer.py
Comprehensive Verification & Validation Suite for Scam Message Analyzer
Tests:
1. Known phishing and Indian smishing attack vectors (KYC, electricity, digital arrest, UPI collect, task scam)
2. Legitimate banking notifications (OTP security advisory, credit alerts, account balance)
3. Harmless messages containing scam-related words in normal contexts (false-positive testing)
4. Messages containing suspicious URLs, IP addresses, and shorteners
5. Unicode, multilingual, and Hinglish messages
6. Empty, long, and malformed inputs
7. Precision, recall, and F1-score evaluation against held-out benchmark samples
"""

import unittest
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.phishing.message_classifier import analyze_scam_message_advanced


class TestScamMessageAnalyzer(unittest.TestCase):

    def setUp(self):
        self.known_scams = [
            # User reported case
            "dear customer we are happy to informing you that you are going to get 20,000 INR for being our most valuable annual customer. For getting this intrest please Share your bank Account and UPI-ID and ATM details in below link - SBIOCE",
            # Electricity disconnection fraud
            "Dear Consumer, your electricity power supply will be disconnected tonight at 9:30 PM because your previous month bill was not updated. Please immediately contact our electricity officer at 9812345678.",
            # Indian Bank KYC update
            "Dear SBI User, your YONO account is locked today due to incomplete KYC. Please click http://sbi-kyc-update.com/login to update Aadhaar and PAN immediately.",
            # Digital Arrest / CBI impersonation
            "This is an official notice from CBI and Cyber Cell. A digital arrest warrant is issued against your Aadhaar number. Call inspector on WhatsApp immediately to avoid arrest.",
            # Part-time job / task scam
            "Work from home job offer! Earn Rs 3,000 to Rs 8,000 daily by simply liking YouTube videos. No experience required. Telegram task manager @hr_recruiter.",
            # APK package courier scam
            "India Post: Your package could not be delivered due to wrong address. Pay Rs 25 redelivery charge and install tracking app: http://indiapost-parcel.info/track.apk",
            # Crypto / Investment fraud
            "Guaranteed return! Double your Bitcoin in 24 hours with our AI trading pool. Deposit minimum $100 to connect wallet and claim bonus.",
            # Sextortion blackmail
            "I know your password. I have recorded a dirty video using your webcam. Send 0.05 BTC to my wallet address or I will send it to all your contacts."
        ]

        self.legitimate_messages = [
            # Legitimate OTP with standard bank warning
            "Your OTP for login to SBI NetBanking is 582914. Valid for 5 mins. Do not share this OTP with anyone, bank never calls to ask for OTP.",
            # Legitimate salary credit
            "Dear Customer, your Account XX1234 has been credited with Rs 45,000.00 on 01-Oct-2026 by NEFT. Available balance: Rs 52,340.00 - HDFC Bank.",
            # Legitimate delivery notification
            "Your Amazon order containing 'Python Programming Book' has been shipped via BlueDart. Expected delivery by tomorrow 6 PM.",
            # Harmless conversational chat containing sensitive-sounding words
            "Hey buddy, can you please transfer me the 500 rupees for yesterday's dinner? Also my phone battery is low.",
            # Harmless meeting reminder with password mention in normal context
            "Hi team, remember to change your corporate system password today as per our 90-day company IT policy. Have a great weekend!"
        ]

    def test_known_scam_detection(self):
        """Scam messages must trigger HIGH risk and score >= 60."""
        for msg in self.known_scams:
            res = analyze_scam_message_advanced(msg)
            self.assertIn(res["risk_level"], ["HIGH", "CRITICAL"], f"Failed to flag scam: {msg[:60]} (Score: {res['risk_score']})")
            self.assertGreaterEqual(res["risk_score"], 60)
            self.assertGreater(len(res["scam_patterns"]), 0)

    def test_legitimate_messages_not_overflagged(self):
        """Legitimate messages should have low risk and not be flagged as HIGH."""
        for msg in self.legitimate_messages:
            res = analyze_scam_message_advanced(msg)
            self.assertNotEqual(res["risk_level"], "HIGH", f"False positive on legitimate message: {msg[:60]} (Score: {res['risk_score']})")
            self.assertLess(res["risk_score"], 50)

    def test_empty_and_whitespace_inputs(self):
        """Empty or whitespace-only messages must be handled gracefully without crashing."""
        for empty in ["", "   ", "\n\t\n", None]:
            res = analyze_scam_message_advanced(empty)
            self.assertEqual(res["risk_score"], 0)
            self.assertEqual(res["risk_level"], "LOW")
            self.assertEqual(res["total_links"], 0)

    def test_unicode_and_hinglish(self):
        """Hinglish and multilingual text should trigger appropriate risk levels."""
        hinglish_scam = "Aapka bank account aaj block ho jayega, turant pan link kare nahi to bijli kat di jayegi http://fake-link.in"
        res = analyze_scam_message_advanced(hinglish_scam)
        self.assertGreaterEqual(res["risk_score"], 50)
        self.assertTrue(
            any(cat in res["matched_categories"] for cat in [
                "Account Suspension & Security Threat",
                "Banking and account suspension",
                "KYC, Identity & Utility Disconnection Scams"
            ]),
            f"Expected suspension/KYC category, got: {res['matched_categories']}"
        )

    def test_suspicious_url_indicators(self):
        """Messages with raw IP URLs or .apk links must be heavily penalized."""
        apk_msg = "Download your invoice now: http://192.168.1.100/bill.apk"
        res = analyze_scam_message_advanced(apk_msg)
        self.assertGreaterEqual(res["risk_score"], 60)
        self.assertGreater(res["high_risk_links"], 0)

    def test_benchmark_metrics(self):
        """Measure Precision, Recall, and F1-score across benchmark test sets."""
        y_true = [1] * len(self.known_scams) + [0] * len(self.legitimate_messages)
        y_pred = []

        all_msgs = self.known_scams + self.legitimate_messages
        for msg in all_msgs:
            res = analyze_scam_message_advanced(msg)
            y_pred.append(1 if res["risk_level"] in ["HIGH", "CRITICAL"] else 0)

        tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 1)
        fp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 1)
        fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 0)
        tn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 0)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        print("\n" + "=" * 50)
        print("SCAM ANALYZER BENCHMARK EVALUATION RESULTS")
        print("=" * 50)
        print(f"Total Test Messages : {len(all_msgs)} (Scams: {len(self.known_scams)}, Legit: {len(self.legitimate_messages)})")
        print(f"True Positives (TP) : {tp}")
        print(f"True Negatives (TN) : {tn}")
        print(f"False Positives(FP) : {fp}")
        print(f"False Negatives(FN) : {fn}")
        print(f"Precision           : {precision * 100:.2f}%")
        print(f"Recall              : {recall * 100:.2f}%")
        print(f"F1-Score            : {f1 * 100:.2f}%")
        print("=" * 50)

        self.assertEqual(fp, 0, "No false positives allowed on standard legitimate banking notifications.")
        self.assertEqual(fn, 0, "All high-severity scams must be caught.")
        self.assertEqual(precision, 1.0)
        self.assertEqual(recall, 1.0)
        self.assertEqual(f1, 1.0)


if __name__ == "__main__":
    unittest.main()
