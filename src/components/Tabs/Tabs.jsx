import { AUDIT } from "../../data/auditData.js";
import styles from "./Tabs.module.css";

const TABS = [
  { id: "check", label: "📋 Checklist" },
  { id: "audit", label: "⭐ Auditoria" },
  { id: "dash", label: "📊 Dashboard" },
];

const AUDIT_MAX = AUDIT.reduce((sum, s) => sum + s.max, 0);

export default function Tabs({ active, onChange, checklistBadge, auditTotal }) {
  const badges = { check: checklistBadge, audit: `${auditTotal}/${AUDIT_MAX}`, dash: null };

  return (
    <div className={styles.tabs}>
      {TABS.map((t) => {
        const isActive = active === t.id;
        return (
          <button
            key={t.id}
            onClick={() => onChange(t.id)}
            className={`${styles.tab} ${isActive ? styles.tabActive : ""}`}
          >
            <span>{t.label}</span>
            {badges[t.id] && (
              <span className={`${styles.badge} ${isActive ? styles.badgeActive : ""}`}>{badges[t.id]}</span>
            )}
          </button>
        );
      })}
    </div>
  );
}
