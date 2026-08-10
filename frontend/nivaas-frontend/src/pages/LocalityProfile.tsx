import { useParams } from "react-router-dom";

export default function LocalityProfile() {
    const { slug } = useParams();

    return (
        <div className="min-h-screen text-white px-6 py-20">
            <div className="mx-auto max-w-6xl">

                <h1 className="font-serif text-7xl mb-4 capitalize">
                    {slug?.replace("-", " ")}
                </h1>

                <p className="text-white/60 mb-12">
                    Locality Personality Profile
                </p>

                <div className="grid md:grid-cols-4 gap-6">

                    <div className="rounded-3xl bg-white/5 p-6">
                        <h3>Rent Score</h3>
                        <p className="text-4xl mt-2">87</p>
                    </div>

                    <div className="rounded-3xl bg-white/5 p-6">
                        <h3>Safety</h3>
                        <p className="text-4xl mt-2">91</p>
                    </div>

                    <div className="rounded-3xl bg-white/5 p-6">
                        <h3>Metro Access</h3>
                        <p className="text-4xl mt-2">84</p>
                    </div>

                    <div className="rounded-3xl bg-white/5 p-6">
                        <h3>Lifestyle</h3>
                        <p className="text-4xl mt-2">95</p>
                    </div>

                </div>

                <div className="mt-12 rounded-3xl bg-white/5 p-8">
                    <h2 className="font-serif text-3xl mb-4">
                        Personality
                    </h2>

                    <p className="text-white/70 leading-relaxed">
                        Koramangala is ambitious, energetic and social.
                        Perfect for young professionals seeking
                        cafes, coworking spaces and short commutes.
                    </p>
                </div>

            </div>
        </div>
    );
}
