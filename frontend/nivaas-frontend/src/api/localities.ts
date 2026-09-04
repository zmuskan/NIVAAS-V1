import axios from "axios";

export async function getLocalities() {
    const response = await axios.get(
        "http://localhost:8000/localities"
    );

    return response.data.items;
}
