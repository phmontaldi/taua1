import { useState } from "react";
import styles from "./Login.module.css";

export default function Login({ onLogin }) {
  const [nome, setNome] = useState("");
  const [pin, setPin] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await onLogin(nome, pin);
    } catch (err) {
      setError(err.message || "Não foi possível entrar. Tente novamente.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.screen}>
      <div className={styles.brand}>TAUÁ</div>
      <div className={styles.brandSub}>Resort & Convention</div>

      <form className={styles.card} onSubmit={handleSubmit}>
        <div className={styles.title}>Entrar na Conferência Diária</div>

        {error && <div className={styles.error}>{error}</div>}

        <div className={styles.field}>
          <span className={styles.fieldLabel}>Nome</span>
          <input
            type="text" className={styles.input} value={nome}
            onChange={(e) => setNome(e.target.value)} autoComplete="username"
            required
          />
        </div>

        <div className={styles.field}>
          <span className={styles.fieldLabel}>PIN</span>
          <input
            type="password" className={styles.input} value={pin}
            onChange={(e) => setPin(e.target.value)} autoComplete="current-password"
            inputMode="numeric" required
          />
        </div>

        <button type="submit" className={styles.submit} disabled={loading}>
          {loading ? "Entrando..." : "Entrar"}
        </button>
      </form>
    </div>
  );
}
