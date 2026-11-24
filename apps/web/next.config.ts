import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // Le package partagé expose des fichiers TypeScript sources.
  transpilePackages: ["@safeclick/shared"],
};

export default nextConfig;
