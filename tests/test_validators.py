import unittest
from core.validators import safe_host

class TestValidators(unittest.TestCase):
    def test_valid_hostnames_and_ips(self):
        self.assertEqual(safe_host("google.com"), "google.com")
        self.assertEqual(safe_host("192.168.1.1"), "192.168.1.1")
        self.assertEqual(safe_host("https://scanme.nmap.org/index.html"), "scanme.nmap.org")
        self.assertEqual(safe_host("sub.domain.example.co.uk"), "sub.domain.example.co.uk")
        self.assertEqual(safe_host("example.com:8080"), "example.com")
        self.assertEqual(safe_host("127.0.0.1"), "127.0.0.1")

    def test_hostile_option_injection_rejected(self):
        self.assertEqual(safe_host("-f"), "")
        self.assertEqual(safe_host("--script=http-vuln"), "")
        self.assertEqual(safe_host("-sV"), "")
        self.assertEqual(safe_host("-oN /tmp/pwn"), "")
        self.assertEqual(safe_host("192.168.1.1; rm -rf /"), "")
        self.assertEqual(safe_host("example.com && whoami"), "")
        self.assertEqual(safe_host(""), "")
        self.assertEqual(safe_host(None), "")

if __name__ == "__main__":
    unittest.main()
