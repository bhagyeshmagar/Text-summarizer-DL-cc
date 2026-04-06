import { useState } from 'react';

export default function OutputCard({ summary, meta }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    if (!summary) return;
    try {
      await navigator.clipboard.writeText(summary);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Fallback for older browsers
      const textarea = document.createElement('textarea');
      textarea.value = summary;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand('copy');
      document.body.removeChild(textarea);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="card result-card glass-panel">
      <div className="card-header">
        <label className="card-label">OUTPUT SUMMARY</label>
        {summary && (
          <button
            className={`btn-copy ${copied ? 'copied' : ''}`}
            onClick={handleCopy}
          >
            {copied ? '✓ COPIED' : '⎘ COPY'}
          </button>
        )}
      </div>

      <div className={`result-box ${summary ? 'has-content' : ''}`}>
        {summary ? (
          summary
        ) : (
          <div className="empty-state">
            <div className="empty-dots">
              <span />
              <span />
              <span />
            </div>
            <p className="empty-text">Run the model to see your summary here</p>
          </div>
        )}
      </div>

      {meta && summary && (
        <div className="stats-row">
          <div className="stat-chip">
            Input <span className="stat-value">{meta.original_words}</span> words
          </div>
          <div className="stat-chip">
            Output <span className="stat-value">{meta.summary_words}</span> words
          </div>
          <div className="stat-chip">
            Sentences <span className="stat-value">{meta.summary_sentences}</span>
          </div>
          <div className="stat-chip">
            Compressed <span className="stat-value">{meta.compression_ratio}%</span>
          </div>
        </div>
      )}
    </div>
  );
}
