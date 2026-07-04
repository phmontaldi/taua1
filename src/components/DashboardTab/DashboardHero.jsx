import styles from "./DashboardTab.module.css";

export default function DashboardHero({ status, emocionador, date }) {
  const formattedDate = new Date(date + "T12:00:00").toLocaleDateString("pt-BR", {
    weekday: "long", day: "2-digit", month: "long", year: "numeric",
  });

  return (
    <div className={styles.hero}>
      <div className={styles.heroIcon}>{status.icon}</div>
      <div className={styles.heroLabel}>{status.label}</div>
      {emocionador && <div className={styles.heroMeta}>Emocionador: {emocionador}</div>}
      <div className={styles.heroMeta}>{formattedDate}</div>
    </div>
  );
}
