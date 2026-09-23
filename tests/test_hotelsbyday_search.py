import unittest
from unittest.mock import patch
import scripts.hotelsbyday_search as hbd


class TestHotelsByDaySearch(unittest.TestCase):

    def test_clean_text(self):
        text = "<div>Aloft&nbsp;SFO   San Francisco,<br> CA</div>"
        cleaned = hbd._clean_text(text)
        self.assertEqual(cleaned, "Aloft SFO San Francisco, CA")

    def test_extract_hotel_cards(self):
        sample_html = """
        <div class="card-hotel" data-href="https://www.hotelsbyday.com/en/hotels/us/hotel-1">
          <div class="card-hotel-name">Aloft SFO San Francisco, CA 4.2 / 5</div>
          <div data-price="120.00" data-currency="USD"></div>
          <div>Day use room Work Friendly Pool Pass Parking</div>
          <div>9 AM - 5 PM</div>
          <div>Pay at property free cancellation</div>
          <div>earn up to 12.0 coins</div>
        </div></div></div></div></div>
        """
        hotels = hbd._extract_hotel_cards(sample_html)
        self.assertEqual(len(hotels), 1)
        hotel = hotels[0]
        self.assertEqual(hotel["name"], "Aloft SFO San Francisco, CA 4.2 / 5")
        self.assertEqual(hotel["rating"], 4.2)
        self.assertEqual(hotel["price"], 120.0)
        self.assertEqual(hotel["currency"], "USD")
        self.assertIn("Work Friendly", hotel["services"])
        self.assertEqual(hotel["time_slots"], ["9 AM - 5 PM"])
        self.assertEqual(hotel["cancellation"], "Pay at property free cancellation")
        self.assertEqual(hotel["loyalty_coins"], 12.0)

    @patch("scripts.hotelsbyday_search.fetch")
    def test_hotel_detail(self, mock_fetch):
        sample_body = """
        <html>
          <head>
            <title>M Social Hotel Times Square &quot;New York&quot;</title>
            <script type="application/ld+json">{"starRating": 4}</script>
          </head>
          <body>
            <div class="hd-room-name">King Room &nbsp; City View</div>
            <div class="hd-room-time">10 AM - 4 PM</div>
            <div data-price="199.00" data-rate-type="day_use"></div>
            <div class="hd-room-cancellation">Free cancellation</div>
          </body>
        </html>
        """
        mock_fetch.return_value = (200, sample_body, "https://www.hotelsbyday.com/test")

        result = hbd.hotel_detail("https://www.hotelsbyday.com/test")
        self.assertEqual(result["source"], "hotelsbyday-detail")
        self.assertEqual(result["stars"], 4)
        self.assertEqual(len(result["rooms"]), 1)
        room = result["rooms"][0]
        self.assertEqual(room["name"], "King Room City View")
        self.assertEqual(room["time_slot"], "10 AM - 4 PM")
        self.assertEqual(room["price"], 199.0)
        self.assertEqual(room["cancellation"], "Free cancellation")


if __name__ == "__main__":
    unittest.main()
