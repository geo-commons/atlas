import { expect, test } from "playwright/test";

const MAP_URL = "/atlas/@126910.00,505834.00,13z/layers=/base=topografische-kaart-grijs";

test.describe("Atlas map smoke", () => {
  test("renders the main map viewer", async ({ page }) => {
    await page.goto(MAP_URL);

    await expect(page.getByTestId("app")).toBeVisible();
    await expect(page.getByTestId("zoom-in-button")).toBeVisible();
    await expect(page.getByTestId("zoom-out-button")).toBeVisible();
    await expect(page.getByTestId("more-options-button")).toBeVisible();
  });

  test("opens the more-options menu", async ({ page }) => {
    await page.goto(MAP_URL);

    await page.getByTestId("more-options-button").click();
    await expect(page.getByTestId("more-menu-embed")).toBeVisible();
    await expect(page.getByTestId("more-menu-help")).toBeVisible();
  });

  test("toggles the base-layers panel", async ({ page }) => {
    await page.goto(MAP_URL);

    await page.getByTestId("toggle-base-layers").click();
    await expect(page.locator("#baseLayers")).toBeVisible();
    await expect(page.getByLabel("Geen")).toBeVisible();
  });

  test("opens the layers panel and expands a category", async ({ page }) => {
    await page.goto(MAP_URL);

    await expect(page.locator("#layers")).toBeVisible();

    const firstCategoryToggle = page.locator("#layers .category-wrapper .expand-button").first();
    await expect(firstCategoryToggle).toBeVisible();
    await firstCategoryToggle.click();

    await expect(page.locator("#layers input[type='checkbox']").first()).toBeVisible();
  });

  test("can select a layer and show it in visible layers", async ({ page }) => {
    await page.goto(MAP_URL);

    const firstCategoryToggle = page.locator("#layers .category-wrapper .expand-button").first();
    await expect(firstCategoryToggle).toBeVisible();
    await firstCategoryToggle.click();

    const firstUncheckedLayer = page.locator("#layers input[type='checkbox']:not([disabled]):not(:checked)").first();
    await expect(firstUncheckedLayer).toBeVisible();
    const layerId = await firstUncheckedLayer.getAttribute("id");
    await page.locator(`#layers label[for='${layerId}']`).click();

    await page.getByTestId("toggle-visible-layers").click();
    await expect(page.locator("#visibleLayers")).toBeVisible();
    await expect(page.locator("[data-testid^='visible-layer-close-']").first()).toBeVisible();
  });
});
