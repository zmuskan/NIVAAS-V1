import axios from "axios";

const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL ||
    "https://nivaas-backend.onrender.com";

export async function getLocalities() {
    const response = await axios.get(
        `${API_BASE_URL}/localities`
    );

    return response.data.items;
}
