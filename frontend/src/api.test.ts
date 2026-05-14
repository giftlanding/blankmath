import { afterEach, describe, expect, it, vi } from "vitest";
import { generateWorksheet } from "./api";

describe("generateWorksheet", () => {
  afterEach(() => {
    vi.restoreAllMocks();
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
});
