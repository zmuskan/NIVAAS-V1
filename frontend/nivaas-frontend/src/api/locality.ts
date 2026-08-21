const API_BASE = "http://127.0.0.1:8000";

export async function getLocality(name: string) {
    const response = await fetch(
        `${API_BASE}/locality/${encodeURIComponent(name)}`
    );

    return response.json();
}
