import { afterEach, describe, expect, it, vi } from "vitest";
import { generateWorksheet, getGoogleAnalyticsClientId } from "./api";

describe("generateWorksheet", () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it("reports empty API responses without throwing a JSON parse error", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response("", { status: 404 })));

    await expect(generateWorksheet({
      worksheetType: "division",
      options: {
        problemCount: 10,
        sheetCount: 1,
        digits: "1d",
        layout: "long_division",
      },
    })).rejects.toThrow("empty response (HTTP 404)");
  });

  it("extracts the GA client id from the analytics cookie", () => {
    vi.stubGlobal("document", {
      cookie: "_ga=GA1.1.1234567890.9876543210",
    });

    expect(getGoogleAnalyticsClientId()).toBe("1234567890.9876543210");
  });
});
