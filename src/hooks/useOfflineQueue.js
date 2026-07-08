import { useCallback, useEffect, useState } from "react";
import { countPendingSubmissions, enqueueSubmission, processQueue } from "../services/offlineQueue.js";

export function useOfflineQueue() {
  const [pendingCount, setPendingCount] = useState(0);

  const runQueue = useCallback(async () => {
    await processQueue({ onChange: setPendingCount });
  }, []);

  useEffect(() => {
    countPendingSubmissions().then(setPendingCount);
    runQueue();

    window.addEventListener("online", runQueue);
    return () => window.removeEventListener("online", runQueue);
  }, [runQueue]);

  const enqueue = useCallback(async (payload, token) => {
    await enqueueSubmission(payload, token);
    setPendingCount(await countPendingSubmissions());
  }, []);

  return { pendingCount, enqueue };
}
