import axios from "axios";

export type NivBotResponse = {
    answer: string;
};

export type NivBotOptions = {
    mode?: "locality" | "recommendation";
    compareLocalities?: string[];
};

const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL ||
    "https://nivaas-backend.onrender.com";

export async function askNivBot(
    question: string,
    localityName: string = "",
    options: NivBotOptions = {}
): Promise<NivBotResponse> {
    try {
        const response = await axios.post<NivBotResponse>(
            `${API_BASE_URL}/nivbot/chat`,
            {
                question,
                locality_name: localityName,
                mode: options.mode ?? "locality",
                compare_names: options.compareLocalities ?? [],
            }
        );

        return response.data;
    } catch {
        throw new Error("Unable to reach the NIVAAS assistant.");
    }
}
