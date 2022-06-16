import { ApiError, get, post } from ".";
import Student from "../data/student";
import Semester from "../data/semester";
import { convertFromApi } from "./utils";
import Choice from "../data/choice";
import ApplicationWindow from "../data/applicationWindow";

export async function getSemestersInfo(
  student: Student,
  options = {}
): Promise<Semester[]> {
  return convertFromApi(
    await get<Semester[]>("semesters", { for_student: student.id })
  ) as Semester[];
}

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
    await get<ApplicationWindow[]>("appwindows", options)
  ) as ApplicationWindow[];
}
