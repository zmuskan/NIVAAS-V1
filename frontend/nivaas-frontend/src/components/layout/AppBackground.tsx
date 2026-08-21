export default function AppBackground() {
    return (
        <div className="fixed inset-0 -z-10 overflow-hidden">
            <div className="absolute inset-0 bg-[#050505]" />

            <div className="absolute left-1/4 top-1/3 h-96 w-96 rounded-full bg-amber-500/10 blur-3xl" />

            <div className="absolute right-1/4 bottom-1/3 h-96 w-96 rounded-full bg-emerald-500/10 blur-3xl" />
        </div>
    );
}
