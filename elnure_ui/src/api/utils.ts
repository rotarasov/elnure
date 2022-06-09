const isArray = function (a: any) {
  return Array.isArray(a);
};

const isObject = function (o: any) {
  return o === Object(o) && !isArray(o) && typeof o !== "function";
};

const toCamel = function (val: string) {
  return val.replace(/[_][a-z]/, (val: string) => {
    return val.toUpperCase().replace("_", "");
  });
};

const keysToCamel = function (o: any) {
  if (isObject(o)) {
    const res: Record<string, any> = {};

    Object.keys(o).forEach((k) => {
      res[toCamel(k)] = keysToCamel(o[k]);
    });

    return res;
  } else if (isArray(o)) {
    return o.map((i: any) => {
      return keysToCamel(i);
    });
  }
  return o;
};

export const convertFromApi = function (
  body: Record<string, any>
): Record<string, any> {
  return keysToCamel(body);
};
