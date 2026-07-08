import { useState } from "react";
import { SECTIONS } from "./data/checklistData.js";
import { useLocalStorage, clearLocalStorageKeys } from "./hooks/useLocalStorage.js";
import { useBarMetrics } from "./hooks/useBarMetrics.js";
import { useAuth } from "./hooks/useAuth.js";
import Login from "./components/Login/Login.jsx";
import Header from "./components/Header/Header.jsx";
import Tabs from "./components/Tabs/Tabs.jsx";
import ChecklistTab from "./components/ChecklistTab/ChecklistTab.jsx";
import AuditTab from "./components/AuditTab/AuditTab.jsx";
import DashboardTab from "./components/DashboardTab/DashboardTab.jsx";
import StatusBar from "./components/StatusBar/StatusBar.jsx";
import styles from "./App.module.css";

const DEVICE_TIMEZONE = "America/Fortaleza";

const todayLocal = () =>
  new Intl.DateTimeFormat("en-CA", {
    timeZone: DEVICE_TIMEZONE,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(new Date());

const defaultOpenSections = () => Object.fromEntries(SECTIONS.map((s) => [s.id, true]));

export default function App() {
  const { auth, login, logout } = useAuth();
  const [tab, setTab] = useState("check");
  const [checked, setChecked] = useLocalStorage("checked", {});
  const [scores, setScores] = useLocalStorage("scores", {});
  const [bar, setBar] = useLocalStorage("bar", "");
  const [date, setDate] = useState(todayLocal());
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

  if (!auth) {
    return <Login onLogin={login} />;
  }

  return (
    <div className={styles.app}>
      <Header
        date={date} onDateChange={setDate}
        emocionador={auth.nome} onLogout={logout}
        bar={bar} onBarChange={setBar}
        status={metrics.status}
      />

      <Tabs
        active={tab} onChange={setTab}
        checklistBadge={`${metrics.done}/${metrics.total}`}
        auditTotal={metrics.auditTotal}
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
          checked={checked} scores={scores} date={date} emocionador={auth.nome} bar={bar}
          done={metrics.done} total={metrics.total} pct={metrics.pct}
          auditTotal={metrics.auditTotal} auditPct={metrics.auditPct} classification={metrics.classification}
          status={metrics.status}
          critItems={metrics.critItems} critDone={metrics.critDone} critPct={metrics.critPct} missing={metrics.missing}
          onToggleItem={toggleItem}
          token={auth.token} onAuthError={logout}
        />
      )}

      <StatusBar done={metrics.done} total={metrics.total} auditTotal={metrics.auditTotal} status={metrics.status} />
    </div>
  );
}
