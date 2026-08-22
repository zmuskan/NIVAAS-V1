import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function ExplorePage() {
    const navigate = useNavigate();

    const [localities, setLocalities] = useState<any[]>([]);
    const [search, setSearch] = useState("");

    useEffect(() => {
        fetch("https://nivaas-backend.onrender.com/localities")
            .then((res) => res.json())
            .then((data) => {
                console.log(data.items.slice(0, 20));
                setLocalities(data.items || []);
            })
            .catch((err) => {
                console.error("Failed to load localities:", err);
            });
    }, []);

    const filteredLocalities = localities.filter((item) =>
        item.locality
            .toLowerCase()
            .includes(search.toLowerCase())
    );

    return (
        <div className="p-8">
            <h1 className="text-3xl font-bold mb-6">
                Explore Bangalore Localities
            </h1>

            <input
                type="text"
                placeholder="Search locality..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="w-full rounded-2xl p-4 text-black"
            />

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {filteredLocalities.map((item) => (
                    <div
                        key={item.locality}
                        onClick={() =>
                            navigate(
                                `/locality/${encodeURIComponent(item.locality)}`
                            )
                        }
                        className="border rounded-xl p-4 shadow hover:shadow-lg transition cursor-pointer"
                    >
                        <h2 className="font-semibold text-lg mb-2">
                            {item.locality}
                        </h2>

                        <p>
                            <strong>Avg Rent:</strong> ₹{item.avg_rent}
                        </p>

                        <p>
                            <strong>Listings:</strong> {item.listing_count}
                        </p>

                        <p>
                            <strong>Score:</strong> {item.overall_score}
                        </p>
                    </div>
                ))}
            </div>
        </div>
    );
}
