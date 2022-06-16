import { get, post } from ".";
import Student from "../data/student";
import { convertFromApi } from "./utils";

export async function getMe(): Promise<Student> {
  return convertFromApi(await get("me"));
}

export async function plainLogin(data: {
  email: string;
  password: string;
}): Promise<Student> {
  return convertFromApi(await post("authenticate", data));
}
