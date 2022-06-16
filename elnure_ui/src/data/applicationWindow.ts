import Semester from "./semester";

export default interface ApplicationWindow {
  id?: number;
  startDate?: string;
  endDate?: string;
  semesters?: Semester[];
}
