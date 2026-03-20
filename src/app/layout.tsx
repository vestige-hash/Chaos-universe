import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "JARVIS — Chaos Universe",
  description: "Advanced AI assistant powered by Chaos Universe",
};

// Next.js App Router requires default exports for layouts
// eslint-disable-next-line import/no-default-export
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full dark">
      <body className="min-h-full bg-black text-zinc-100 font-mono antialiased">
        {children}
      </body>
    </html>
  );
}
