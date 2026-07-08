import { useCallback, useState } from "react";
import { login as loginRequest } from "../services/api.js";

const STORAGE_KEY = "tauaBar:auth";

function readStoredAuth() {
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    if (!parsed?.token || !parsed?.expiresAt) return null;
    if (new Date(parsed.expiresAt) <= new Date()) {
      window.localStorage.removeItem(STORAGE_KEY);
      return null;
    }
    return parsed;
  } catch {
    return null;
  }
}

export function useAuth() {
  const [auth, setAuth] = useState(readStoredAuth);

  const login = useCallback(async (nome, pin) => {
    const data = await loginRequest(nome, pin);
    const session = { token: data.access_token, nome: data.nome, expiresAt: data.expires_at };
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(session));
    setAuth(session);
    return session;
  }, []);

  const logout = useCallback(() => {
    window.localStorage.removeItem(STORAGE_KEY);
    setAuth(null);
  }, []);

  return { auth, login, logout };
}
