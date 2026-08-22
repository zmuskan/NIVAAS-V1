const API_BASE = "https://nivaas-backend.onrender.com";

export async function getLocality(name: string) {
    const response = await fetch(
        `${API_BASE}/localities/${encodeURIComponent(name)}`
    );

    return response.json();
}
