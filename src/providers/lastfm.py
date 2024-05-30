import logging
import os
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv

from src.db_store.store import Store
from src.providers.base import Provider
from src.utils.logger import get_logger

load_dotenv()

BASE_URL = "http://ws.audioscrobbler.com/2.0"
API_KEY = os.getenv("LASTFM_API_KEY")


class LastFm(Provider):
    def __init__(self, log: logging.Logger):
        super().__init__(log)
        self.raw_data: List[Dict[str, Any]] = []
        self.transformed_data: List[Dict[str, Any]] = []


    def _retrieve_data(self, params) -> List[Dict[str, Any]]:
        """

        Args:
            **kwargs:

        Returns:

        """

        response = requests.get(url=BASE_URL, params=params)
        response.raise_for_status()

        try:
            data = response.json()
            self.raw_data = data.get('artists', {}).get('artist', [])

        except requests.exceptions.RequestException as req_exception:
            self.log.error(f"{req_exception}")
        except Exception as exc:
            self.log.error(f"{exc}")

        return self.raw_data

    def retrieve_data(self):
        self._retrieve_data(params={"method": "chart.gettopartists", "api_key": API_KEY, "format": "json"})

    def transform_data(self):
        for row in self.raw_data:
            artist_name = row.get('name')
            if artist_name is None:
                continue
            self.transformed_data.append({
                "artist": artist_name
            })


if __name__ == '__main__':
    log = get_logger("last fm", logging.INFO)
    store = Store()
    lastfm = LastFm(log)
    lastfm.retrieve_data()
    lastfm.transform_data()
    store.store(lastfm.transformed_data, "artists")
