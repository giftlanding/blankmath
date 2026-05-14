import { expect, test } from "@playwright/test";

test("division generation shows a friendly error when the API returns an empty 404", async ({ page }) => {
  await page.goto("/division");

  await page.getByLabel("Layout").selectOption("long_division");
  await page.getByRole("button", { name: /create pdf/i }).click();

  await expect(page.getByText("Worksheet generation failed with an empty response (HTTP 404).")).toBeVisible();
  await expect(page.getByText(/Unexpected end of JSON input/i)).toHaveCount(0);
});
