import { scoreColor } from "../../utils/status.js";
import AuditItem from "./AuditItem.jsx";
import styles from "./AuditTab.module.css";

export default function AuditSection({ section, scores, onSetScore }) {
  const secScore = section.items.reduce((a, i) => a + (scores[i.id] || 0), 0);
  const secPct = Math.round((secScore / section.max) * 100);
  const color = scoreColor(secPct);

  return (
    <div className={styles.section}>
      <div className={styles.sectionHeader}>
        <span className={styles.sectionTitle}>{section.title}</span>
        <span className={styles.sectionScore}>
          {secScore}/{section.max}&nbsp;<span className={styles.sectionScorePct}>({secPct}%)</span>
        </span>
      </div>
      <div className={styles.sectionBarTrack}>
        <div className={styles.sectionBarFill} style={{ width: `${secPct}%`, background: color }} />
      </div>

      {section.items.map((item) => (
        <AuditItem key={item.id} item={item} score={scores[item.id] || 0} onSetScore={onSetScore} />
      ))}
    </div>
  );
}
