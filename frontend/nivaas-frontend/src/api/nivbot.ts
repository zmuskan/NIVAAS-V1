import axios from "axios";

export type NivBotResponse = {
    answer: string;
};

const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL ||
    "https://nivaas-backend.onrender.com";

export async function askNivBot(
    question: string,
    localityName: string = ""
): Promise<NivBotResponse> {
    try {
        const response = await axios.post<NivBotResponse>(
            `${API_BASE_URL}/nivbot/chat`,
            {
                question,
                locality_name: localityName,
            }
        );

        console.log("NIVBOT SUCCESS", response.data);

        return response.data;
    } catch (error) {
        console.error("NIVBOT FAILED", error);
        throw error;
    }
}
