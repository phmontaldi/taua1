import Ring from "../Ring/Ring.jsx";
import styles from "./DashboardTab.module.css";

export default function MetricsRow({ done, total, pct, auditTotal, auditPct, classification }) {
  return (
    <div className={styles.metricsRow}>
      <div className={styles.metricCard}>
        <div className={styles.metricLabel}>Checklist</div>
        <Ring value={done} max={total} size={60} stroke={6} color={pct === 100 ? "#003D32" : "#C8A84B"} />
        <div className={styles.metricSub}>{done}/{total} itens</div>
        <div className={styles.metricValue} style={{ color: pct === 100 ? "#003D32" : "#C8A84B" }}>{pct}%</div>
      </div>
      <div className={styles.metricCard}>
        <div className={styles.metricLabel}>Auditoria</div>
        <Ring value={auditTotal} max={200} size={60} stroke={6} color={classification.color} label={`${auditTotal}`} />
        <div className={styles.metricSub}>{auditPct}% · 200 pts</div>
        <div className={styles.metricValueBold} style={{ color: classification.color }}>{classification.label}</div>
      </div>
    </div>
  );
}
