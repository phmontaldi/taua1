import styles from "./ChecklistTab.module.css";

export default function ChecklistItem({ item, index, checked, onToggle }) {
  return (
    <button
      onClick={() => onToggle(item.id)}
      className={`${styles.item} ${checked ? styles.itemChecked : index % 2 === 0 ? styles.itemEven : styles.itemOdd}`}
    >
      <div className={`${styles.checkbox} ${checked ? styles.checkboxChecked : item.critical ? styles.checkboxCritical : styles.checkboxDefault}`}>
        {checked && <span className={styles.checkmark}>✓</span>}
      </div>
      <span className={`${styles.label} ${checked ? styles.labelChecked : ""}`}>{item.label}</span>
      {item.critical && !checked && <span className={styles.essential}>ESSENCIAL</span>}
    </button>
  );
}
