import { afterEach, describe, expect, it, vi } from "vitest";
import { apiFetch, ApiError, ApiMethod } from "@/utils/api-helpers";

describe("apiFetch", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("uses detail from JSON error responses", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify({ detail: "Deze categorie kan niet worden verwijderd" }), {
          status: 400,
          statusText: "Bad Request",
          headers: { "Content-Type": "application/json" },
        }),
      ),
    );

    await expect(apiFetch("/atlas/api/v1/categories/1/", ApiMethod.DELETE)).rejects.toMatchObject({
      message: "Deze categorie kan niet worden verwijderd",
      statusCode: 400,
      httpMethod: ApiMethod.DELETE,
    } satisfies Partial<ApiError>);
  });

  it("falls back to status text when the response body is not JSON", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response("Bad request", {
          status: 400,
          statusText: "Bad Request",
        }),
      ),
    );

    await expect(apiFetch("/atlas/api/v1/categories/1/", ApiMethod.DELETE)).rejects.toMatchObject({
      message: "Bad Request",
      statusCode: 400,
      httpMethod: ApiMethod.DELETE,
    } satisfies Partial<ApiError>);
  });
});
