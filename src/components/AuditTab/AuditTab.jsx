import { AUDIT, SCALE } from "../../data/auditData.js";
import AuditSection from "./AuditSection.jsx";
import styles from "./AuditTab.module.css";

export default function AuditTab({ scores, auditTotal, auditPct, classification, onSetScore }) {
  return (
    <div className={styles.tab}>
      <div className={styles.hero}>
        <div className={styles.heroLabel}>Pontuação Total</div>
        <div className={styles.heroValue}>{auditTotal}</div>
        <div className={styles.heroSub}>de 200 pontos · {auditPct}%</div>
        <div
          className={styles.heroBadge}
          style={{ background: classification.bg, color: classification.color, borderColor: classification.color }}
        >
          {classification.label}
        </div>
      </div>

      {AUDIT.map((sec) => (
        <AuditSection key={sec.id} section={sec} scores={scores} onSetScore={onSetScore} />
      ))}

      <div className={styles.scaleCard}>
        <div className={styles.scaleTitle}>Escala de Classificação</div>
        {SCALE.map((sc) => {
          const active = classification.label === sc.label;
          return (
            <div
              key={sc.label}
              className={styles.scaleRow}
              style={{ background: active ? sc.bg : "transparent", borderColor: active ? sc.color : "transparent" }}
            >
              <span className={styles.scaleLabel} style={{ color: sc.color, fontWeight: active ? 800 : 400 }}>{sc.label}</span>
              <span className={styles.scaleRange}>{sc.range} pts</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
