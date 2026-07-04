import { useMemo } from "react";
import { SECTIONS } from "../data/checklistData.js";
import { SCALE } from "../data/auditData.js";
import { getClassification, getOpenStatus } from "../utils/status.js";

export function useBarMetrics(checked, scores) {
  return useMemo(() => {
    const allItems = SECTIONS.flatMap((s) => s.items);
    const total = allItems.length;
    const done = allItems.filter((i) => checked[i.id]).length;
    const pct = total ? Math.round((done / total) * 100) : 0;

    const critItems = allItems.filter((i) => i.critical);
    const critDone = critItems.filter((i) => checked[i.id]).length;
    const critPct = critItems.length ? Math.round((critDone / critItems.length) * 100) : 0;
    const missing = critItems.filter((i) => !checked[i.id]);

    const auditTotal = Object.values(scores).reduce((a, v) => a + (v || 0), 0);
    const auditPct = Math.round((auditTotal / 200) * 100);
    const classification = getClassification(auditTotal, SCALE);

    const status = getOpenStatus(critPct, pct);

    return {
      total, done, pct,
      critItems, critDone, critPct, missing,
      auditTotal, auditPct, classification, status,
    };
  }, [checked, scores]);
}
