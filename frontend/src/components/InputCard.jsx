export default function InputCard({ text, setText, onSummarize, loading }) {
  const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;
  const charCount = text.length;

  const handleClear = () => {
    setText('');
  };

  return (
    <div className="card glass-panel">
      <div className="card-header">
        <label className="card-label">INPUT TEXT</label>
        <span className="word-count">
          {wordCount} words · {charCount} chars
        </span>
      </div>

      <textarea
        className="input-textarea"
        placeholder="Paste your article, essay, or any text here..."
        value={text}
        onChange={e => setText(e.target.value)}
      />

      <div className="button-row">
        <button
          className="btn btn-primary"
          onClick={onSummarize}
          disabled={loading || !text.trim()}
        >
          {loading ? (
            <>
              <span className="spinner" />
              PROCESSING
            </>
          ) : (
            'SUMMARIZE.EXE'
          )}
        </button>
        {text && (
          <button className="btn btn-secondary" onClick={handleClear}>
            CLEAR
          </button>
        )}
      </div>
    </div>
  );
}
