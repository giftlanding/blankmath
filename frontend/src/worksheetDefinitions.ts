import { z } from "zod";

export const problemCountOptions = [10, 20, 30, 50] as const;
export const sheetCountOptions = Array.from({ length: 50 }, (_, index) => index + 1);
export const digitOptions = ["1d", "2d", "3d", "l12", "l20"] as const;
export const layoutOptions = ["horizontal", "vertical"] as const;
export const divisionLayoutOptions = ["equation", "long_division"] as const;
export const distributiveBaseOptions = ["near_10", "near_100", "mixed"] as const;
export const distributiveDirectionOptions = ["subtraction", "addition", "mixed"] as const;
export const distributiveDifficultyOptions = ["multiples_of_10", "one_digit", "two_digit", "mixed"] as const;
export const numberSizeOptions = ["small", "big"] as const;
export const placeValueDigitOptions = ["2d", "3d", "4d", "5d"] as const;
export const zeroModeOptions = ["avoid", "allow", "mixed"] as const;

type SelectControl = {
  id: string;
  label: string;
  type: "select";
  options: readonly (string | number)[];
  defaultValue: string | number;
  optionLabels?: Record<string, string>;
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
  category:
    | "Addition & Subtraction"
    | "Multiplication & Division"
    | "Comparison"
    | "Math Properties"
    | "Place Value"
    | "Word Problems";
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

const propertyProblemCount = (): SelectControl => ({
  id: "problemCount",
  label: "Problems",
  type: "select",
  options: [10, 20],
  defaultValue: 10,
});

const sheetCount = (): SelectControl => ({
  id: "sheetCount",
  label: "Sheets",
  type: "select",
  options: sheetCountOptions,
  defaultValue: 1,
});

const propertySheetCount = (): SelectControl => ({
  id: "sheetCount",
  label: "Sheets",
  type: "select",
  options: sheetCountOptions.slice(0, 10),
  defaultValue: 1,
});

const layout = (defaultValue: "horizontal" | "vertical"): SelectControl => ({
  id: "layout",
  label: "Layout",
  type: "select",
  options: layoutOptions,
  defaultValue,
});

const divisionLayout = (): SelectControl => ({
  id: "layout",
  label: "Layout",
  type: "select",
  options: divisionLayoutOptions,
  defaultValue: "equation",
  optionLabels: {
    equation: "Equation",
    long_division: "Long division",
  },
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

const divisionWorksheetControls = (): WorksheetControl[] => [
  problemCount(),
  sheetCount(),
  digits(),
  divisionLayout(),
];

const distributivePropertyControls = (): WorksheetControl[] => [
  propertyProblemCount(),
  propertySheetCount(),
  {
    id: "base",
    label: "Near",
    type: "select",
    options: distributiveBaseOptions,
    defaultValue: "near_100",
    optionLabels: {
      near_10: "10s",
      near_100: "100s",
      mixed: "Mixed",
    },
  },
  {
    id: "direction",
    label: "Direction",
    type: "select",
    options: distributiveDirectionOptions,
    defaultValue: "subtraction",
    optionLabels: {
      subtraction: "Below base",
      addition: "Above base",
      mixed: "Mixed",
    },
  },
  {
    id: "difficulty",
    label: "Factor",
    type: "select",
    options: distributiveDifficultyOptions,
    defaultValue: "multiples_of_10",
    optionLabels: {
      multiples_of_10: "Multiples of 10",
      one_digit: "1 digit",
      two_digit: "2 digit",
      mixed: "Mixed",
    },
  },
  {
    id: "layout",
    label: "Layout",
    type: "select",
    options: ["distributive_property"],
    defaultValue: "distributive_property",
    optionLabels: {
      distributive_property: "Guided steps",
    },
  },
];

const breakingParenthesesControls = (): WorksheetControl[] => [
  {
    id: "problemCount",
    label: "Problems",
    type: "select",
    options: [10, 15, 20],
    defaultValue: 10,
  },
  {
    id: "sheetCount",
    label: "Sheets",
    type: "select",
    options: sheetCountOptions.slice(0, 10),
    defaultValue: 1,
  },
  {
    id: "layout",
    label: "Layout",
    type: "select",
    options: ["breaking_parentheses"],
    defaultValue: "breaking_parentheses",
    optionLabels: {
      breaking_parentheses: "Rewrite lines",
    },
  },
];

const chickenRabbitControls = (): WorksheetControl[] => [
  {
    id: "problemCount",
    label: "Problems",
    type: "select",
    options: [4, 6, 8, 10],
    defaultValue: 6,
  },
  {
    id: "numberSize",
    label: "Number size",
    type: "select",
    options: numberSizeOptions,
    defaultValue: "small",
    optionLabels: {
      small: "Small numbers",
      big: "Big numbers",
    },
  },
  answerKeyControl(),
];

const placeValueControls = (): WorksheetControl[] => [
  {
    id: "problemCount",
    label: "Problems",
    type: "select",
    options: [10, 20],
    defaultValue: 10,
  },
  {
    id: "sheetCount",
    label: "Sheets",
    type: "select",
    options: sheetCountOptions.slice(0, 10),
    defaultValue: 1,
  },
  {
    id: "placeValueDigits",
    label: "Number size",
    type: "select",
    options: placeValueDigitOptions,
    defaultValue: "3d",
    optionLabels: {
      "2d": "2 digits",
      "3d": "3 digits",
      "4d": "4 digits",
      "5d": "5 digits",
    },
  },
  {
    id: "zeroMode",
    label: "Zeros",
    type: "select",
    options: zeroModeOptions,
    defaultValue: "mixed",
    optionLabels: {
      avoid: "Avoid zeros",
      allow: "Allow zeros",
      mixed: "Mixed",
    },
  },
  answerKeyControl(),
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
    controls: divisionWorksheetControls(),
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
  {
    id: "place_value_expanded_form",
    path: "/place_value_expanded_form",
    title: "Expanded Form",
    category: "Place Value",
    examples: ["4,582 = 4,000 + 500 + 80 + 2", "6,040 = 6,000 + 40"],
    controls: placeValueControls(),
  },
  {
    id: "place_value_standard_form",
    path: "/place_value_standard_form",
    title: "Standard Form",
    category: "Place Value",
    examples: ["3,000 + 400 + 20 + 8 = 3,428", "900 + 60 + 5 = 965"],
    controls: placeValueControls(),
  },
  {
    id: "place_value_digit_value",
    path: "/place_value_digit_value",
    title: "Digit Value",
    category: "Place Value",
    examples: ["In 4,582, what is the value of 5?", "In 7,306, what is the value of 3?"],
    controls: placeValueControls(),
  },
  {
    id: "distributive_property_near_numbers",
    path: "/distributive_property_near_numbers",
    title: "Distributive Property",
    category: "Math Properties",
    examples: ["600 x 99", "7 x 101"],
    controls: distributivePropertyControls(),
  },
  {
    id: "breaking_parentheses",
    path: "/breaking_parentheses",
    title: "Breaking Parentheses Practice",
    category: "Math Properties",
    examples: ["21 - (8 + 9)", "39 - (8 - 13)", "(8 + 6) - 5 + 11"],
    controls: breakingParenthesesControls(),
  },
  {
    id: "chicken_rabbit",
    path: "/chicken_rabbit",
    title: "Chicken-Rabbit Word Problems",
    category: "Word Problems",
    examples: [
      "Chickens and rabbits have 26 legs",
      "$5 bills and $2 bills total $41",
      "Spiders and dragonflies have 68 legs",
    ],
    controls: chickenRabbitControls(),
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
