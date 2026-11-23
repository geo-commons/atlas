import { Liquid } from "liquidjs";

type TemplateContext = Record<string, unknown>;

const plainTextTemplateEngine = new Liquid();
const htmlTemplateEngine = new Liquid({ outputEscape: "escape" });

/**
 * Escape a value used inside a quoted CQL string.
 *
 * @param insertedValue - The value added to the CQL string.
 * @returns The value with apostrophes doubled.
 *
 * @example
 * ```ts
 * escapeCqlValue("O'Brien"); // "O''Brien"
 * ```
 */
const escapeCqlValue = (insertedValue: unknown): string => String(insertedValue ?? "").replaceAll("'", "''");

const cqlTemplateEngine = new Liquid({ outputEscape: escapeCqlValue });

/**
 * Fill values in a Liquid template for URLs and plain text.
 *
 * @param templateText - The template to render.
 * @param templateValues - The values available to the template.
 * @returns The rendered text.
 *
 * @example
 * ```ts
 * renderTemplate("{{ address.postcode | replace: ' ', '' }}", {
 *   address: { postcode: "1234 AB" },
 * }); // "1234AB"
 * ```
 */
export const renderTemplate = (templateText: string | null | undefined, templateValues: TemplateContext = {}): string =>
  plainTextTemplateEngine.parseAndRenderSync(templateText ?? "", templateValues);

/**
 * Fill values in a Liquid template and escape them for HTML.
 *
 * @param templateText - The template to render.
 * @param templateValues - The values available to the template.
 * @returns The rendered HTML text.
 *
 * @example
 * ```ts
 * renderHtmlTemplate("{{ label }}", { label: "<b>Hi</b>" }); // "&lt;b&gt;Hi&lt;/b&gt;"
 * ```
 */
export const renderHtmlTemplate = (
  templateText: string | null | undefined,
  templateValues: TemplateContext = {},
): string => htmlTemplateEngine.parseAndRenderSync(templateText ?? "", templateValues);

/**
 * Fill values in a CQL filter and escape apostrophes in those values.
 *
 * @param templateText - The CQL template to render.
 * @param templateValues - The values available to the template.
 * @returns The rendered CQL filter.
 *
 * @example
 * ```ts
 * renderCqlTemplate("name = '{{ name }}'", { name: "O'Brien" }); // "name = 'O''Brien'"
 * ```
 */
export const renderCqlTemplate = (
  templateText: string | null | undefined,
  templateValues: TemplateContext = {},
): string => cqlTemplateEngine.parseAndRenderSync(templateText ?? "", templateValues);

/**
 * Fill string values in a JSON request body.
 *
 * JSON.stringify escapes quotes in the rendered values so the body stays valid JSON.
 *
 * @param requestBody - A JSON value or text that contains a JSON value.
 * @param templateValues - The values available to the template.
 * @returns The rendered request body as JSON text.
 *
 * @example
 * ```ts
 * const body = renderJsonTemplate({ name: "{{ name }}" }, { name: 'A "quoted" name' });
 * JSON.parse(body); // { name: 'A "quoted" name' }
 * ```
 */
export const renderJsonTemplate = (requestBody: unknown, templateValues: TemplateContext = {}): string => {
  const parsedRequestBody = typeof requestBody === "string" ? JSON.parse(requestBody) : requestBody;

  /**
   * Render text values while JSON.stringify visits each value in the body.
   *
   * @param _key - The JSON key, which is not needed here.
   * @param fieldValue - The current JSON value.
   * @returns The rendered text or the unchanged value.
   */
  const renderJsonStringValue = (_key: string, fieldValue: unknown): unknown =>
    typeof fieldValue === "string" ? renderTemplate(fieldValue, templateValues) : fieldValue;

  return JSON.stringify(parsedRequestBody, renderJsonStringValue);
};
