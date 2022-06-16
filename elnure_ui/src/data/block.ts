import ElectiveCourse from "./electiveCourse";

export default interface Block {
  id?: number;
  name?: string;
  capacity?: number | null;
  mustChoose?: number;
  electiveCourses?: ElectiveCourse[];
}
