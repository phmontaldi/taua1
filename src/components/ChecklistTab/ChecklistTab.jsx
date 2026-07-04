import { SECTIONS } from "../../data/checklistData.js";
import Ring from "../Ring/Ring.jsx";
import ChecklistSection from "./ChecklistSection.jsx";
import styles from "./ChecklistTab.module.css";

export default function ChecklistTab({ checked, open, done, total, pct, missing, onToggleItem, onToggleSection, onResetAll }) {
  return (
    <div className={styles.tab}>
      <div className={styles.summary}>
        <Ring value={done} max={total} size={54} stroke={5} color={pct === 100 ? "#003D32" : "#C8A84B"} />
        <div className={styles.summaryText}>
          <div className={styles.summaryTitle}>{done} de {total} itens concluídos</div>
          <div className={styles.summaryBarTrack}>
            <div className={styles.summaryBarFill} style={{ width: `${pct}%`, background: pct === 100 ? "#003D32" : "#C8A84B" }} />
          </div>
          {missing.length > 0
            ? <div className={styles.summaryWarning}>⚠️ {missing.length} itens essenciais pendentes</div>
            : <div className={styles.summaryOk}>✅ Todos itens essenciais OK</div>}
        </div>
      </div>

      {SECTIONS.map((sec) => (
        <ChecklistSection
          key={sec.id}
          section={sec}
          checked={checked}
          isOpen={!!open[sec.id]}
          onToggleSection={onToggleSection}
          onToggleItem={onToggleItem}
        />
      ))}

      <button onClick={onResetAll} className={styles.resetButton}>↺ Limpar tudo para novo turno</button>
    </div>
  );
}
