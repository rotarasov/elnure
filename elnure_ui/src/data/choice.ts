import ApplicationWindow from "./applicationWindow";
import { Strategy } from "./strategies";
import DefaultStrategyChoiceValue from "./strategies/default";
import Student from "./student";

export default interface Choice {
  student: Student | number;
  applicationWindow: ApplicationWindow | number;
  value: DefaultStrategyChoiceValue;
  strategy: Strategy;
  semester: number;
}
