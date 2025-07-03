
const ThemeToggle = () => {
  const toggleTheme = () => {
    document.body.classList.toggle("dark");
  };

  return (
    <button className="theme-toggle" onClick={toggleTheme}>
      ??
    </button>
  );
};

export default ThemeToggle;
