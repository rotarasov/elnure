import { useState, useEffect } from "react";
import { get } from ".";
import Student from "src/data/student";

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
        setResult(await get(endpoint, data, options));
      } catch (e) {
        setErrors([(e as Error).message]);
      }

      setInProgress(false);
    }
    fetchData();
  }, [endpoint]);

  return [inProgress, result, errors];
}

export const useUser = async (): Promise<Student | null> => {
  let jsonUser = localStorage.getItem("user") || "";
  if (!jsonUser) {
    const jsonResp = await get("me");
    jsonUser = jsonResp;
    localStorage.setItem("user", jsonUser);
  }
  return JSON.parse(jsonUser);
};
