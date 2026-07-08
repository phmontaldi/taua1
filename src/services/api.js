import { SECTIONS } from "../data/checklistData.js";
import { AUDIT, SCALE } from "../data/auditData.js";
import { getClassification } from "../utils/status.js";

const API_URL = import.meta.env.VITE_API_URL;

export class ApiError extends Error {
  constructor(message, { status, body } = {}) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.body = body;
  }
}

export class AuthError extends ApiError {}
export class DuplicateTurnoError extends ApiError {}

// Mesma fórmula do backend: services/scoring.py::_pct -> round(n/d*100, 2)
function pct(numerator, denominator) {
  if (!denominator) return 0;
  return Math.round((numerator / denominator) * 100 * 100) / 100;
}

function buildChecklistPayload(checked) {
  const items = SECTIONS.flatMap((section) =>
    section.items.map((item) => ({
      id: item.id,
      label: item.label,
      section_id: section.id,
      section_title: section.title,
      critical: !!item.critical,
      checked: !!checked[item.id],
    }))
  );

  const sections = SECTIONS.map((section) => {
    const total = section.items.length;
    const done = section.items.filter((item) => checked[item.id]).length;
    return { id: section.id, title: section.title, total, done, pct: pct(done, total) };
  });

  const total = items.length;
  const done = items.filter((item) => item.checked).length;
  const criticalItems = items.filter((item) => item.critical);
  const criticalDone = criticalItems.filter((item) => item.checked).length;

  return {
    total,
    done,
    critical_total: criticalItems.length,
    critical_done: criticalDone,
    pct: pct(done, total),
    critical_pct: pct(criticalDone, criticalItems.length),
    sections,
    items,
  };
}

function buildAuditoriaPayload(scores) {
  const items = AUDIT.flatMap((section) =>
    section.items.map((item) => {
      const score = scores[item.id] || 0;
      return {
        id: item.id,
        label: item.label,
        section_id: section.id,
        section_title: section.title,
        score,
        max: item.max,
        pct: pct(score, item.max),
      };
    })
  );

  const sections = AUDIT.map((section) => {
    const score = section.items.reduce((sum, item) => sum + (scores[item.id] || 0), 0);
    return { id: section.id, title: section.title, score, max: section.max, pct: pct(score, section.max) };
  });

  const total = items.reduce((sum, item) => sum + item.score, 0);
  const max = items.reduce((sum, item) => sum + item.max, 0);

  return {
    total,
    pct: pct(total, max),
    classification: getClassification(total, SCALE).label,
    sections,
    items,
  };
}

export function buildTurnoPayload({ checked, scores, date, bar, emocionador, statusLabel }) {
  return {
    date,
    bar,
    emocionador,
    status: statusLabel,
    submitted_at: new Date().toISOString(),
    checklist: buildChecklistPayload(checked),
    auditoria: buildAuditoriaPayload(scores),
  };
}

async function request(path, { method = "GET", body, token } = {}) {
  if (!API_URL) {
    throw new ApiError("VITE_API_URL não configurada. Defina a URL da API antes de enviar.");
  }

  const headers = { "Content-Type": "application/json" };
  if (token) headers.Authorization = `Bearer ${token}`;

  let response;
  try {
    response = await fetch(`${API_URL}${path}`, {
      method,
      headers,
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });
  } catch {
    throw new ApiError("Não foi possível conectar ao servidor. Verifique sua conexão.");
  }

  let data = null;
  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    if (response.status === 401) {
      throw new AuthError(data?.detail || "Sessão expirada. Faça login novamente.", {
        status: 401,
        body: data,
      });
    }
    if (response.status === 409) {
      throw new DuplicateTurnoError(
        data?.message || "Já existe uma conferência enviada para este bar e data.",
        { status: 409, body: data }
      );
    }
    throw new ApiError(data?.message || data?.detail || `Erro ao comunicar com o servidor (${response.status}).`, {
      status: response.status,
      body: data,
    });
  }

  return data;
}

export function login(nome, pin) {
  return request("/api/v1/auth/login", { method: "POST", body: { nome, pin } });
}

export function submitTurno(state, token) {
  return request("/api/v1/turnos", { method: "POST", body: buildTurnoPayload(state), token });
}
