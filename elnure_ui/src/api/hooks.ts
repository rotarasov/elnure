import { useState, useEffect } from "react";
import { get, ApiError } from ".";
import Student from "../data/student";
import { getApplicationWindows } from "./core";
import { getMe } from "./users";
import { convertFromApi } from "./utils";

export function useGet<T>(
  endpoint: string,
  data = {},
  options = {}
): [boolean, T | null, string[]] {
  const [inProgress, setInProgress] = useState(false);
  const [result, setResult] = useState<T | null>(null);
  const [errors, setErrors] = useState<string[]>([]);

  useEffect(() => {
    async function fetchData() {
      setInProgress(true);

      try {
        return await get(endpoint, data, options);
      } catch (e) {
        if ((e as ApiError).code >= 500) {
          setErrors(["Internal Error"]);
        } else {
          setErrors((e as ApiError).body);
        }
      }

      setInProgress(false);
    }
    fetchData().then((result) => setResult(convertFromApi(result) as T | null));
  }, [endpoint]);

  return [inProgress, result, errors];
}

export const useUser = async (): Promise<Student> => {
  let jsonUser = localStorage.getItem("user") || "";
  if (!jsonUser) {
    const jsonResp = await getMe();
    jsonUser = JSON.stringify(jsonResp);
    localStorage.setItem("user", jsonUser);
  }
  return JSON.parse(jsonUser);
};

export const useApplicationWindow = async () => {
  let jsonApplicationWindow = localStorage.getItem("appwindow") || "null";
  if (!jsonApplicationWindow) {
    const jsonResp = await getApplicationWindows();
    jsonApplicationWindow = JSON.stringify(jsonResp[0]);
    localStorage.setItem("appwindow", jsonApplicationWindow);
  }
  return JSON.parse(jsonApplicationWindow);
};
