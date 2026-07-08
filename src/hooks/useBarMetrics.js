import { useMemo } from "react";
import { SECTIONS } from "../data/checklistData.js";
import { AUDIT, SCALE } from "../data/auditData.js";
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

    const validAuditIds = new Set(AUDIT.flatMap((s) => s.items.map((i) => i.id)));
    const auditMax = AUDIT.reduce((sum, s) => sum + s.max, 0);
    const auditTotal = Object.entries(scores)
      .filter(([id]) => validAuditIds.has(id))
      .reduce((sum, [, v]) => sum + (v || 0), 0);
    const auditPct = auditMax ? Math.round((auditTotal / auditMax) * 100) : 0;
    const classification = getClassification(auditTotal, SCALE);

    const status = getOpenStatus(critPct, pct);

    return {
      total, done, pct,
      critItems, critDone, critPct, missing,
      auditTotal, auditMax, auditPct, classification, status,
    };
  }, [checked, scores]);
}
