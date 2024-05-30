import logging
import os
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv

from src.db_store.store import Store
from src.providers.base import Provider
from src.utils.logger import get_logger

load_dotenv()

BASE_URL = "https://customer.api.soundcharts.com/api/v2"
API_KEY = os.getenv("SOUNDCHARTS_API_KEY", "soundcharts")
APP_ID = os.getenv("SOUNDCHARTS_API_ID", "soundcharts")



class SoundCharts(Provider):
    def __init__(self, log: logging.Logger):
        super().__init__(log)
        self.raw_data: List[Dict[str, Any]] = []
        self.transformed_data: List[Dict[str, Any]] = []

    def _retrieve_data(self, platform: str, metricType: str, params) -> List[dict[str, Any]]:
        response = requests.get(url=f"{BASE_URL}/top-artist/{platform}/{metricType}", headers={"x-app-id": APP_ID, "x-api-key": API_KEY}, params=params)
        response.raise_for_status()
        try:
            data = response.json()
            data = data.get('items', [])
        except requests.exceptions.RequestException as req_exception:
            self.log.error(f"{req_exception}")
        except Exception as exc:
            self.log.error(f"{exc}")

        self.raw_data = data

    def retrieve_data(self):
        self._retrieve_data(platform="spotify", metricType="monthly_listeners", params={"sortBy": "total", "period": "month"})

    def transform_data(self):
        for row in self.raw_data:
            artist = row.get('artist')
            artist_name = artist.get("name")
            if artist_name is None:
                continue
            self.transformed_data.append({"artist": artist_name})


if __name__ == '__main__':
    log = get_logger("last fm", logging.INFO)
    store = Store()
    sc = SoundCharts(log)
    data = sc.retrieve_data(platform="spotify", metricType="monthly_listeners", params={"sortBy": "total", "period": "month"})
    transformed_data = sc.transform_data(data)

    store.store(transformed_data, table="artists")
