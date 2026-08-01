from abc import ABC, abstractmethod


class RentalSourceClient(ABC):

    @abstractmethod
    def fetch(self):
        """Fetch raw rental listings."""
        raise NotImplementedError
