import { useState } from "react";
import { submitTurno, AuthError, DuplicateTurnoError } from "../../services/api.js";
import styles from "./DashboardTab.module.css";

export default function SubmitTurno({
  checked, scores, date, bar, emocionador, statusLabel, missing, token, onAuthError,
}) {
  const [state, setState] = useState("idle"); // idle | loading | success | error
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
    try {
      await submitTurno({ checked, scores, date, bar, emocionador, statusLabel }, token);
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
      setState("error");
      setMessage(err.message || "Erro ao enviar a conferência. Tente novamente.");
    }
  };

  return (
    <div className={styles.card}>
      <div className={styles.cardTitle}>📤 Enviar Conferência</div>

      {state === "success" ? (
        <div className={styles.submitSuccess}>✅ {message}</div>
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
