import { useState } from "react";
import {
  buildTurnoPayload, submitTurnoPayload, AuthError, DuplicateTurnoError, NetworkError,
} from "../../services/api.js";
import styles from "./DashboardTab.module.css";

export default function SubmitTurno({
  checked, scores, date, bar, emocionador, statusLabel, missing, token, onAuthError, onQueueOffline,
}) {
  const [state, setState] = useState("idle"); // idle | loading | success | queued | error
  const [message, setMessage] = useState("");

  const handleSubmit = async () => {
    setMessage("");

    if (!bar) {
      setState("error");
      setMessage("Selecione o bar antes de enviar a conferência.");
      return;
    }
    if (!emocionador || emocionador.trim().length < 2) {
      setState("error");
      setMessage("Emocionador inválido. Faça login novamente.");
      return;
    }
    if (missing.length > 0) {
      const confirmado = window.confirm(
        `Existem ${missing.length} item(ns) essencial(is) pendente(s). Deseja enviar a conferência mesmo assim?`
      );
      if (!confirmado) return;
    }

    setState("loading");
    const payload = buildTurnoPayload({ checked, scores, date, bar, emocionador, statusLabel });
    try {
      await submitTurnoPayload(payload, token);
      setState("success");
      setMessage("Conferência enviada com sucesso!");
    } catch (err) {
      if (err instanceof AuthError) {
        setState("error");
        setMessage("Sessão expirada. Faça login novamente.");
        onAuthError();
        return;
      }
      if (err instanceof DuplicateTurnoError) {
        setState("error");
        setMessage(err.message);
        return;
      }
      if (err instanceof NetworkError) {
        await onQueueOffline(payload, token);
        setState("queued");
        setMessage("Sem conexão. A conferência foi salva e será enviada automaticamente quando a internet voltar.");
        return;
      }
      setState("error");
      setMessage(err.message || "Erro ao enviar a conferência. Tente novamente.");
    }
  };

  return (
    <div className={styles.card}>
      <div className={styles.cardTitle}>📤 Enviar Conferência</div>

      {state === "success" ? (
        <div className={styles.submitSuccess}>✅ {message}</div>
      ) : state === "queued" ? (
        <div className={styles.submitQueued}>📶 {message}</div>
      ) : (
        <>
          <button
            type="button" className={styles.submitBtn} onClick={handleSubmit} disabled={state === "loading"}
          >
            {state === "loading" ? "Enviando..." : "Enviar Conferência"}
          </button>
          {state === "error" && <div className={styles.submitError}>⚠️ {message}</div>}
        </>
      )}
    </div>
  );
}
