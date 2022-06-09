import InstructorAssignment from "./instructorAssignment";

export default interface ElectiveCourse {
  id?: number;
  name?: string;
  shortcut?: string;
  syllabus?: string;
  capaciy?: number | null;
  credits?: number;
  performaceAssessment?: string;
  instructors?: InstructorAssignment[];
}
