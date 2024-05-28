import argparse
import logging
from time import sleep
from typing import Any, Dict, List, Optional

import requests

from src.api import ApiFactory
from src.utils.logger import get_logger

BASE_URL = "http://ws.audioscrobbler.com/2.0"


class MusicDiscoverApi(ApiFactory):
    """
    To retrieve music related data from lastfm

    Attributes
    """

    def __init__(self, api_key: str, logger: logging.Logger):
        """

        Args:
            api_key (str): A Last.fm API key.
            logger (logging.Logger): A logger, for streaming logs to console.
        """
        super().__init__(logger)
        self.api_key = api_key

    def _get_top_artists(self, limit: int = 50, page: int = 1) -> List[Dict[str, str]]:
        """
        Gathers top artist according to the lastfm
        Args:
            limit (int): The number of results to fetch per page. Defaults to 50.
            page (int): The page number to fetch. Defaults to first page.

        Returns:

        """
        top_artists = []

        try:
            res = requests.get(
                f"{BASE_URL}/?method=chart.gettopartists&api_key={self.api_key}&limit={limit}&page={page}&format=json")
            res.raise_for_status()

            data = res.json().get('artists', {})
            artist_list = data['artist']
            for artist in artist_list:
                top_artists.append({
                    "name": artist.get("name"),
                    "playcount": artist.get("playcount"),
                    "listeners": artist.get("listeners")
                })
        except requests.exceptions.RequestException as err:
            self.log.error(f"Could not fetch top artists: {err}")
        except Exception as exc:
            self.log.error(exc)
        return top_artists

    def _get_top_artists_in(self, country: str, limit: int = 50, page: int = 1) -> List[Dict[str, Any]]:
        """
        Top artists in the specified country

        Args:
            country (str): A country name, as defined by the ISO 3166-1 country names standard
            limit:
            page:

        Returns:

        """
        top_artists = []
        try:
            sleep(15)
            res = requests.get(
                f"{BASE_URL}/?method=geo.gettopartists&country={country}&api_key={self.api_key}&limit={limit}&page={page}&format=json")
            res.raise_for_status()

            data = res.json().get('topartists', {})
            artist_list = data['artist']
            for artist in artist_list:
                top_artists.append({
                    "name": artist.get("name"),
                    "listeners": artist.get("listeners"),
                    "country": country
                })
        except requests.exceptions.RequestException as err:
            self.log.error(f"Could not fetch top artists: {err}")
        except Exception as exc:
            self.log.error(exc)
        return top_artists

    def retrieve_data(self, countries: Optional[List[str]] = None):
        worldwide_top_artists = self._get_top_artists()

        if countries:
            top_artists_in_country = {}
            for country in countries:
                geo_top_artists = self._get_top_artists_in(country)
                top_artists_in_country[country] = geo_top_artists




if __name__ == "__main__":
    log = get_logger("Music API Key - Logger", level=10)
    parser = argparse.ArgumentParser()
    parser.add_argument("--api_key")
    args = parser.parse_args()

    music = MusicDiscoverApi(api_key=args.api_key, logger=log)
    music.retrieve_data()
    pass
