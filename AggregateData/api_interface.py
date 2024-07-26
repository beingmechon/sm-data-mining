from abc import ABC, abstractmethod


class APIFetch(ABC):
    @abstractmethod
    def fetch_from_api(self):
        pass