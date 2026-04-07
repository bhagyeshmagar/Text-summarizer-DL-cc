import { useState, useEffect } from 'react';
import axios from 'axios';

export default function HistoryPanel({ isOpen, onClose, onLoadEntry }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [expandedId, setExpandedId] = useState(null);

  useEffect(() => {
    if (isOpen) {
      fetchHistory();
    }
  }, [isOpen]);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const res = await axios.get('/history');
      setHistory(res.data);
    } catch (err) {
      console.error('Failed to fetch history', err);
    } finally {
      setLoading(false);
    }
  };

  const deleteEntry = async (id, e) => {
    e.stopPropagation();
    try {
      await axios.delete(`/history/${id}`);
      setHistory(prev => prev.filter(h => h.id !== id));
    } catch (err) {
      console.error('Failed to delete entry', err);
    }
  };

  const clearAll = async () => {
    try {
      await axios.delete('/history');
      setHistory([]);
    } catch (err) {
      console.error('Failed to clear history', err);
    }
  };

  const formatTime = (iso) => {
    const d = new Date(iso);
    const now = new Date();
    const diff = now - d;
    if (diff < 60000) return 'Just now';
    if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
  };

  if (!isOpen) return null;

  return (
    <div className="history-overlay" onClick={onClose}>
      <div className="history-panel glass-panel" onClick={e => e.stopPropagation()}>
        {/* Header */}
        <div className="history-header">
          <h2>History</h2>
          <div className="history-header-actions">
            {history.length > 0 && (
              <button className="btn-clear-all" onClick={clearAll}>
                Clear All
              </button>
            )}
            <button className="btn-close-history" onClick={onClose} aria-label="close">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="history-list">
          {loading && <p className="history-empty">Loading...</p>}
          {!loading && history.length === 0 && (
            <div className="history-empty">
              <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12 6 12 12 16 14"></polyline>
              </svg>
              <p>No summaries yet</p>
              <span>Your summarization history will appear here</span>
            </div>
          )}

          {history.map(entry => (
            <div
              key={entry.id}
              className={`history-item ${expandedId === entry.id ? 'expanded' : ''}`}
              onClick={() => setExpandedId(prev => prev === entry.id ? null : entry.id)}
            >
              <div className="history-item-header">
                <div className="history-item-info">
                  <span className="history-model">{entry.model}</span>
                  <span className="history-time">{formatTime(entry.timestamp)}</span>
                </div>
                <div className="history-item-actions">
                  <button
                    className="btn-history-action"
                    title="Load this summary"
                    onClick={(e) => {
                      e.stopPropagation();
                      onLoadEntry(entry);
                      onClose();
                    }}
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <polyline points="1 4 1 10 7 10"></polyline>
                      <path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"></path>
                    </svg>
                  </button>
                  <button
                    className="btn-history-action delete"
                    title="Delete"
                    onClick={(e) => deleteEntry(entry.id, e)}
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <polyline points="3 6 5 6 21 6"></polyline>
                      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    </svg>
                  </button>
                </div>
              </div>

              <p className="history-preview">{entry.input_preview}...</p>

              {expandedId === entry.id && (
                <div className="history-expanded">
                  <div className="history-summary-label">Summary</div>
                  <p className="history-summary-text">{entry.summary}</p>
                  {entry.meta && (
                    <div className="history-meta">
                      <span>{entry.meta.original_words} → {entry.meta.summary_words} words</span>
                      <span>{entry.meta.compression_ratio}% compressed</span>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
