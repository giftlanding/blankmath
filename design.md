# Blankmath Rewrite Design Notes

This document captures the current rewrite direction and the reasoning behind the main frontend and backend choices.

## Goals

- Preserve the current Blankmath feature set documented in `features.md`.
- Make new worksheet types cheap to add.
- Avoid one-off layout tuning for every new math format.
- Move math/problem generation toward a single source of truth.
- Keep deployment simple enough for a small static frontend plus serverless backend.

## Backend Direction

### Chosen Approach

Keep PDF generation on the backend, using Python and ReportLab, but rewrite the renderer around structured layout components instead of raw canvas coordinate drawing.

The preferred backend PDF stack is:

- Python
- AWS Lambda
- ReportLab
- ReportLab Platypus where it helps with tables, page flow, and reusable document structure
- Custom ReportLab flowables for math-specific rendering

### Why Not Browser-Based PDF Rendering

HTML/CSS-to-PDF with Playwright or headless Chromium would provide a strong layout engine, but it is likely too heavy for this project’s Lambda deployment model.

Concerns:

- large deployment package or Lambda layer;
- slower cold starts;
- higher memory usage;
- native browser dependency issues;
- more complicated packaging;
- harder local/deployed parity.

For Blankmath, staying with ReportLab is a better fit because the project already uses it and it is much lighter in Lambda.

### Current Backend Problem

The current PDF renderer treats layout as low-level drawing:

- equation strings are manually parsed;
- spaces are inserted into strings to influence layout;
- x/y coordinates are hand-calculated;
- missing-number blanks are drawn manually;
- each new math format risks trial-and-error spacing adjustments.

This does not scale well as worksheet types become more varied.

### Target Backend Architecture

The backend should use a pipeline like:

```text
worksheet request
  -> validated worksheet options
  -> generated structured problems
  -> worksheet document model
  -> reusable PDF layout components
  -> PDF bytes
  -> storage/result URL
```

The frontend should send a worksheet request, not pre-generated equation strings:

```json
{
  "worksheetType": "distributive-property",
  "options": {
    "problemCount": 20,
    "sheetCount": 3,
    "difficulty": "easy",
    "includeAnswerKey": true
  }
}
```

The backend should generate structured problem objects instead of relying on strings like `12+3=x`:

```json
{
  "kind": "equation",
  "terms": [
    { "kind": "number", "value": 3 },
    { "kind": "operator", "value": "*" },
    { "kind": "group", "terms": [
      { "kind": "number", "value": 4 },
      { "kind": "operator", "value": "+" },
      { "kind": "blank" }
    ]},
    { "kind": "equals" },
    { "kind": "number", "value": 21 }
  ]
}
```

The exact schema can evolve, but the important rule is that math structure should be explicit.

### Backend Components

The rewritten backend should have clear ownership boundaries:

- Worksheet registry: maps worksheet type IDs to generators, option schemas, and renderers.
- Option validation: validates request options before generation.
- Problem generators: create structured problem data.
- Answer generation: computes answer keys from structured problems.
- Document model: groups problems into sheets/pages.
- PDF renderer: renders document models to PDF.
- Storage/result service: uploads or returns generated PDFs.

Reusable PDF components should include:

- `WorksheetDocument`
- `WorksheetPage`
- `Header`
- `ProblemGrid`
- `ProblemCell`
- `HorizontalEquation`
- `VerticalEquation`
- `ComparisonProblem`
- `BlankBox`
- `AnswerKeySection`

## Frontend Direction

### Chosen Stack

The recommended frontend stack is:

- React
- TypeScript
- Vite
- TanStack Router
- TanStack Query
- React Hook Form
- Zod
- Tailwind CSS or CSS modules
- Vitest
- Testing Library
- Playwright for frontend browser tests only

### Why This Stack

- React keeps continuity with the current project.
- TypeScript is important because worksheet definitions and option schemas should be type-safe.
- Vite is a simpler modern replacement for Create React App.
- TanStack Router gives type-safe routing and good URL-state handling.
- TanStack Query fits the app’s main async workflow: submit worksheet generation request, handle loading/errors/result.
- React Hook Form handles local form state without needing Redux.
- Zod provides shared validation schemas for worksheet option definitions.
- Vitest and Testing Library cover fast unit/component tests.
- Playwright is useful for end-to-end frontend checks, but should not be part of the PDF-generation path.

### Why Not Redux

The current app uses Redux with separate actions, reducers, selectors, and containers for each worksheet. That creates too much scaffolding as the number of worksheets grows.

The rewritten frontend should not need global state for ordinary worksheet forms. Most state is local form state plus one API mutation. React Hook Form and TanStack Query are a better fit.

### Why Not Next.js Initially

Next.js is not necessary for the current product shape.

Blankmath can remain a static frontend because:

- the app is mostly interactive worksheet configuration;
- PDF generation happens on the backend;
- there is no current need for accounts, dashboards, server-rendered pages, or server-side app logic;
- static hosting keeps deployment simple.

Next.js could be reconsidered later if the project grows into SEO-heavy content, authenticated user features, saved worksheets, subscriptions, or a larger content site.

## Schema-Driven Frontend

The main frontend design choice is to make worksheet pages definition-driven.

Instead of creating a new React page, reducer, selector, and action set for every worksheet, each worksheet should be described by data:

```ts
export const distributivePropertyWorksheet = {
  id: "distributive-property",
  title: "Distributive Property",
  category: "Pre-Algebra",
  examples: ["3(4 + 5) = ?", "6(x + 2) = 42"],
  controls: [
    {
      id: "difficulty",
      type: "select",
      label: "Difficulty",
      options: ["easy", "medium", "hard"],
      defaultValue: "easy"
    },
    {
      id: "problemCount",
      type: "radio",
      label: "Number of Problems",
      options: [10, 20, 30, 50],
      defaultValue: 20
    },
    {
      id: "sheetCount",
      type: "select",
      label: "Number of Sheets",
      options: [1, 2, 3, 4, 5],
      defaultValue: 1
    },
    {
      id: "includeAnswerKey",
      type: "checkbox",
      label: "Include Answer Key",
      defaultValue: false
    }
  ]
} as const;
```

The app should have reusable screens:

- Worksheet catalog page
- Category/filter/search UI
- Worksheet configuration page
- Form renderer for worksheet controls
- Generate button and result handling
- Error/loading states

Adding a worksheet should usually require:

- adding a frontend worksheet definition;
- adding or referencing a backend worksheet type ID;
- adding the backend generator/renderer if it is a new math format;
- adding tests.

It should not require duplicating an entire frontend page stack.

## Frontend/Backend Contract

The frontend should submit worksheet requests:

```json
{
  "worksheetType": "addition",
  "options": {
    "problemCount": 20,
    "sheetCount": 1,
    "layout": "vertical",
    "range": {
      "from": 0,
      "to": 20
    },
    "restrictions": {
      "smallerAddendLessThan10": false
    },
    "includeAnswerKey": false
  }
}
```

The backend should return a result object:

```json
{
  "url": "https://r.blankmath.com/example.pdf"
}
```

The exact API shape can be refined, but the frontend should avoid sending finished equation strings as the primary API contract.

## Scaling To More Worksheets

The rewrite should support many worksheet categories, such as:

- addition and subtraction;
- multiplication and division;
- mixed review;
- comparisons;
- missing-number problems;
- fractions;
- decimals;
- place value;
- pre-algebra;
- distributive property;
- equations and inequalities;
- geometry;
- word problems.

The home page should evolve from a flat card grid into a worksheet catalog with:

- categories;
- search;
- filters by topic or grade/level;
- examples;
- recently used or popular worksheets if needed later.

## Testing Strategy

Frontend tests should cover:

- worksheet definition validation;
- form rendering from definitions;
- request payload creation;
- route behavior;
- API loading/error/success states.

Backend tests should cover:

- option validation;
- problem generation;
- answer generation;
- page splitting;
- renderer smoke tests;
- visual or structural regression checks for representative PDFs.

PDF layout should have regression coverage. At minimum, generate representative sample PDFs and verify page counts and successful rendering. Ideally, render PDFs to images and compare key visual snapshots or measured bounding boxes.

## Design Principles

- New worksheet types should be added through registries and definitions, not copied page stacks.
- Problem data should be structured before it becomes visual layout.
- Layout components should own spacing decisions.
- The frontend should configure worksheets; the backend should generate and render them.
- Keep infrastructure simple until the product requires more.
