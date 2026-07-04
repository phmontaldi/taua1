import styles from "./Header.module.css";

export default function Header({ date, onDateChange, emocionador, onEmocionadorChange, status }) {
  return (
    <div className={styles.header}>
      <div className={styles.topRow}>
        <div>
          <div className={styles.brand}>TAUÁ</div>
          <div className={styles.brandSub}>Resort & Convention</div>
        </div>
        <div className={styles.titleBlock}>
          <div className={styles.title}>Conferência Diária</div>
          <div className={styles.subtitle}>Bar da Piscina</div>
        </div>
      </div>

      <div className={styles.metaRow}>
        <div className={styles.field}>
          <span className={styles.fieldLabel}>Data</span>
          <input type="date" value={date} onChange={(e) => onDateChange(e.target.value)} className={styles.input} />
        </div>
        <div className={styles.field}>
          <span className={styles.fieldLabel}>Emocionador</span>
          <input
            type="text" value={emocionador} onChange={(e) => onEmocionadorChange(e.target.value)}
            placeholder="Nome..." className={`${styles.input} ${styles.inputWide}`}
          />
        </div>
        <div className={styles.statusBadge} style={{ background: status.bg, color: status.color, borderColor: status.color }}>
          {status.icon} {status.label}
        </div>
      </div>
    </div>
  );
}
