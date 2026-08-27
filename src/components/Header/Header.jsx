import styles from "./Header.module.css";

export default function Header({ date, onDateChange, emocionador, onLogout, bar, onBarChange, bars, status }) {
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
          <span className={styles.fieldLabel}>Bar</span>
          <select
            required value={bar} onChange={(e) => onBarChange(e.target.value)} className={styles.input}
          >
            <option value="" disabled>Selecione o bar</option>
            {bars.map((b) => (
              <option key={b.slug} value={b.slug}>{b.rotulo}</option>
            ))}
          </select>
        </div>
        <div className={styles.field}>
          <span className={styles.fieldLabel}>Data</span>
          <input type="date" value={date} onChange={(e) => onDateChange(e.target.value)} className={styles.input} />
        </div>
        <div className={styles.field}>
          <span className={styles.fieldLabel}>Emocionador</span>
          <span className={styles.emocionadorValue}>{emocionador}</span>
          <button type="button" onClick={onLogout} className={styles.logoutBtn}>Sair</button>
        </div>
        <div className={styles.statusBadge} style={{ background: status.bg, color: status.color, borderColor: status.color }}>
          {status.icon} {status.label}
        </div>
      </div>
    </div>
  );
}
