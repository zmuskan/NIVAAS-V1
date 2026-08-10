type Props = {
    locality: string;
    score: number;
};

export default function RecommendationCard({
    locality,
}: Props) {
    return (
        <div
            style={{
                border: "1px solid #333",
                borderRadius: "16px",
                padding: "20px",
                marginBottom: "12px",
            }}
        >
            <h2>{locality} ⭐</h2>

            <p>Good rental inventory</p>

            <p>Affordable for your budget</p>

            <button>
                Explore Area
            </button>
        </div>
    );
}
