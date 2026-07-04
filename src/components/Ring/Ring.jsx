export default function Ring({ value, max, size = 56, stroke = 5, color = "#003D32", label }) {
  const r = (size - stroke * 2) / 2;
  const circ = 2 * Math.PI * r;
  const fill = (value / max) * circ;

  return (
    <svg width={size} height={size} style={{ transform: "rotate(-90deg)" }}>
      <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="#e0e0e0" strokeWidth={stroke} />
      <circle
        cx={size / 2} cy={size / 2} r={r} fill="none" stroke={color} strokeWidth={stroke}
        strokeDasharray={`${fill} ${circ}`} strokeLinecap="round"
        style={{ transition: "stroke-dasharray 0.4s" }}
      />
      <text
        x="50%" y="50%" dominantBaseline="middle" textAnchor="middle"
        style={{ fontSize: size * 0.22, fontWeight: 800, fill: color, transform: "rotate(90deg)", transformOrigin: "center" }}
      >
        {label ?? Math.round((value / max) * 100) + "%"}
      </text>
    </svg>
  );
}
