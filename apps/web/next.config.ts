import type { NextConfig } from "next";

const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

const connections = [`'self'`, apiUrl];
if (process.env.NODE_ENV !== "production") {
  connections.push("ws://localhost:3000", "ws://127.0.0.1:3000");
}

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // Permet d'ouvrir le serveur de développement via 127.0.0.1 aussi bien que localhost.
  allowedDevOrigins: ["127.0.0.1"],
  output: "standalone",
  // Le package partagé expose des fichiers TypeScript sources.
  transpilePackages: ["@safeclick/shared"],
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          { key: "X-Content-Type-Options", value: "nosniff" },
          { key: "Referrer-Policy", value: "no-referrer" },
          { key: "X-Frame-Options", value: "DENY" },
          {
            key: "Permissions-Policy",
            value: "camera=(), microphone=(), geolocation=()",
          },
          {
            key: "Content-Security-Policy",
            value: [
              "default-src 'self'",
              "script-src 'self' 'unsafe-inline'",
              "style-src 'self' 'unsafe-inline'",
              "img-src 'self' data: https:",
              "font-src 'self' data:",
              `connect-src ${connections.join(" ")}`,
              "frame-ancestors 'none'",
              "base-uri 'self'",
              "form-action 'self'",
            ].join("; "),
          },
        ],
      },
    ];
  },
};

export default nextConfig;
