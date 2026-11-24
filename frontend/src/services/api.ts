const BASE_URL = import.meta.env.VITE_API_URL ?? "";

export class ApiError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

export function getToken() {
  return localStorage.getItem("plant_token") ?? "";
}

export function setToken(token: string) {
  localStorage.setItem("plant_token", token);
}

export function clearSession() {
  localStorage.removeItem("plant_token");
}

export async function apiRequest<T>(
  path: string,
  options: RequestInit = {},
  authenticated = true,
): Promise<T> {
  const headers = new Headers(options.headers);
  if (authenticated) {
    const token = getToken();
    if (token) headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${BASE_URL}${path}`, { ...options, headers });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    if (response.status === 401) clearSession();
    throw new ApiError(response.status, data.detail ?? data.message ?? "Yêu cầu thất bại");
  }
  return data as T;
}

export function jsonHeaders() {
  return { "Content-Type": "application/json" };
}
