import styles from "./StatusBar.module.css";

export default function StatusBar({ done, total, auditTotal, status, pendingCount = 0 }) {
  return (
    <div className={styles.bar}>
      <span className={styles.counts}>
        ✓ {done}/{total} &nbsp;·&nbsp; ⭐ {auditTotal}/200
        {pendingCount > 0 && (
          <>
            {" "}
            &nbsp;·&nbsp;
            <span className={styles.pending}>
              📶 {pendingCount} envio{pendingCount > 1 ? "s" : ""} pendente{pendingCount > 1 ? "s" : ""}
            </span>
          </>
        )}
      </span>
      <div className={styles.badge} style={{ background: status.bg, color: status.color, borderColor: status.color }}>
        {status.icon} {status.label}
      </div>
    </div>
  );
}
