import styles from "./StatusBar.module.css";

export default function StatusBar({ done, total, auditTotal, status }) {
  return (
    <div className={styles.bar}>
      <span className={styles.counts}>
        ✓ {done}/{total} &nbsp;·&nbsp; ⭐ {auditTotal}/200
      </span>
      <div className={styles.badge} style={{ background: status.bg, color: status.color, borderColor: status.color }}>
        {status.icon} {status.label}
      </div>
    </div>
  );
}
