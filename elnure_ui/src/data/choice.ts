import ApplicationWindow from "./applicationWindow";
import { Strategy } from "./strategies";
import DefaultStrategyValue from "./strategies/default";
import Student from "./student";

export default interface Choice {
  student: Student | number;
  applicationWindow: ApplicationWindow | number;
  value: DefaultStrategyValue;
  strategy: Strategy;
  semester: number;
}
