import { openDB } from "idb";
import { submitTurnoPayload, DuplicateTurnoError, NetworkError } from "./api.js";

const DB_NAME = "tauaBar-offline-queue";
const DB_VERSION = 1;
const STORE_NAME = "submissions";

function openQueueDb() {
  return openDB(DB_NAME, DB_VERSION, {
    upgrade(db) {
      if (!db.objectStoreNames.contains(STORE_NAME)) {
        db.createObjectStore(STORE_NAME, { keyPath: "id", autoIncrement: true });
      }
    },
  });
}

export async function enqueueSubmission(payload, token) {
  const db = await openQueueDb();
  await db.add(STORE_NAME, { payload, token, queuedAt: new Date().toISOString() });
  db.close();
}

export async function countPendingSubmissions() {
  const db = await openQueueDb();
  const count = await db.count(STORE_NAME);
  db.close();
  return count;
}

let processing = false;

// Reenvia a fila de conferências salvas offline. A constraint (date, bar) do
// backend garante idempotência: um 409 significa que o turno já foi entregue
// em uma tentativa anterior, então o item é apenas removido da fila.
export async function processQueue({ onChange } = {}) {
  if (processing) return;
  processing = true;

  try {
    const db = await openQueueDb();
    const items = await db.getAll(STORE_NAME);

    for (const item of items) {
      try {
        await submitTurnoPayload(item.payload, item.token);
        await db.delete(STORE_NAME, item.id);
      } catch (err) {
        if (err instanceof DuplicateTurnoError) {
          await db.delete(STORE_NAME, item.id);
          continue;
        }
        if (err instanceof NetworkError) {
          // Ainda sem conexão: interrompe e tenta a fila inteira novamente mais tarde.
          break;
        }
        // Outros erros (ex.: sessão expirada) permanecem na fila para uma próxima tentativa.
      }
    }

    db.close();
  } finally {
    processing = false;
    onChange?.(await countPendingSubmissions());
  }
}
