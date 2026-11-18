import unittest
from modules.validation import normalize_host, validate_port, validate_https_url


class ValidationTests(unittest.TestCase):
    def test_domain_normalization(self):
        self.assertEqual(normalize_host("Example.COM."), "example.com")

    def test_idna_domain(self):
        self.assertTrue(normalize_host("مثال.ایران").startswith("xn--"))

    def test_reject_bad_domain(self):
        for value in ("", "bad host", "-bad.example", "localhost", "example..com"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                normalize_host(value)

    def test_port_bounds(self):
        self.assertEqual(validate_port("443"), 443)
        for value in ("0", "65536", "abc"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_port(value)

    def test_reject_unsafe_urls(self):
        for value in ("http://example.com", "https://user:pass@example.com", "https://example.com:8443", "https://127.0.0.1"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_https_url(value)


if __name__ == "__main__":
    unittest.main()
