import unittest

from app import app


class PortalServicesTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_all_seven_pages_are_available(self):
        for path in ("/", "/compra", "/salario", "/temperatura", "/empresa", "/servicios", "/contacto"):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)

    def test_purchase_discount_threshold_and_no_discount(self):
        discounted = self.client.post("/compra", data={"cantidad": "5", "precio": "250"})
        self.assertIn(b"$1,250.00", discounted.data)
        self.assertIn(b"$125.00", discounted.data)
        self.assertIn(b"$1,125.00", discounted.data)

        no_discount = self.client.post("/compra", data={"cantidad": "4", "precio": "250"})
        self.assertIn(b"$1,000.00", no_discount.data)
        self.assertIn(b"$0.00", no_discount.data)

    def test_salary_with_overtime_and_without_overtime(self):
        overtime = self.client.post("/salario", data={"horas": "45", "pago_hora": "100"})
        self.assertIn(b"$5,000.00", overtime.data)

        regular = self.client.post("/salario", data={"horas": "40", "pago_hora": "100"})
        self.assertIn(b"$4,000.00", regular.data)
        self.assertIn(b"0 h", regular.data)

    def test_temperature_conversion(self):
        response = self.client.post("/temperatura", data={"celsius": "25"})
        self.assertIn(b"77", response.data)
        self.assertIn(b"298.15", response.data)

    def test_invalid_values_are_reported_in_the_page(self):
        response = self.client.post("/temperatura", data={"celsius": "-300"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("cero absoluto".encode(), response.data)


if __name__ == "__main__":
    unittest.main()
