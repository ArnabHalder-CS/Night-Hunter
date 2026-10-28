import unittest
from modules.phishing.url_analyzer import PhishingAnalyzer

class TestUrlPhishingAdvanced(unittest.TestCase):
    def test_official_domains_are_benign(self):
        """Official corporate domains must be 100% benign with 0 risk score."""
        official_urls = [
            "https://google.com",
            "https://www.paypal.com",
            "https://github.com",
            "https://apple.com"
        ]
        for url in official_urls:
            rep = PhishingAnalyzer(url, fetch_content=False).analyze()
            self.assertEqual(rep["risk_score"], 0, f"Failed for {url}: score was {rep['risk_score']}")
            self.assertIn("BENIGN", rep["risk_level"].upper(), f"Failed for {url}: level was {rep['risk_level']}")
            self.assertTrue(rep["is_verified_official"], f"Expected verified official for {url}")

    def test_combosquatting_detected_as_critical(self):
        """Unregistered brand domains must be flagged as CRITICAL / HIGH."""
        phish_urls = [
            "https://paypal-security-update.com/verify",
            "https://chase-bank-verify.net/signin",
            "https://netflix-billing-alert.org/login"
        ]
        for url in phish_urls:
            rep = PhishingAnalyzer(url, fetch_content=False).analyze()
            self.assertGreaterEqual(rep["risk_score"], 50, f"Expected high score for {url}, got {rep['risk_score']}")
            self.assertIn(rep["risk_level"], ["HIGH", "CRITICAL"], f"Expected HIGH/CRITICAL for {url}, got {rep['risk_level']}")
            self.assertIsNotNone(rep["ethical_hacking_profile"]["targeted_brand"])

    def test_leetspeak_typosquatting_detected(self):
        """Visual character substitutions must be detected as typosquatting."""
        typo_urls = [
            "https://paypa1-security.com",
            "https://micros0ft-login.xyz",
            "https://arnazon-orders.net"
        ]
        for url in typo_urls:
            rep = PhishingAnalyzer(url, fetch_content=False).analyze()
            self.assertGreaterEqual(rep["risk_score"], 60, f"Expected >=60 for {url}, got {rep['risk_score']}")
            self.assertEqual(rep["risk_level"], "CRITICAL")
            self.assertTrue(len(rep["ethical_hacking_profile"]["mitre_techniques"]) > 0)

    def test_fuzzy_typosquatting_detected(self):
        """Fuzzy typosquatting (Flipkert, Yotube, Aamazon) must be flagged as CRITICAL."""
        typos = [
            ("www.FLipkert.com", "FLIPKART"),
            ("www.yotube.com", "YOUTUBE"),
            ("www.Aamazon.com", "AMAZON"),
        ]
        for url, expected_brand in typos:
            rep = PhishingAnalyzer(url, fetch_content=False).analyze()
            self.assertGreaterEqual(rep["risk_score"], 60, f"Expected >=60 for {url}, got {rep['risk_score']}")
            self.assertEqual(rep["risk_level"], "CRITICAL", f"Expected CRITICAL for {url}, got {rep['risk_level']}")
            self.assertEqual(rep["ethical_hacking_profile"]["targeted_brand"], expected_brand)

    def test_mitre_and_soc_profile_generated(self):
        """Ethical hacking profile must populate MITRE techniques and SOC playbooks."""
        rep = PhishingAnalyzer("https://micros0ft-login.xyz/account", fetch_content=False).analyze()
        profile = rep.get("ethical_hacking_profile", {})
        self.assertIn("Initial Access (TA0001)", profile.get("mitre_tactics", []))
        self.assertTrue(any(t["id"] == "T1566.002" for t in profile.get("mitre_techniques", [])))
        self.assertTrue(len(profile.get("soc_remediation", [])) >= 2)

if __name__ == "__main__":
    unittest.main()
