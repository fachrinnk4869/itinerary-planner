from pydantic import ValidationError
from unittest import IsolatedAsyncioTestCase
from schemas.finaltripplan import FinalTripPlan
from fastapi.testclient import TestClient
from app import app
# ================== Test Case ==================


class TestRecommendSchema(IsolatedAsyncioTestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_itinerary_success(self):
        # Given: request body sesuai itineraryQuery
        params = {
            "input": "Plan a romantic 4-day trip to Bali next month. Booking OK.",
            "auto_book": False
        }

        # When
        response = self.client.get("/itinerary", params=params)
        print("Raw Response:", response.text)

        # Then: status code OK
        self.assertEqual(response.status_code, 200)

        data = response.json()

        # Validate response using FinalTripPlan schema
        try:
            FinalTripPlan(**data)
        except ValidationError as e:
            self.fail(f"Response does not match FinalTripPlan schema:\n{e}")

        # Additional sanity checks
        self.assertIn("trip_title", data)
        self.assertIn("start_date", data)
        self.assertIn("end_date", data)
        self.assertIn("itinerary", data)
        self.assertIn("flights", data)
        self.assertIn("hotels", data)

        self.assertIsInstance(data["itinerary"], list)
        self.assertIsInstance(data["flights"], list)
        self.assertIsInstance(data["hotels"], list)

    def test_itinerary_missing_input(self):
        # Given: hanya auto_book, input tidak diberikan (atau empty)
        params = {
            "input": "",        # sengaja kosong
            "auto_book": "false"
        }

        # When
        response = self.client.get("/itinerary", params=params)
        print("Raw Response (missing input):", response.text)

        # Then: seharusnya gagal (422 Unprocessable Entity)
        self.assertEqual(response.status_code, 422)

    def test_itinerary_invalid_auto_book_type(self):
        # Given: auto_book salah tipe
        params = {
            "input": "Plan something",
            "auto_book": "notaboolean"    # salah tipe
        }

        # When
        response = self.client.get("/itinerary", params=params)
        print("Raw Response (invalid auto_book):", response.text)

        # Then
        self.assertEqual(response.status_code, 422)
