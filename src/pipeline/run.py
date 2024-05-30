from src.db_store.store import Store
from src.providers.base import Provider


class Pipeline:
    def __init__(self, provider: Provider, store: Store):
        self.raw_data = []
        self.transformed_data = []
        self.provider = provider
        self.store = store

    def run(self):
        self.provider.retrieve_data()
        self.provider.transform_data()
        self.store.store(self.provider.transformed_data, "artists")