export default function HeroVideo() {
    return (
        <div className="absolute inset-0 -z-10 overflow-hidden">
            <video
                autoPlay
                muted
                loop
                playsInline
                className="absolute inset-0 h-full w-full object-cover"
            >
                <source src="/videos/hero-bg.mp4" type="video/mp4" />
            </video>

            <div className="absolute inset-0 bg-gradient-to-b from-black/50 via-black/55 to-black/70" />
        </div>
    );
}
