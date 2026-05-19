export function MastheadDate() {
  const now = new Date();
  const formatted = now.toLocaleDateString("es-ES", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });
  const edition = `Nº ${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, "0")}${String(now.getDate()).padStart(2, "0")}`;

  return (
    <p className="masthead-meta">
      <span>{formatted}</span>
      <span className="meta-sep">|</span>
      <span>{edition}</span>
      <span className="meta-sep">|</span>
      <span>Motor CLIPS</span>
    </p>
  );
}
