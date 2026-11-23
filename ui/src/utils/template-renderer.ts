import { Liquid } from "liquidjs";

type TemplateContext = Record<string, unknown>;

const liquid = new Liquid();
const htmlLiquid = new Liquid({ outputEscape: "escape" });
const cqlLiquid = new Liquid({
  outputEscape: (value: unknown) => String(value ?? "").replaceAll("'", "''"),
});

export const renderTemplate = (template: string | null | undefined, context: TemplateContext = {}): string =>
  liquid.parseAndRenderSync(template ?? "", context);

export const renderHtmlTemplate = (template: string | null | undefined, context: TemplateContext = {}): string =>
  htmlLiquid.parseAndRenderSync(template ?? "", context);

export const renderCqlTemplate = (template: string | null | undefined, context: TemplateContext = {}): string =>
  cqlLiquid.parseAndRenderSync(template ?? "", context);

export const renderJsonTemplate = (template: unknown, context: TemplateContext = {}): string => {
  const jsonValue = typeof template === "string" ? JSON.parse(template) : template;
  return JSON.stringify(jsonValue, (_key, value: unknown) =>
    typeof value === "string" ? liquid.parseAndRenderSync(value, context) : value,
  );
};
