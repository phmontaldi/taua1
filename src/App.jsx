import { useState } from "react";
import { SECTIONS } from "./data/checklistData.js";
import { useLocalStorage, clearLocalStorageKeys } from "./hooks/useLocalStorage.js";
import { useBarMetrics } from "./hooks/useBarMetrics.js";
import Header from "./components/Header/Header.jsx";
import Tabs from "./components/Tabs/Tabs.jsx";
import ChecklistTab from "./components/ChecklistTab/ChecklistTab.jsx";
import AuditTab from "./components/AuditTab/AuditTab.jsx";
import DashboardTab from "./components/DashboardTab/DashboardTab.jsx";
import StatusBar from "./components/StatusBar/StatusBar.jsx";
import styles from "./App.module.css";

const todayISO = () => new Date().toISOString().split("T")[0];
const defaultOpenSections = () => Object.fromEntries(SECTIONS.map((s) => [s.id, true]));

export default function App() {
  const [tab, setTab] = useState("check");
  const [checked, setChecked] = useLocalStorage("checked", {});
  const [scores, setScores] = useLocalStorage("scores", {});
  const [emocionador, setEmocionador] = useLocalStorage("emocionador", "");
  const [date, setDate] = useLocalStorage("date", todayISO());
  const [open, setOpen] = useLocalStorage("open", defaultOpenSections());

  const metrics = useBarMetrics(checked, scores);

  const toggleItem = (id) => setChecked((p) => ({ ...p, [id]: !p[id] }));
  const toggleSection = (id) => setOpen((p) => ({ ...p, [id]: !p[id] }));
  const setScore = (id, val, max) => setScores((p) => ({ ...p, [id]: Math.max(0, Math.min(max, val)) }));

  const resetAll = () => {
    setChecked({});
    setScores({});
    clearLocalStorageKeys(["checked", "scores"]);
  };

  return (
    <div className={styles.app}>
      <Header
        date={date} onDateChange={setDate}
        emocionador={emocionador} onEmocionadorChange={setEmocionador}
        status={metrics.status}
      />

      <Tabs
        active={tab} onChange={setTab}
        checklistBadge={`${metrics.done}/${metrics.total}`}
        auditBadge={`${metrics.auditTotal}/200`}
      />

      {tab === "check" && (
        <ChecklistTab
          checked={checked} open={open}
          done={metrics.done} total={metrics.total} pct={metrics.pct} missing={metrics.missing}
          onToggleItem={toggleItem} onToggleSection={toggleSection} onResetAll={resetAll}
        />
      )}

      {tab === "audit" && (
        <AuditTab
          scores={scores}
          auditTotal={metrics.auditTotal} auditPct={metrics.auditPct} classification={metrics.classification}
          onSetScore={setScore}
        />
      )}

      {tab === "dash" && (
        <DashboardTab
          checked={checked} scores={scores} date={date} emocionador={emocionador}
          done={metrics.done} total={metrics.total} pct={metrics.pct}
          auditTotal={metrics.auditTotal} auditPct={metrics.auditPct} classification={metrics.classification}
          status={metrics.status}
          critItems={metrics.critItems} critDone={metrics.critDone} critPct={metrics.critPct} missing={metrics.missing}
          onToggleItem={toggleItem}
        />
      )}

      <StatusBar done={metrics.done} total={metrics.total} auditTotal={metrics.auditTotal} status={metrics.status} />
    </div>
  );
}
