import { useState } from 'react';
import axios from 'axios';
import './index.css';

import Sidebar from './components/Sidebar';
import Header from './components/Header';
import InputCard from './components/InputCard';
import OutputCard from './components/OutputCard';
import HistoryPanel from './components/HistoryPanel';

const MODELS = [
  { value: "AI Contextual (Deep Learning)", label: "BART LLM (Human-like)" },
  { value: "Core Python algo(Frequency and Ranking based)", label: "TF-IDF Algorithm" },
  { value: "Lex Rank: From Python lib sumy", label: "Sumy: Lex Rank" },
  { value: "LSA: From Python lib sumy", label: "Sumy: LSA" },
  { value: "Text Rank: From Python lib sumy", label: "Sumy: Text Rank" },
];

function App() {
  const [text, setText] = useState('');
  const [model, setModel] = useState(MODELS[0].value);
  const [numSentences, setNumSentences] = useState(3);
  const [summary, setSummary] = useState('');
  const [meta, setMeta] = useState(null);
  const [loading, setLoading] = useState(false);
  const [historyOpen, setHistoryOpen] = useState(false);
  const [theme, setTheme] = useState(
    () => localStorage.getItem('txt-summ-theme') || 'dark'
  );

  const handleSummarize = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setSummary('');
    setMeta(null);
    try {
      const response = await axios.post('http://localhost:8000/summarize', {
        text,
        model_selection: model,
        no_of_sentence_on_output: numSentences,
      });
      setSummary(response.data.summary);
      setMeta(response.data.meta);
    } catch (error) {
      console.error(error);
      setSummary('Error generating summary. Please check the backend server.');
    } finally {
      setLoading(false);
    }
  };

  const handleLoadEntry = (entry) => {
    setSummary(entry.summary);
    setMeta(entry.meta);
  };

  return (
    <div className="layout">
      <Sidebar
        model={model}
        setModel={setModel}
        numSentences={numSentences}
        setNumSentences={setNumSentences}
        models={MODELS}
        onOpenHistory={() => setHistoryOpen(true)}
      />

      <main className="main-content">
        <Header theme={theme} setTheme={setTheme} />

        <section className="editor-section">
          <InputCard
            text={text}
            setText={setText}
            onSummarize={handleSummarize}
            loading={loading}
          />

          <OutputCard summary={summary} meta={meta} />
        </section>
      </main>

      <HistoryPanel
        isOpen={historyOpen}
        onClose={() => setHistoryOpen(false)}
        onLoadEntry={handleLoadEntry}
      />
    </div>
  );
}

export default App;
