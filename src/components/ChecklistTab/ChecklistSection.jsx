import styles from "./ChecklistTab.module.css";
import ChecklistItem from "./ChecklistItem.jsx";

export default function ChecklistSection({ section, checked, isOpen, onToggleSection, onToggleItem }) {
  const secDone = section.items.filter((i) => checked[i.id]).length;
  const secPct = Math.round((secDone / section.items.length) * 100);
  const allDone = secDone === section.items.length;

  return (
    <div className={`${styles.section} ${allDone ? styles.sectionDone : ""}`}>
      <button onClick={() => onToggleSection(section.id)} className={`${styles.sectionHeader} ${allDone ? styles.sectionHeaderDone : ""}`}>
        <span className={styles.sectionIcon}>{section.icon}</span>
        <span className={styles.sectionTitle}>{section.title}</span>
        <div className={styles.sectionMeta}>
          <div className={styles.sectionBarTrack}>
            <div className={styles.sectionBarFill} style={{ width: `${secPct}%`, background: allDone ? "var(--color-green)" : "var(--color-gold)" }} />
          </div>
          <span className={`${styles.sectionCount} ${allDone ? styles.sectionCountDone : ""}`}>{secDone}/{section.items.length}</span>
          <span className={styles.chevron}>{isOpen ? "▲" : "▼"}</span>
        </div>
      </button>

      {isOpen && (
        <div className={styles.itemList}>
          {section.items.map((item, idx) => (
            <ChecklistItem key={item.id} item={item} index={idx} checked={!!checked[item.id]} onToggle={onToggleItem} />
          ))}
        </div>
      )}
    </div>
  );
}
