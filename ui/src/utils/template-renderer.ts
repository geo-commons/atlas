import fetchDot from "fetch-dot";

type TemplateContext = Record<string, unknown>;

const TEMPLATE_EXPRESSION = /{{\s*([^}]+?)\s*}}/g;
const REPLACE_METHOD_EXPRESSION =
  /^(?<path>[A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)*)\.(?<method>replaceAll|replace)\(\s*(['"])(?<search>.*?)\3\s*,\s*(['"])(?<replacement>.*?)\5\s*\)$/;

/** Resolve a property path or an allowed replace method from the supplied data. */
const resolveValue = (expression: string, context: TemplateContext): unknown => {
  const normalizedExpression = expression.trim();
  const replaceMethodMatch = normalizedExpression.match(REPLACE_METHOD_EXPRESSION);

  if (replaceMethodMatch?.groups) {
    const value = fetchDot(replaceMethodMatch.groups.path, context);

    if (typeof value !== "string") {
      return "";
    }

    const search = replaceMethodMatch.groups.search;
    const replacement = replaceMethodMatch.groups.replacement;

    return replaceMethodMatch.groups.method === "replaceAll"
      ? value.replaceAll(search, replacement)
      : value.replace(search, replacement);
  }

  return fetchDot(normalizedExpression, context);
};

/** Apply a supported pipe filter to a rendered value. Unknown filters leave the value unchanged. */
const applyFilter = (value: unknown, filter: string): unknown => {
  const [name, ...argumentsText] = filter.trim().split(/\s*\(\s*|\s*\)\s*/);
  const argumentValues = argumentsText
    .join("")
    .split(",")
    .filter(Boolean)
    .map((argument) => argument.trim().replace(/^(['"])(.*)\1$/, "$2"));
  const stringValue = String(value ?? "");

  switch (name) {
    case "lower":
      return stringValue.toLowerCase();
    case "upper":
      return stringValue.toUpperCase();
    case "trim":
      return stringValue.trim();
    case "replace":
      return stringValue.replaceAll(argumentValues[0] ?? "", argumentValues[1] ?? "");
    default:
      return value;
  }
};

/** Render {{ property.path }} placeholders using the provided data without running generated JavaScript. */
export const renderTemplate = (template: string | null | undefined, context: TemplateContext = {}): string => {
  if (!template) {
    return "";
  }

  return template.replace(TEMPLATE_EXPRESSION, (_match, expression: string) => {
    const [valueExpression, ...filters] = expression.split("|");
    const value = filters.reduce(
      (currentValue, filter) => applyFilter(currentValue, filter),
      resolveValue(valueExpression, context),
    );

    return value == null ? "" : String(value);
  });
};
