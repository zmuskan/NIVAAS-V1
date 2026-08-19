type Props = {
    locality: string;
    score: number;
    reasons: string[];
};

export default function RecommendationCard({
    locality,
    score,
    reasons,
}: Props) {

    return (
        <div
            className="
                rounded-3xl
                border
                border-white/10
                bg-white/5
                backdrop-blur-xl
                p-6
                mb-4
            "
        >
            <h2 className="text-3xl font-semibold">
                {locality}
            </h2>

            <p className="mt-2 text-emerald-300">
                Match Score: {score}
            </p>

            <div className="mt-4 space-y-2">
                {reasons.map((reason) => (
                    <p key={reason}>
                        • {reason}
                    </p>
                ))}
            </div>
        </div>
    );
}
