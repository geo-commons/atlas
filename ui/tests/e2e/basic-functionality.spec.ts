import { expect, test } from "playwright/test";

const MAP_URL = "/atlas/@126910.00,505834.00,13z/layers=/base=topografische-kaart-grijs";

test.describe("Basic functionality test", () => {
  test("Search and select the scholen layer check if it appears in the data panel", async ({ page }) => {
    await page.goto(MAP_URL);
    await page.locator("#layers-search").click();
    await page.locator("#layers-search").fill("scholen");
    await page.getByText("Scholen", { exact: true }).click();
    await page.getByTestId("toggle-data-panel").click();
    await expect(page.getByTestId("data-panel")).toContainText("Scholen");
  });
});
