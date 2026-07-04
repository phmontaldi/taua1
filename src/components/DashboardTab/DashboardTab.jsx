import DashboardHero from "./DashboardHero.jsx";
import MetricsRow from "./MetricsRow.jsx";
import CriticalItems from "./CriticalItems.jsx";
import SectionBreakdown from "./SectionBreakdown.jsx";
import AuditBreakdown from "./AuditBreakdown.jsx";
import styles from "./DashboardTab.module.css";

export default function DashboardTab({
  checked, scores, date, emocionador,
  done, total, pct, auditTotal, auditPct, classification, status,
  critItems, critDone, critPct, missing, onToggleItem,
}) {
  return (
    <div className={styles.tab}>
      <DashboardHero status={status} emocionador={emocionador} date={date} />
      <MetricsRow done={done} total={total} pct={pct} auditTotal={auditTotal} auditPct={auditPct} classification={classification} />
      <CriticalItems critDone={critDone} critTotal={critItems.length} critPct={critPct} missing={missing} onToggleItem={onToggleItem} />
      <SectionBreakdown checked={checked} />
      <AuditBreakdown scores={scores} />
    </div>
  );
}
