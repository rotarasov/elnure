import { BASE_API_URL, VERSION } from "src/constants";
import redirectToGoogleSSO from "src/api/sso";

export enum StatusCode {
  SUCCESS = 200,
  CREATED = 201,
  UNAUTHENTICATED = 401,
}

export type Errors = Record<string, string[]>;

const DEFAULT_OPTIONS = {
  headers: {
    "Content-Type": "application/json",
  },
};

function getUrl(endpoint: string) {
  return `${BASE_API_URL}/api/${VERSION}/${endpoint}`;
}

export async function request(enddpoint: string, options = {}) {
  const url = getUrl(enddpoint);
  const resp = await fetch(url, options);
  const json = await resp.json();
  const { status } = resp;

  if (status === StatusCode.UNAUTHENTICATED) {
    redirectToGoogleSSO(window.location.href);
  }

  if (status >= StatusCode.SUCCESS && status < 300) {
    return json;
  } else {
    throw new Error(`API Error: ${json}`);
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
