import csv
from pathlib import Path


class RentalSourceClient:

    def __init__(self, path: str):
        self.path = Path(path)

    def fetch(self):

        with self.path.open(
            mode="r",
            encoding="utf-8",
            newline=""
        ) as file:

            return list(csv.DictReader(file))
