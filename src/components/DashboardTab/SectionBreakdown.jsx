import { SECTIONS } from "../../data/checklistData.js";
import styles from "./DashboardTab.module.css";

export default function SectionBreakdown({ checked }) {
  return (
    <div className={styles.card}>
      <div className={styles.cardTitle}>📊 Progresso por Seção</div>
      {SECTIONS.map((sec) => {
        const secDone = sec.items.filter((i) => checked[i.id]).length;
        const secPct = Math.round((secDone / sec.items.length) * 100);
        const complete = secDone === sec.items.length;
        return (
          <div key={sec.id} className={styles.breakdownRow}>
            <div className={styles.breakdownHead}>
              <span className={styles.breakdownLabel} style={{ fontWeight: complete ? 700 : 400 }}>
                {complete ? "✅" : "○"} {sec.icon} {sec.title}
              </span>
              <span className={styles.breakdownCount} style={{ color: secPct === 100 ? "#003D32" : "#bbb" }}>
                {secDone}/{sec.items.length}
              </span>
            </div>
            <div className={styles.breakdownBarTrack}>
              <div className={styles.breakdownBarFill} style={{ width: `${secPct}%`, background: secPct === 100 ? "#003D32" : "#C8A84B" }} />
            </div>
          </div>
        );
      })}
    </div>
  );
}
