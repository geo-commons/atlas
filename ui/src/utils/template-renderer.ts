import fetchDot from "fetch-dot";

type TemplateContext = Record<string, unknown>;

/** Matches a supported Atlas template expression without interpreting it as JavaScript. */
const TEMPLATE_EXPRESSION = /{{\s*(?<expression>[^}]+?)\s*}}/g;

/**
 * Matches a property path with an optional replacement pipe.
 *
 * Supported examples:
 * - `postcode`
 * - `postcode | replace(' ', '')`
 * - `postcode | replaceAll(' ', '')`
 */
const PIPE_EXPRESSION =
  /^(?<path>[A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)*)(?:\s*\|\s*(?<method>replace|replaceAll)\((?<arguments>.*)\))?$/;

/**
 * Splits replacement arguments on commas outside quoted text.
 *
 * @example
 * splitArguments("'(a,b)', 'c,d'") // ["'(a,b)'", " 'c,d'"]
 */
const splitArguments = (value: string): string[] => {
  const parts: string[] = [];
  let currentPart = "";
  let quote: "'" | '"' | null = null;
  let escaped = false;

  for (const character of value) {
    if (escaped) {
      currentPart += character;
      escaped = false;
      continue;
    }

    if (quote && character === "\\") {
      currentPart += character;
      escaped = true;
      continue;
    }

    if (character === "'" || character === '"') {
      quote = quote === character ? null : (quote ?? character);
      currentPart += character;
      continue;
    }

    if (!quote && character === ",") {
      parts.push(currentPart);
      currentPart = "";
      continue;
    }

    currentPart += character;
  }

  parts.push(currentPart);
  return parts;
};

/**
 * Converts a quoted replacement argument to its literal value.
 *
 * @example
 * parseStringArgument("'it\\'s'") // "it's"
 */
const parseStringArgument = (argument: string): string => {
  const value = argument.trim();
  const quote = value[0];

  if ((quote !== "'" && quote !== '"') || value.at(-1) !== quote) {
    return value;
  }

  return value.slice(1, -1).replace(/\\(['"\\])/g, "$1");
};

/**
 * Parses the two arguments used by `replace` and `replaceAll`.
 *
 * @param argumentsText The contents between the method parentheses.
 * @returns The search value followed by the replacement value.
 */
const parseReplacementArguments = (argumentsText: string): [string, string] => {
  const [search = "", replacement = ""] = splitArguments(argumentsText).map(parseStringArgument);
  return [search, replacement];
};

/**
 * Renders one property expression and its optional replacement pipe.
 *
 * Only `replace` and `replaceAll` are allowed. Expressions never execute
 * JavaScript, so the renderer works with a strict CSP.
 *
 * @param expression The text between `{{` and `}}`.
 * @param context Values available to the template.
 */
const renderExpression = (expression: string, context: TemplateContext): unknown => {
  const match = expression.trim().match(PIPE_EXPRESSION);

  if (!match?.groups) {
    return "";
  }

  const value = fetchDot(match.groups.path, context);

  if (!match.groups.method || typeof value !== "string") {
    return value;
  }

  const [search, replacement] = parseReplacementArguments(match.groups.arguments);
  return match.groups.method === "replaceAll"
    ? value.replaceAll(search, replacement)
    : value.replace(search, replacement);
};

/**
 * Renders a text, URL, CQL, or Markdown template.
 *
 * @example
 * renderTemplate("/places/{{ postcode | replace(' ', '') }}", { postcode: "1234 AB" })
 * // "/places/1234AB"
 *
 * @param template The configured template string.
 * @param context Values available to the template.
 */
export const renderTemplate = (template: string | null | undefined, context: TemplateContext = {}): string => {
  if (!template) {
    return "";
  }

  return template.replace(TEMPLATE_EXPRESSION, (_match, expression: string) => {
    const value = renderExpression(expression, context);
    return value == null ? "" : String(value);
  });
};

/**
 * Renders template strings in a parsed JSON value without changing its shape.
 *
 * Only string values are rendered. JSON object keys and unquoted values are
 * intentionally left as configured, so a request body remains valid JSON
 * before template rendering starts.
 *
 * @param value A JSON value from a request body.
 * @param context Values available to the template.
 */
const renderJsonValue = (value: unknown, context: TemplateContext): unknown => {
  if (typeof value === "string") {
    return renderTemplate(value, context);
  }

  if (Array.isArray(value)) {
    return value.map((item) => renderJsonValue(item, context));
  }

  if (value && typeof value === "object") {
    return Object.fromEntries(Object.entries(value).map(([key, item]) => [key, renderJsonValue(item, context)]));
  }

  return value;
};

/**
 * Renders a JSON request body and serializes it after interpolation.
 *
 * The configured template must already be valid JSON. Place expressions in
 * string values, for example `{"postcode":"{{ postcode }}"}`. Expressions
 * in object keys and unquoted expressions such as `{"limit": {{ limit }}}`
 * are not supported.
 *
 * Parsing before rendering ensures values such as `A "quoted" name` remain
 * valid JSON instead of being inserted into JSON text verbatim.
 *
 * @param template A JSON object or legacy JSON string.
 * @param context Values available to the template.
 */
export const renderJsonTemplate = (template: unknown, context: TemplateContext = {}): string => {
  const jsonValue = typeof template === "string" ? JSON.parse(template) : template;
  return JSON.stringify(renderJsonValue(jsonValue, context));
};
