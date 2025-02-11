import { motion } from "framer-motion";

const Logo = () => {
  return (
    <motion.svg
      width="180"
      height="60"
      viewBox="0 0 300 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      initial={{ y: -10, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ type: "spring", stiffness: 100, damping: 10 }}
      whileHover={{ scale: 1.1 }}
    >
      <motion.g
        transform="translate(10,10)"
        animate={{ rotate: [0, -5, 5, 0] }}
        transition={{ repeat: Infinity, duration: 2, ease: "easeInOut" }}
      >
        <circle cx="20" cy="40" r="10" fill="#FF5733" />
        <rect x="17" y="50" width="6" height="30" fill="#FF5733" />
        <rect x="14" y="20" width="4" height="20" fill="#FF5733" />
        <rect x="18" y="20" width="4" height="20" fill="#FF5733" />
        <rect x="22" y="20" width="4" height="20" fill="#FF5733" />
        <rect x="26" y="20" width="4" height="20" fill="#FF5733" />
      </motion.g>

      <motion.text
        x="50"
        y="65"
        fontSize="40"
        fontWeight="bold"
        fill="#333"
        fontFamily="Arial, sans-serif"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5, duration: 1 }}
        whileHover={{ fill: "#FF5733" }}
      >
        Bite
        <tspan fill="#FF5733">Sync</tspan>
      </motion.text>
    </motion.svg>
  );
};

export default Logo;
