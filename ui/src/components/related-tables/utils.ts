import fetchDot from "fetch-dot";

/**
 * Extracts all Nunjucks template variables used in a string
 * and returns an object containing their resolved values.
 *
 * Example:
 *  template: "http://url.com/{{kvkNummer}}?foo={{user.id}}"
 *  values: { kvkNummer: "123", user: { id: 5 } }
 *
 *  returns:
 *  { kvkNummer: "123", "user.id": 5 }
 */
export const pickTemplateValues = (template: string, values: Record<string, any>) => {
  // Matches: {{ kvkNummer }}, {{ user.id }}, {{ foo | lower }}  -> captures "kvkNummer", "user.id", "foo"
  const re = /{{\s*([^}|]+?)(?:\s*\|[^}]*)?\s*}}/g;

  const out: Record<string, any> = {};
  let match: RegExpExecArray | null;

  while ((match = re.exec(template)) !== null) {
    const key = match[1].trim();
    out[key] = fetchDot(key, values);
  }

  return out;
};
