from abc import ABC, abstractmethod
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


class BaseScraper(ABC):

    def run(self):

        logger.info(f"Starting {self.__class__.__name__}")

        data = self.extract()

        data = self.transform(data)

        self.load(data)

        logger.info("Completed")

    @abstractmethod
    def extract(self):
        ...

    @abstractmethod
    def transform(self, data):
        ...

    @abstractmethod
    def load(self, data):
        ...
