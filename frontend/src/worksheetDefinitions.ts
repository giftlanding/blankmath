import { z } from "zod";

export const problemCountOptions = [10, 20, 30, 50] as const;
export const sheetCountOptions = Array.from({ length: 50 }, (_, index) => index + 1);
export const digitOptions = ["1d", "2d", "3d", "l12", "l20"] as const;
export const layoutOptions = ["horizontal", "vertical"] as const;

type SelectControl = {
  id: string;
  label: string;
  type: "select";
  options: readonly (string | number)[];
  defaultValue: string | number;
};

type CheckboxControl = {
  id: string;
  label: string;
  type: "checkbox";
  defaultValue: boolean;
};

type NumberControl = {
  id: string;
  label: string;
  type: "number";
  min: number;
  max: number;
  defaultValue: number;
};

export type WorksheetControl = SelectControl | CheckboxControl | NumberControl;

export type WorksheetDefinition = {
  id: string;
  path: string;
  title: string;
  category: "Addition & Subtraction" | "Multiplication & Division" | "Comparison";
  examples: string[];
  controls: WorksheetControl[];
};

const problemCount = (defaultValue = 20): SelectControl => ({
  id: "problemCount",
  label: "Problems",
  type: "select",
  options: problemCountOptions,
  defaultValue,
});

const sheetCount = (): SelectControl => ({
  id: "sheetCount",
  label: "Sheets",
  type: "select",
  options: sheetCountOptions,
  defaultValue: 1,
});

const layout = (defaultValue: "horizontal" | "vertical"): SelectControl => ({
  id: "layout",
  label: "Layout",
  type: "select",
  options: layoutOptions,
  defaultValue,
});

const digits = (defaultValue = "1d"): SelectControl => ({
  id: "digits",
  label: "Numbers",
  type: "select",
  options: digitOptions,
  defaultValue,
});

const rangeControls = (): WorksheetControl[] => [
  { id: "from", label: "From", type: "number", min: 0, max: 10000, defaultValue: 0 },
  { id: "to", label: "To", type: "number", min: 0, max: 10000, defaultValue: 20 },
];

const smallerOperandControl = (label: string): CheckboxControl => ({
  id: "smallOperandLessThan10",
  label,
  type: "checkbox",
  defaultValue: false,
});

const answerKeyControl = (): CheckboxControl => ({
  id: "includeAnswerKey",
  label: "Answer key",
  type: "checkbox",
  defaultValue: false,
});

const rangeWorksheetControls = (
  defaultLayout: "horizontal" | "vertical",
  restrictionLabel?: string,
  includeAnswerKey = false,
): WorksheetControl[] => [
  problemCount(),
  sheetCount(),
  layout(defaultLayout),
  ...rangeControls(),
  ...(restrictionLabel ? [smallerOperandControl(restrictionLabel)] : []),
  ...(includeAnswerKey ? [answerKeyControl()] : []),
];

const digitWorksheetControls = (defaultLayout: "horizontal" | "vertical"): WorksheetControl[] => [
  problemCount(),
  sheetCount(),
  digits(),
  layout(defaultLayout),
];

export const worksheets: WorksheetDefinition[] = [
  {
    id: "addition",
    path: "/addition",
    title: "Addition",
    category: "Addition & Subtraction",
    examples: ["12 + 9 = ?"],
    controls: rangeWorksheetControls("vertical", "Smaller addend under 10"),
  },
  {
    id: "minus",
    path: "/minus",
    title: "Minus",
    category: "Addition & Subtraction",
    examples: ["12 - 9 = ?"],
    controls: rangeWorksheetControls("vertical", "Subtrahend under 10"),
  },
  {
    id: "mixed_add_minus",
    path: "/mixed_add_minus",
    title: "Mixed Addition and Subtraction",
    category: "Addition & Subtraction",
    examples: ["12 + 9 = ?", "12 - 9 = ?"],
    controls: rangeWorksheetControls("vertical", "Smaller operand under 10"),
  },
  {
    id: "additionmn",
    path: "/additionmn",
    title: "Addition Missing Number",
    category: "Addition & Subtraction",
    examples: ["7 + ? = 15", "? + 3 = 12"],
    controls: rangeWorksheetControls("horizontal", "Smaller addend under 10"),
  },
  {
    id: "minusmn",
    path: "/minusmn",
    title: "Minus Missing Number",
    category: "Addition & Subtraction",
    examples: ["7 - ? = 5", "? - 3 = 12"],
    controls: rangeWorksheetControls("horizontal", "Subtrahend under 10"),
  },
  {
    id: "mixed_add_minus_mn",
    path: "/mixed_add_minus_mn",
    title: "Mixed Addition and Subtraction Missing Number",
    category: "Addition & Subtraction",
    examples: ["7 + ? = 15", "? - 3 = 12"],
    controls: rangeWorksheetControls("horizontal", "Smaller operand under 10", true),
  },
  {
    id: "add_three_numbers",
    path: "/add_three_numbers",
    title: "Add Three Numbers",
    category: "Addition & Subtraction",
    examples: ["7 + 8 + 12 = ?"],
    controls: [problemCount(), sheetCount(), digits()],
  },
  {
    id: "add_minus_three_numbers",
    path: "/add_minus_three_numbers",
    title: "Add and Subtract Three Numbers",
    category: "Addition & Subtraction",
    examples: ["17 - 8 + 7 = ?"],
    controls: [problemCount(), sheetCount(), digits()],
  },
  {
    id: "add_three_numbers_mn",
    path: "/add_three_numbers_mn",
    title: "Add Three Numbers Missing Number",
    category: "Addition & Subtraction",
    examples: ["7 + ? + 8 = 20"],
    controls: [problemCount(), sheetCount(), digits()],
  },
  {
    id: "multiplication",
    path: "/multiplication",
    title: "Multiplication",
    category: "Multiplication & Division",
    examples: ["8 x 9 = ?"],
    controls: digitWorksheetControls("vertical"),
  },
  {
    id: "division",
    path: "/division",
    title: "Division",
    category: "Multiplication & Division",
    examples: ["8 / 2 = ?"],
    controls: digitWorksheetControls("horizontal"),
  },
  {
    id: "mixed_times_divide",
    path: "/mixed_times_divide",
    title: "Mixed Multiplication and Division",
    category: "Multiplication & Division",
    examples: ["8 x 9 = ?", "8 / 2 = ?"],
    controls: digitWorksheetControls("horizontal"),
  },
  {
    id: "multiplicationmn",
    path: "/multiplicationmn",
    title: "Multiplication Missing Number",
    category: "Multiplication & Division",
    examples: ["8 x ? = 72"],
    controls: digitWorksheetControls("horizontal"),
  },
  {
    id: "division_mn",
    path: "/division_mn",
    title: "Division Missing Number",
    category: "Multiplication & Division",
    examples: ["8 / ? = 2", "? / 4 = 3"],
    controls: digitWorksheetControls("horizontal"),
  },
  {
    id: "mixed_times_divide_mn",
    path: "/mixed_times_divide_mn",
    title: "Mixed Multiplication and Division Missing Number",
    category: "Multiplication & Division",
    examples: ["8 x ? = 72", "? / 4 = 3"],
    controls: digitWorksheetControls("horizontal"),
  },
  {
    id: "greater_than_less_than",
    path: "/greater_than_less_than",
    title: "Comparision",
    category: "Comparison",
    examples: ["12 __ 9"],
    controls: [problemCount(10), sheetCount(), digits("l20")],
  },
];

export const worksheetById = new Map(worksheets.map((worksheet) => [worksheet.id, worksheet]));

export function defaultsForWorksheet(definition: WorksheetDefinition): Record<string, string | number | boolean> {
  return Object.fromEntries(definition.controls.map((control) => [control.id, control.defaultValue]));
}

export function schemaForWorksheet(definition: WorksheetDefinition) {
  const shape: Record<string, z.ZodType> = {};

  for (const control of definition.controls) {
    if (control.type === "checkbox") {
      shape[control.id] = z.boolean();
    } else if (control.type === "number") {
      shape[control.id] = z.coerce.number().min(control.min).max(control.max);
    } else {
      shape[control.id] = z.union([z.string(), z.coerce.number()]);
    }
  }

  return z.object(shape).refine((options) => {
    if ("from" in options && "to" in options) {
      return Number(options.from) < Number(options.to);
    }
    return true;
  }, {
    message: "From must be less than To.",
    path: ["to"],
  });
}
