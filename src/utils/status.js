export const scoreColor = (pct) =>
  pct >= 80 ? "#003D32" : pct >= 60 ? "#C8A84B" : pct >= 40 ? "#cc6600" : "#b22222";

export const getClassification = (pts, scale) =>
  scale.find((s) => pts >= s.min) || scale[scale.length - 1];

export const getOpenStatus = (critPct, pct) => {
  if (critPct === 100 && pct >= 90) return { label: "Pronto para Abertura", color: "#003D32", bg: "#d4f0e8", icon: "✅" };
  if (critPct === 100 && pct >= 70) return { label: "Quase Pronto", color: "#1a6b4a", bg: "#e4f5ed", icon: "🟡" };
  if (critPct >= 75) return { label: "Em Preparação", color: "#C8A84B", bg: "#fef3cc", icon: "🟠" };
  if (critPct >= 40) return { label: "Incompleto", color: "#cc6600", bg: "#fde8cc", icon: "🔴" };
  return { label: "Não Iniciado", color: "#b22222", bg: "#fde0e0", icon: "🚨" };
};
