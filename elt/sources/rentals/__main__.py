from .client import RentalSourceClient
from .pipeline import RentalPipeline


def main():

    client = RentalSourceClient(
        "data/raw/rentals/Bangalore_rent.csv"
    )

    pipeline = RentalPipeline(client)

    pipeline.run()


if __name__ == "__main__":
    main()
