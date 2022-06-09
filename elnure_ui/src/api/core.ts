import { Errors, get, post } from "src/api/index";
import Student from "src/data/student";
import Semester from "src/data/semester";
import { convertFromApi } from "src/api/utils";
import Choice from "src/data/choice";

export async function getSemestersInfo(
  student: Student,
  options = {}
): Promise<Semester[] | Errors> {
  return convertFromApi(
    await get<Semester[] | Errors>("semesters", { for_student: student.id })
  ) as Semester[];
}

export async function createChoice(
  choice: Choice,
  options = {}
): Promise<Choice | Errors> {
  return convertFromApi(
    await post<Choice | Errors>("choices", choice, options)
  );
}
