import { BASE_API_URL, BASE_FRONTEND_URL, VERSION } from "../constants";
import redirectToGoogleSSO from "./sso";

export enum StatusCode {
  SUCCESS = 200,
  CREATED = 201,
  UNAUTHENTICATED = 401,
}

export class ApiError extends Error {
  code: number;
  body: any;

  constructor(code: number, body?: any) {
    super(`API Error: code ${code}; body ${body}`);

    this.code = code;
    this.body = body;

    Object.setPrototypeOf(this, ApiError.prototype);
  }
}

const DEFAULT_OPTIONS = {
  headers: {
    "Content-Type": "application/json",
  },
  credentials: "include",
};

function getUrl(endpoint: string) {
  return `${BASE_API_URL}/api/${VERSION}/${endpoint}`;
}

export async function request(endpoint: string, options = {}) {
  const url = getUrl(endpoint);
  const resp = await fetch(url, options);
  const json = await resp.json();
  const { status } = resp;

  if (status === StatusCode.UNAUTHENTICATED) {
    // redirectToGoogleSSO(window.location.href);
    window.location.href = `${BASE_FRONTEND_URL}/login`;
  }

  if (status >= StatusCode.SUCCESS && status < 300) {
    return json;
  } else if (status >= 400 && status < 500) {
    throw new ApiError(status, json);
  } else if (status >= 500) {
    throw new ApiError(status);
  }
}

export function get<T = any>(
  endpoint: string,
  data = {},
  options = {}
): Promise<T> {
  if (data) {
    const params = new URLSearchParams(data);
    endpoint = `${endpoint}?${params.toString()}`;
  }
  return request(endpoint, { ...DEFAULT_OPTIONS, ...options, method: "GET" });
}

export function post<T = any>(
  endpoint: string,
  data = {},
  options = {}
): Promise<T> {
  return request(endpoint, {
    ...DEFAULT_OPTIONS,
    ...options,
    method: "POST",
    body: JSON.stringify(data),
  });
}
