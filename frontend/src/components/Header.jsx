import ThemeToggle from './ThemeToggle';

export default function Header({ theme, setTheme }) {
  return (
    <header className="header">
      <h1>
        Text Summarization
        <span className="header-badge">V2.0</span>
      </h1>
      <ThemeToggle theme={theme} setTheme={setTheme} />
    </header>
  );
}
