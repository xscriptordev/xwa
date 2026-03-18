"use client";

import { useEffect, useState } from "react";
import "./ReportDashboard.css";

interface ScanReport {
  target_url: string;
  scan_timestamp: string;
  seo: any;
  sitemap: any;
  security: any;
}

export default function ReportDashboard({ scanId }: { scanId: string }) {
  const [status, setStatus] = useState<string>("Connecting to engine...");
  const [isCompleted, setIsCompleted] = useState<boolean>(false);
  const [reportData, setReportData] = useState<ScanReport | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Connect to SSE Endpoint
    const es = new EventSource(`http://localhost:8000/api/progress/${scanId}`);

    es.onmessage = (event) => {
      const newStatus = event.data;
      setStatus(newStatus);
      
      if (newStatus.includes("Completed")) {
        setIsCompleted(true);
        es.close();
      } else if (newStatus.includes("Error")) {
        setError(newStatus);
        es.close();
      }
    };

    es.onerror = (err) => {
      console.error("SSE Error:", err);
      // Sometimes it fails immediately if already finished, so we just attempt to fetch
      setIsCompleted(true);
      es.close();
    };

    return () => {
      es.close();
    };
  }, [scanId]);

  useEffect(() => {
    if (isCompleted && !error) {
      // Fetch full report payload
      fetch(`http://localhost:8000/api/reports/${scanId}`)
        .then(r => r.json())
        .then(data => {
          if (data.status === "In Progress") {
            // Edge case where SSE disconnected but DB says in progress
            setIsCompleted(false);
          } else {
            setReportData(data);
          }
        })
        .catch(err => setError("Failed to load report data"));
    }
  }, [isCompleted, error, scanId]);

  if (error) {
    return (
      <div className="dashboard-container">
        <div className="glass-panel error-panel">
          <h2>Scan Failed</h2>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (!isCompleted || !reportData) {
    return (
      <div className="dashboard-container loading-state">
        <div className="glass-panel loader-panel">
          <div className="pulse-ring"></div>
          <h2>Analysis In Progress</h2>
          <p className="status-text">{status}</p>
          <div className="progress-bar">
            {/* Indeterminate premium progress bar */}
            <div className="progress-fill indeterminate"></div>
          </div>
        </div>
      </div>
    );
  }

  // Dashboard Overview
  return (
    <div className="dashboard-container">
      <header className="dashboard-header glass-panel">
        <div>
          <h1>Scan Report: {reportData.target_url}</h1>
          <p className="scan-time">Timestamp: {new Date(reportData.scan_timestamp).toLocaleString()}</p>
        </div>
        <div className="header-actions">
          <a href={`http://localhost:8000/api/export/md/${scanId}`} className="btn-secondary" download>Export MD</a>
          <a href={`http://localhost:8000/api/export/jsonc/${scanId}`} className="btn-primary" download>Export JSON</a>
        </div>
      </header>

      <div className="metrics-grid">
        <div className="metric-card glass-panel">
          <h3>SEO Score (Estimate)</h3>
          <div className="metric-value text-accent">
            {reportData.seo.standard_meta?.title ? "Good" : "Needs Work"}
          </div>
          <p className="metric-sub">H1 Tags: {reportData.seo.headings?.counts?.h1 || 0}</p>
        </div>
        
        <div className="metric-card glass-panel">
          <h3>Sitemap Map</h3>
          <div className="metric-value text-success">
            {reportData.sitemap.urls_found} URLs
          </div>
          <p className="metric-sub">Broken Links: {reportData.sitemap.broken_links?.length || 0}</p>
        </div>
        
        <div className="metric-card glass-panel">
          <h3>Security Rating</h3>
          <div className="metric-value text-warning">
            {reportData.security.ssl?.valid ? "Secured" : "Insecure"}
          </div>
          <p className="metric-sub">Missing Headers: {reportData.security.headers?.missing_headers?.length || 0}</p>
        </div>
        
        <div className="metric-card glass-panel">
          <h3>Exposed Paths</h3>
          <div className="metric-value text-danger">
            {reportData.security.sensitive_paths_found?.length || 0}
          </div>
          <p className="metric-sub">Directory Brute-Forced</p>
        </div>
      </div>

      <div className="details-grid">
        {/* SEO Details */}
        <div className="details-card glass-panel">
          <h2>SEO Analysis</h2>
          <div className="details-content">
            <div className="detail-item">
              <span className="label">Title:</span>
              <span className="value">{reportData.seo.standard_meta?.title || "Missing"}</span>
            </div>
            <div className="detail-item">
              <span className="label">Description:</span>
              <span className="value">{reportData.seo.standard_meta?.description || "Missing"}</span>
            </div>
            <div className="detail-item">
              <span className="label">Canonical URL:</span>
              <span className="value">{reportData.seo.canonical || "Not Set"}</span>
            </div>
            <div className="detail-item">
              <span className="label">Text Ratio:</span>
              <span className="value">{reportData.seo.text_ratio?.text_to_html_ratio}% ({reportData.seo.text_ratio?.word_count} words)</span>
            </div>
            <div className="detail-item">
              <span className="label">Headings:</span>
              <span className="value">
                H1: {reportData.seo.headings?.counts?.h1 || 0} | 
                H2: {reportData.seo.headings?.counts?.h2 || 0} | 
                H3: {reportData.seo.headings?.counts?.h3 || 0}
              </span>
            </div>
            <div className="detail-item">
              <span className="label">Missing Image Alts:</span>
              <span className="value">{reportData.seo.image_alts?.missing_alt || 0} / {reportData.seo.image_alts?.total_images || 0}</span>
            </div>
          </div>
        </div>

        {/* Security Details */}
        <div className="details-card glass-panel">
          <h2>Security & Headers</h2>
          <div className="details-content">
            <div className="detail-item">
              <span className="label">SSL Issuer:</span>
              <span className="value">{reportData.security.ssl?.issuer || "Unknown"}</span>
            </div>
            <div className="detail-item">
              <span className="label">SSL Expiration:</span>
              <span className="value">{reportData.security.ssl?.expires_on || "N/A"}</span>
            </div>
            <div className="detail-item">
              <span className="label">Server Info Leaks:</span>
              <span className="value text-warning">
                {Object.keys(reportData.security.headers?.leaked_server_info || {}).length > 0 
                  ? JSON.stringify(reportData.security.headers.leaked_server_info) 
                  : "None Detected"}
              </span>
            </div>
            <div className="detail-item vertical">
              <span className="label">Missing Security Headers:</span>
              <ul className="value-list">
                {reportData.security.headers?.missing_headers?.length > 0 ? (
                  reportData.security.headers.missing_headers.map((h: string) => <li key={h}>{h}</li>)
                ) : (
                  <li>None. All good!</li>
                )}
              </ul>
            </div>
            {reportData.security.sensitive_paths_found?.length > 0 && (
              <div className="detail-item vertical">
                <span className="label text-danger">⚠️ Exposed Sensitive Paths:</span>
                <ul className="value-list error-list">
                  {reportData.security.sensitive_paths_found.map((p: string) => <li key={p}>{p}</li>)}
                </ul>
              </div>
            )}
          </div>
        </div>
        
        {/* Sitemap Details */}
        <div className="details-card glass-panel full-width">
          <h2>Sitemap & Links</h2>
          <div className="details-content">
            <div className="detail-item">
              <span className="label">Total Sitemap URLs:</span>
              <span className="value">{reportData.sitemap.urls_found}</span>
            </div>
            <div className="detail-item">
              <span className="label">Validation Scanned:</span>
              <span className="value">{reportData.sitemap.scanned_count} URLs tested</span>
            </div>
            
            {reportData.sitemap.broken_links?.length > 0 ? (
              <div className="detail-item vertical mt-4">
                <span className="label text-danger">Broken Links Found (4xx/5xx):</span>
                <div className="table-responsive">
                  <table className="link-table">
                    <thead>
                      <tr>
                        <th>Status</th>
                        <th>URL</th>
                        <th>Error</th>
                      </tr>
                    </thead>
                    <tbody>
                      {reportData.sitemap.broken_links.map((link: any, idx: number) => (
                        <tr key={idx}>
                          <td className="text-danger font-medium">{link.status || "FAIL"}</td>
                          <td className="url-cell">{link.url}</td>
                          <td className="text-muted">{link.error || "-"}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            ) : (
              <div className="detail-item mt-4">
                <span className="label">Broken Links:</span>
                <span className="value text-success">None detected among scanned URLs.</span>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
