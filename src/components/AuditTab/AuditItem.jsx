import { scoreColor } from "../../utils/status.js";
import styles from "./AuditTab.module.css";

export default function AuditItem({ item, score, onSetScore }) {
  const pct = Math.round((score / item.max) * 100);
  const color = scoreColor(pct);
  const quickValues = [...new Set([0, Math.round(item.max / 2), item.max])];

  return (
    <div className={styles.item}>
      <div className={styles.itemHead}>
        <div className={styles.itemInfo}>
          <div className={styles.itemLabel}>{item.label}</div>
          <div className={styles.itemDesc}>{item.desc}</div>
        </div>
        <div className={styles.itemScore}>
          <div className={styles.itemScoreValue} style={{ color }}>{score}</div>
          <div className={styles.itemScoreMax}>de {item.max}</div>
        </div>
      </div>

      <div className={styles.itemBarTrack}>
        <div className={styles.itemBarFill} style={{ width: `${pct}%`, background: color }} />
      </div>

      <div className={styles.controls}>
        {quickValues.map((v) => (
          <button
            key={v}
            onClick={() => onSetScore(item.id, v, item.max)}
            className={`${styles.quickButton} ${score === v ? styles.quickButtonActive : ""}`}
          >
            {v}
          </button>
        ))}
        <div className={styles.divider} />
        <div className={styles.stepper}>
          <button onClick={() => onSetScore(item.id, score - 1, item.max)} className={styles.stepButton}>−</button>
          <input
            type="number" min={0} max={item.max} value={score}
            onChange={(e) => onSetScore(item.id, parseInt(e.target.value) || 0, item.max)}
            className={styles.stepInput}
          />
          <button onClick={() => onSetScore(item.id, score + 1, item.max)} className={styles.stepButton}>+</button>
        </div>
      </div>
    </div>
  );
}
