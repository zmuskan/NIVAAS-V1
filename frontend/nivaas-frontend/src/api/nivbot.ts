import axios from "axios";

export type NivBotResponse = {
    answer: string;
};

export async function askNivBot(question: string): Promise<NivBotResponse> {
    const response = await axios.post<NivBotResponse>(
        "http://localhost:8000/nivbot/chat",
        {
            question,
            locality_context: "",
        },
    );

    return response.data;
}
