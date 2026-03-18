"use client";

import { useState } from "react";
import "./ScanForm.css";

export default function ScanForm() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleScan = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const res = await fetch("http://localhost:8000/api/scan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url })
      });
      
      if (!res.ok) throw new Error("Failed to start scan");
      
      const data = await res.json();
      console.log("Scan started:", data);
      
      // Redirect to report progress view
      window.location.href = `/reports/${data.scan_id}`;
      
    } catch (err: any) {
      setError(err.message || "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="scan-form glass-panel" onSubmit={handleScan}>
      <div className="input-wrapper">
        <svg className="input-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        <input 
          type="url" 
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://example.com" 
          required
          className="url-input"
          disabled={loading}
        />
      </div>
      <button type="submit" className="btn-primary scan-btn" disabled={loading}>
        {loading ? (
          <span className="loader-spin"></span>
        ) : (
          <>Initialize Scan</>
        )}
      </button>
      
      {error && <p className="error-text">{error}</p>}
    </form>
  );
}
