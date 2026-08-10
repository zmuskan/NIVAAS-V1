"use client";

import { motion } from "framer-motion";

export default function IntroLogo() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 1 }}
      className="absolute inset-0 z-20 flex flex-col items-center justify-center"
    >
      <img
        src="/images/nivaas-logo.png"
        alt="Nivaas"
        className="w-52 md:w-72"
      />
    </motion.div>
  );
}
