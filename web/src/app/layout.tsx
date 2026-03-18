import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "xwa - Web Analysis Dashboard",
  description: "Advanced SEO, Sitemap, and Security Analysis Tool.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <div className="app-container">
          <nav className="navbar">
            <div className="nav-brand">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ color: "var(--accent-color)" }}>
                <path d="M2 12h4l3-9 5 18 3-9h5" />
              </svg>
              xwa
            </div>
            <div className="nav-links">
              <a href="/" className="nav-link" data-active="true">New Scan</a>
              <a href="/reports" className="nav-link">Reports</a>
              <a href="/settings" className="nav-link">Settings</a>
            </div>
          </nav>
          
          <main className="main-content">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
