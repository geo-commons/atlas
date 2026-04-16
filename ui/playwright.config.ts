import { defineConfig, devices } from "playwright/test";

const isCI = !!process.env.CI;
const baseURL = process.env.E2E_BASE_URL ?? "http://localhost:8000";
const backendURL = new URL(baseURL);
const backendHost = backendURL.hostname;
const backendPort = backendURL.port || (backendURL.protocol === "https:" ? "443" : "80");
const backendHealthcheckURL = process.env.E2E_HEALTHCHECK_URL ?? `${backendURL.origin}/atlas/`;
const frontendHost = process.env.E2E_UI_HOST ?? "localhost";
const frontendPort = process.env.E2E_UI_PORT ?? "5173";
const storageStatePath = process.env.E2E_STORAGE_STATE;
const skipWebServer = process.env.PW_SKIP_WEBSERVER === "1";

export default defineConfig({
  testDir: "./tests/e2e",
  outputDir: "test-results",
  fullyParallel: false,
  forbidOnly: isCI,
  retries: isCI ? 2 : 0,
  workers: isCI ? 2 : undefined,
  timeout: 45_000,
  expect: {
    timeout: 10_000,
  },
  reporter: [
    ["list"],
    ["html", { open: "never", outputFolder: "playwright-report" }],
  ],
  use: {
    baseURL,
    headless: true,
    locale: "nl-NL",
    trace: "on-first-retry",
    video: "retain-on-failure",
    screenshot: "only-on-failure",
    actionTimeout: 10_000,
    navigationTimeout: 20_000,
    storageState: storageStatePath || undefined,
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
  webServer: skipWebServer
    ? undefined
    : [
        {
          command: `python3 manage.py runserver ${backendHost}:${backendPort}`,
          cwd: "..",
          url: backendHealthcheckURL,
          timeout: 120_000,
          reuseExistingServer: !isCI,
        },
        {
          command: `pnpm run dev -- --host ${frontendHost} --port ${frontendPort}`,
          cwd: ".",
          url: `http://${frontendHost}:${frontendPort}`,
          timeout: 120_000,
          reuseExistingServer: !isCI,
        },
      ],
});
