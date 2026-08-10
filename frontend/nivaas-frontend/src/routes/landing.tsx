import Hero from "@/components/landing/Hero";
import HeroVideo from "@/components/landing/HeroVideo";

export default function Landing() {
    return (
        <main className="absolute inset-0 h-full w-full object-cover">
            <HeroVideo />
            <Hero />
        </main>
    );
}
