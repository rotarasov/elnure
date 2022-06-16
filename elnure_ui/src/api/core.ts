import { ApiError, get, post } from ".";
import Student from "../data/student";
import Semester from "../data/semester";
import { convertFromApi } from "./utils";
import Choice from "../data/choice";
import ApplicationWindow from "../data/applicationWindow";
import { FormationResult } from "../data/formationResult";

export async function createChoice(
  choice: Choice,
  options = {}
): Promise<Choice> {
  return convertFromApi(
    await post<Choice>("choices", choice, options)
  ) as Choice;
}

export async function getApplicationWindows(
  options = {}
): Promise<ApplicationWindow[]> {
  return convertFromApi(
    await get<ApplicationWindow[]>("ref/appwindows", {}, options)
  ) as ApplicationWindow[];
}

export async function getFormationResults(
  applicationWindowId: number | string,
  options = {}
): Promise<FormationResult[]> {
  return await get<FormationResult[]>(
    `appwindows/${applicationWindowId}/formation-results`,
    {},
    options
  );
}
