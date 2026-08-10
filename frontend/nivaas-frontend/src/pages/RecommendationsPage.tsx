import { useEffect, useState } from "react";

import { getRecommendations } from "../api/recommend";

import RecommendationCard from "../components/recommendation/RecommendationCard";

export default function RecommendationsPage() {
    const [rows, setRows] = useState<any[]>([]);

    useEffect(() => {
        getRecommendations().then((data) => {
            setRows(data.recommendations);
        });
    }, []);

    return (
        <div>
            <h1>NIVAAS Recommendations</h1>

            {rows.map((item: any) => (
                <RecommendationCard
                    key={item.locality}
                    locality={item.locality}
                    score={item.score}
                />
            ))}
        </div>
    );
}
