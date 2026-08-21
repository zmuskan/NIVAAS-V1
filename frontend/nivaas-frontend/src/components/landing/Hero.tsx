import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useNavigate } from "react-router-dom";

const Hero = () => {
    const navigate = useNavigate();
    const [showIntro, setShowIntro] = useState(true);

    useEffect(() => {
        const timer = setTimeout(() => {
            setShowIntro(false);
        }, 2000);

        return () => clearTimeout(timer);
    }, []);

    return (
        <section className="relative z-10 flex min-h-screen items-center justify-center px-6">
            <div className="mx-auto flex w-full max-w-[800px] flex-col items-center text-center">

                <AnimatePresence mode="wait">

                    {showIntro ? (
                        <motion.div
                            key="intro"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            transition={{ duration: 0.8 }}
                        >
                            <h1
                                className="text-4xl md:text-5xl font-light tracking-[0.06em] text-white"
                            >
                                NIVAAS
                            </h1>

                            <p className="mt-3 text-base md:text-lg text-white/80 font-light">
                                Find where you belong
                            </p>
                        </motion.div>
                    ) : (
                        <motion.div
                            key="hero"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{ duration: 1 }}
                        >
                            <h1 className="flex flex-col text-white text-3xl md:text-4xl font-medium leading-[1.05]">
                                <span>Find where you belong.</span>
                                <span>Five questions.</span>
                                <span>One neighbourhood that feels like home.</span>
                            </h1>

                            <p className="mt-6 text-base md:text-lg text-white/75 font-light">
                                Elegant, quick, and grounded in real inventory.
                            </p>

                            <div className="mt-8">
                                <button
                                    onClick={() => navigate("/questionnaire")}
                                    className="rounded-full border border-white/20 bg-black/40 backdrop-blur-md text-white hover:bg-black/60 transition-all px-10 py-4"
                                >
                                    Begin Journey
                                </button>
                            </div>
                        </motion.div>
                    )}

                </AnimatePresence>
            </div>
        </section>
    );
};

export default Hero;
