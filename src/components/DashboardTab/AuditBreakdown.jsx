import { AUDIT } from "../../data/auditData.js";
import { scoreColor } from "../../utils/status.js";
import styles from "./DashboardTab.module.css";

export default function AuditBreakdown({ scores }) {
  return (
    <div className={styles.card}>
      <div className={styles.cardTitle}>⭐ Resultado da Auditoria por Seção</div>
      {AUDIT.map((sec) => {
        const secScore = sec.items.reduce((a, i) => a + (scores[i.id] || 0), 0);
        const secPct = Math.round((secScore / sec.max) * 100);
        const color = scoreColor(secPct);
        return (
          <div key={sec.id} className={styles.auditBreakdownSection}>
            <div className={styles.breakdownHead}>
              <span className={styles.auditSectionLabel}>{sec.title}</span>
              <span className={styles.auditSectionScore} style={{ color }}>
                {secScore}/{sec.max} <span className={styles.auditSectionPct}>({secPct}%)</span>
              </span>
            </div>
            <div className={styles.auditSectionBarTrack}>
              <div className={styles.auditSectionBarFill} style={{ width: `${secPct}%`, background: color }} />
            </div>
            {sec.items.map((item) => {
              const itemScore = scores[item.id] || 0;
              const itemPct = Math.round((itemScore / item.max) * 100);
              return (
                <div key={item.id} className={styles.auditItemRow}>
                  <span className={styles.auditItemLabel}>{item.label.split(". ")[0]}.</span>
                  <div className={styles.auditItemBarTrack}>
                    <div className={styles.auditItemBarFill} style={{ width: `${itemPct}%`, background: scoreColor(itemPct) }} />
                  </div>
                  <span className={styles.auditItemScore} style={{ color: scoreColor(itemPct) }}>{itemScore}/{item.max}</span>
                </div>
              );
            })}
          </div>
        );
      })}
    </div>
  );
}
