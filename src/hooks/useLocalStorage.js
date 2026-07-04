import { useEffect, useState } from "react";

const PREFIX = "tauaBar:";

function readStoredValue(key, initialValue) {
  try {
    const raw = window.localStorage.getItem(PREFIX + key);
    return raw !== null ? JSON.parse(raw) : initialValue;
  } catch {
    return initialValue;
  }
}

export function useLocalStorage(key, initialValue) {
  const [value, setValue] = useState(() => readStoredValue(key, initialValue));

  useEffect(() => {
    window.localStorage.setItem(PREFIX + key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue];
}

export function clearLocalStorageKeys(keys) {
  keys.forEach((key) => window.localStorage.removeItem(PREFIX + key));
}
