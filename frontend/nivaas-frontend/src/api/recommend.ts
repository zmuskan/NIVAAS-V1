const API_BASE = "http://127.0.0.1:8000";

export async function getRecommendations() {
    const response = await fetch(
        `${API_BASE}/recommend`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                rent_weight: 0.5,
                metro_weight: 0.3,
                property_weight: 0.2,
            }),
        }
    );

    return response.json();
}
