import styles from "./DashboardTab.module.css";

export default function CriticalItems({ critDone, critTotal, critPct, missing, onToggleItem }) {
  return (
    <div className={styles.card}>
      <div className={styles.cardHeadRow}>
        <span className={styles.cardTitle}>🎯 Itens Essenciais</span>
        <span className={styles.critCount} style={{ color: critPct === 100 ? "#003D32" : "#cc6600" }}>
          {critDone}/{critTotal} · {critPct}%
        </span>
      </div>
      <div className={styles.critBarTrack}>
        <div className={styles.critBarFill} style={{ width: `${critPct}%`, background: critPct === 100 ? "#003D32" : "#cc6600" }} />
      </div>

      {missing.length === 0 ? (
        <div className={styles.critAllDone}>✅ Todos os itens essenciais completos!</div>
      ) : (
        <>
          <div className={styles.critPendingLabel}>Pendentes ({missing.length}):</div>
          {missing.map((item) => (
            <button key={item.id} onClick={() => onToggleItem(item.id)} className={styles.critPendingItem}>
              <div className={styles.critPendingBox} />
              <span className={styles.critPendingLabelText}>{item.label}</span>
            </button>
          ))}
        </>
      )}
    </div>
  );
}
