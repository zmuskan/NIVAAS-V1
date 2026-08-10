import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useNavigate } from "react-router-dom";

const Hero = () => {
    const navigate = useNavigate();
    const [name, setName] = useState("");
    const [showIntro, setShowIntro] = useState(true);

    useEffect(() => {
        const timer = setTimeout(() => {
            setShowIntro(false);
        }, 2000);

        return () => clearTimeout(timer);
    }, []);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        localStorage.setItem("nivaas_name", name);

        navigate("/questionnaire");
    };

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
                                className="
                                    text-7xl
                                    md:text-9xl
                                    font-light
                                    tracking-[0.08em]
                                    text-white
                                "
                            >
                                NIVAAS
                            </h1>

                            <p
                                className="
                                    mt-4
                                    text-xl
                                    md:text-2xl
                                    text-white/80
                                    font-light
                                "
                            >
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
                            <h1 className="flex flex-col text-white text-[2.75rem] md:text-[4.5rem] font-medium leading-[1.05]">
                                <span>Every locality</span>
                                <span>has a personality.</span>
                                <span>
                                    Let's find
                                    <span className="text-[#D6B46C]"> yours.</span>
                                </span>
                            </h1>

                            <p className="mt-8 text-lg text-white/75">
                                A couple of questions.
                                <br />
                                Then we'll do the hard part.
                            </p>

                            <div className="mt-10">
                                <button
                                    onClick={() => navigate("/questionnaire")}
                                    className="rounded-full bg-white text-black px-8 py-4"
                                >
                                    Get Started
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
