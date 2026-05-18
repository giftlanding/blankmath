import { describe, expect, it } from "vitest";
import { defaultsForWorksheet, schemaForWorksheet, worksheetById, worksheets } from "./worksheetDefinitions";

const existingWorksheetIds = [
  "addition",
  "minus",
  "mixed_add_minus",
  "additionmn",
  "minusmn",
  "mixed_add_minus_mn",
  "add_three_numbers",
  "add_minus_three_numbers",
  "add_three_numbers_mn",
  "multiplication",
  "division",
  "mixed_times_divide",
  "multiplicationmn",
  "division_mn",
  "mixed_times_divide_mn",
  "greater_than_less_than",
  "fraction_reduce",
  "fraction_equivalent",
  "fraction_compare",
  "place_value_expanded_form",
  "place_value_standard_form",
  "place_value_digit_value",
  "distributive_property_near_numbers",
  "breaking_parentheses",
  "chicken_rabbit",
];

describe("worksheet definitions", () => {
  it("preserves the existing worksheet catalog", () => {
    expect(worksheets.map((worksheet) => worksheet.id)).toEqual(existingWorksheetIds);
  });

  it("has valid defaults for every worksheet schema", () => {
    for (const worksheet of worksheets) {
      const result = schemaForWorksheet(worksheet).safeParse(defaultsForWorksheet(worksheet));
      expect(result.success, worksheet.id).toBe(true);
    }
  });

  it("can look up every worksheet by id", () => {
    for (const worksheet of worksheets) {
      expect(worksheetById.get(worksheet.id)).toBe(worksheet);
    }
  });
});
