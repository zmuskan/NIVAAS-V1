from scrapers.core.loader import DatabaseLoader
from scrapers.core.osm_scraper import OSMScraper

QUERY = """
[out:json][timeout:120];

area["name"="Bengaluru"]->.searchArea;

(
node["railway"="station"](area.searchArea);
);

out body;
"""

scraper = OSMScraper(QUERY)

stations = scraper.fetch()

loader = DatabaseLoader()

count = 0

for station in stations:

    tags = station.get("tags", {})

    loader.insert_amenity(
        osm_type=station["type"],
        osm_id=station["id"],
        amenity_type="metro",
        name=tags.get("name"),
        lat=station["lat"],
        lon=station["lon"],
    )

    count += 1

loader.commit()
loader.close()

print(f"Imported {count} metro stations.")
