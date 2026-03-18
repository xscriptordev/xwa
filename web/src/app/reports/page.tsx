"use client";

import { useEffect, useState } from "react";
import "./reports.css";

interface ReportSummary {
  id: number;
  target_url: string;
  urls_found: number;
  broken_links_count: number;
  missing_security_headers: number;
  is_ssl_valid: boolean;
  timestamp: string;
}

export default function ReportsPage() {
  const [reports, setReports] = useState<ReportSummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/api/reports")
      .then(r => r.json())
      .then(data => {
        setReports(data || []);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to load reports", err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="reports-page fade-in">
      <header className="page-header">
        <h1 className="title">Scan History</h1>
        <p className="subtitle">Review your past website analyses</p>
      </header>
      
      {loading ? (
        <div className="loader-container">
          <span className="loader-spin dark-loader"></span>
        </div>
      ) : reports.length === 0 ? (
        <div className="glass-panel empty-state">
          <p>No scans found. Start by running a new analysis.</p>
        </div>
      ) : (
        <div className="glass-panel table-container">
          <table className="reports-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Target URL</th>
                <th>Date</th>
                <th>Sitemap URLs</th>
                <th>Issues</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {reports.map((r) => (
                <tr key={r.id}>
                  <td>#{r.id}</td>
                  <td className="font-medium">{r.target_url}</td>
                  <td className="text-muted">{new Date(r.timestamp).toLocaleString()}</td>
                  <td>{r.urls_found}</td>
                  <td>
                    {r.broken_links_count > 0 ? (
                      <span className="badge danger">{r.broken_links_count} Broken Links</span>
                    ) : (
                      <span className="badge success">0 Broken</span>
                    )}
                    {!r.is_ssl_valid && (
                      <span className="badge warning">SSL Invalid</span>
                    )}
                  </td>
                  <td>
                    <a href={`/reports/${r.id}`} className="view-btn">View Details</a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
