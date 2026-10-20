import fetchDot from "fetch-dot";

type TemplateContext = Record<string, unknown>;

/**
 * Template syntax supported by this module:
 *
 * - Property values: `{{ address.city }}`
 * - String methods: `{{ postcode.replaceAll(' ', '') }}`
 * - String methods without arguments: `{{ name.toUpperCase() }}`
 *
 * Expressions are read as data. They are never turned into JavaScript code.
 */
const TEMPLATE_EXPRESSION = /{{\s*([^}]+?)\s*}}/g;
const STRING_METHOD_EXPRESSION =
  /^(?<path>[A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)*)\.(?<method>replaceAll|replace|toLowerCase|toUpperCase|trim)\((?<arguments>.*)\)$/;

/**
 * Split method arguments at commas that are outside quoted text.
 *
 * For example, `replace('a,b', 'c,d')` returns two arguments. The commas in
 * the quoted values stay intact.
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

/** Remove surrounding quotes from one method argument. */
const parseStringArgument = (argument: string): string => {
  const value = argument.trim();
  const quote = value[0];

  if ((quote !== "'" && quote !== '"') || value.at(-1) !== quote) {
    return value;
  }

  return value.slice(1, -1).replace(/\\(['"\\])/g, "$1");
};

/** Read comma-separated method arguments while retaining quoted punctuation. */
const parseStringArguments = (argumentsText: string): string[] =>
  splitArguments(argumentsText).map(parseStringArgument);

/** Resolve a property path or one of the explicitly supported string methods. */
const resolveValue = (expression: string, context: TemplateContext): unknown => {
  const normalizedExpression = expression.trim();
  const methodMatch = normalizedExpression.match(STRING_METHOD_EXPRESSION);

  if (!methodMatch?.groups) {
    return fetchDot(normalizedExpression, context);
  }

  const value = fetchDot(methodMatch.groups.path, context);

  if (typeof value !== "string") {
    return "";
  }

  const [search = "", replacement = ""] = parseStringArguments(methodMatch.groups.arguments);

  switch (methodMatch.groups.method) {
    case "replaceAll":
      return value.replaceAll(search, replacement);
    case "replace":
      return value.replace(search, replacement);
    case "toLowerCase":
      return value.toLowerCase();
    case "toUpperCase":
      return value.toUpperCase();
    case "trim":
      return value.trim();
  }
};

/** Render {{ property.path }} placeholders without evaluating JavaScript. */
export const renderTemplate = (template: string | null | undefined, context: TemplateContext = {}): string => {
  if (!template) {
    return "";
  }

  return template.replace(TEMPLATE_EXPRESSION, (_match, expression: string) => {
    const value = resolveValue(expression, context);
    return value == null ? "" : String(value);
  });
};

/** Render every string in a parsed JSON value while preserving its JSON structure. */
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

/** Render a JSON request body and serialize it after values have been inserted. */
export const renderJsonTemplate = (template: unknown, context: TemplateContext = {}): string => {
  const jsonValue = typeof template === "string" ? JSON.parse(template) : template;
  return JSON.stringify(renderJsonValue(jsonValue, context));
};
