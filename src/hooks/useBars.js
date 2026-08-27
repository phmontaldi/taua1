import { useEffect, useState } from "react";
import { fetchBares } from "../services/api.js";

const STORAGE_KEY = "tauaBar:bares";

// Semente para o primeiro uso offline, antes de qualquer resposta da API.
// A fonte da verdade é a tabela `bar` no banco (GET /api/v1/bares).
const DEFAULT_BARS = [
  { slug: "piscina", rotulo: "Bar da Piscina" },
  { slug: "sport_bar", rotulo: "Sport Bar" },
  { slug: "ondas_1", rotulo: "Bar Ondas 1" },
  { slug: "rooftop", rotulo: "Rooftop" },
  { slug: "nigori", rotulo: "Nigori" },
  { slug: "coppolla", rotulo: "Coppolla" },
  { slug: "beach_club", rotulo: "Beach Club" },
];

function readCachedBars() {
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed) || parsed.length === 0) return null;
    if (!parsed.every((b) => b?.slug && b?.rotulo)) return null;
    return parsed;
  } catch {
    return null;
  }
}

export function useBars(token) {
  const [bars, setBars] = useState(() => readCachedBars() ?? DEFAULT_BARS);

  useEffect(() => {
    if (!token) return undefined;
    let cancelled = false;

    fetchBares(token)
      .then((data) => {
        if (cancelled || !Array.isArray(data) || data.length === 0) return;
        setBars(data);
        try {
          window.localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
        } catch {
          // cache indisponível: segue com o estado em memória
        }
      })
      .catch(() => {
        // rede falhou: mantém a lista em cache para o app seguir offline
      });

    return () => {
      cancelled = true;
    };
  }, [token]);

  return bars;
}
