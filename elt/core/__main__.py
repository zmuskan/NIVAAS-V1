from .pipeline import CorePipeline


def main():
    pipeline = CorePipeline()
    stats = pipeline.run()
    stats.print_summary()


if __name__ == "__main__":
    main()
