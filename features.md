# Blankmath Feature Inventory

This file captures the current feature set to preserve during a full rewrite.

## Product

- Blankmath is a free, open-source math worksheet generator.
- The app generates printable worksheets in PDF format.
- The home page presents worksheet-type cards with operation icons, example problems, and a `Generate` action.
- The header shows the `Blankmath` brand and the subtitle `Unlimited FREE math worksheets`.
- Clicking the brand returns to the home page.
- The public frontend is configured for static hosting from `docs/` / GitHub Pages, with `blankmath.com` configured by `CNAME`.

## Worksheet Types

The app currently exposes these worksheet routes:

- `/addition`: addition problems, for example `12 + 9 = ?`.
- `/minus`: subtraction problems, labeled `Minus`, for example `12 - 9 = ?`.
- `/mixed_add_minus`: mixed addition and subtraction problems.
- `/additionmn`: addition missing-number problems, for example `7 + ? = 15` and `? + 3 = 12`.
- `/minusmn`: subtraction missing-number problems, for example `7 - ? = 5` and `? - 3 = 12`.
- `/mixed_add_minus_mn`: mixed addition/subtraction missing-number problems.
- `/add_three_numbers`: three-number addition problems, for example `7 + 8 + 12 = ?`.
- `/add_minus_three_numbers`: three-number mixed addition/subtraction problems, for example `17 - 8 + 7 = ?`.
- `/add_three_numbers_mn`: three-number addition missing-number problems, for example `7 + ? + 8 = 20`.
- `/multiplication`: multiplication problems, for example `8 * 9 = ?`.
- `/division`: division problems, for example `8 / 2 = ?`.
- `/mixed_times_divide`: mixed multiplication and division problems.
- `/multiplicationmn`: multiplication missing-number problems, for example `8 * ? = 72`.
- `/division_mn`: division missing-number problems, for example `8 / ? = 2` and `? / 4 = 3`.
- `/mixed_times_divide_mn`: mixed multiplication/division missing-number problems.
- `/greater_than_less_than`: comparison problems, labeled `Comparision`, for choosing greater-than or less-than.
- `/distributive_property_near_numbers`: distributive property practice for near-number multiplication, for example `600 x 99 = 600 x (100 - 1)`.

## Shared Worksheet Controls

- Problem count options are `10`, `20`, `30`, and `50` problems per sheet.
- Sheet count can be selected from `1` through `50`.
- Most worksheet pages generate one batch per selected sheet and send all generated problems to the PDF service.
- Range-based worksheets expose `From` and `To` numeric inputs.
- Range validation requires:
  - values to be present;
  - `0 <= value <= 10000`;
  - `from < to`.
- Invalid range values show `invalid entry` helper text and disable the `Create` button on pages using range selectors.
- Digit-based worksheets expose these number-size options:
  - `1d`: 1 digit;
  - `2d`: 2 digit;
  - `3d`: 3 digit;
  - `l12`: number less than 12;
  - `l20`: number less than 20.
- Layout options, where exposed, are `horizontal` and `vertical`.
- Standard division exposes division-specific layout labels:
  - `equation`: inline division facts, for example `12 ÷ 2 = ____`;
  - `long_division`: long-division panels with a quotient line and work rows.
- Distributive property near-number worksheets expose:
  - `base`: `near_10`, `near_100`, or `mixed`;
  - `direction`: `addition`, `subtraction`, or `mixed`;
  - `difficulty`: `one_digit`, `two_digit`, `multiples_of_10`, or `mixed`;
  - `layout`: fixed to `distributive_property`.
  - sheet count is limited to `1` through `10`.
- Clicking `Create` posts generated equations to the configured PDF generator endpoint and opens the returned PDF URL in a new window.

## Default Settings

- Addition, subtraction, mixed addition/subtraction, and multiplication default to:
  - `20` problems;
  - `vertical` layout;
  - `1` sheet.
- Range-based addition/subtraction worksheets default to range `0` through `20`.
- Missing-number addition/subtraction and mixed missing-number addition/subtraction default to:
  - `20` problems;
  - `horizontal` layout;
  - range `0` through `20`;
  - `1` sheet.
- Multiplication, division, mixed multiplication/division, and their missing-number versions default to:
  - `20` problems;
  - `1d`;
  - `equation` layout for standard division;
  - `horizontal` layout for mixed multiplication/division and missing-number division;
  - `vertical` layout for standard multiplication;
  - `1` sheet.
- Three-number worksheets default to:
  - `20` problems;
  - `1d`;
  - `1` sheet.
- Greater-than/less-than defaults to:
  - `10` problems;
  - `l20`;
  - `1` sheet.
- Distributive property near-number worksheets default to:
  - `10` problems;
  - `near_100`;
  - subtraction direction;
  - multiples-of-10 factors;
  - guided-step layout;
  - `1` sheet.

## Problem Generation Rules

- Generated problems are randomized.
- Generators avoid duplicate problem strings within a generated batch.
- Missing values are represented internally as `x`.
- Addition:
  - Generates `a+b=x`.
  - The sum must be within the selected range.
  - Optional restriction: smaller addend less than 10.
- Subtraction:
  - Generates `a-b=x`.
  - The result must be greater than or equal to the selected `From` value.
  - Optional restriction: subtrahend less than 10.
- Mixed addition/subtraction:
  - Generates addition and subtraction pools, then randomly selects from both.
  - Supports the same range and restriction controls as addition/subtraction.
- Addition missing number:
  - Randomly hides the first addend, second addend, or result.
  - Supports range and restriction controls.
- Subtraction missing number:
  - Randomly hides the minuend, subtrahend, or result.
  - Supports range and restriction controls.
- Mixed addition/subtraction missing number:
  - Generates addition-missing-number and subtraction-missing-number pools, then randomly selects from both.
  - Supports range and restriction controls.
  - Has an `Include Answer Key` checkbox.
- Multiplication:
  - Generates `a*b=x`.
  - Factors are positive integers in the selected digit/range mode.
- Multiplication missing number:
  - Randomly hides the first factor, second factor, or product.
- Division:
  - Generates exact integer division problems as `dividend/divisor=x`.
  - The dividend is generated from two factors, so the quotient is an integer.
- Division missing number:
  - Randomly hides the dividend, divisor, or quotient.
- Mixed multiplication/division:
  - Generates multiplication and division pools, then randomly selects from both.
- Mixed multiplication/division missing number:
  - Generates multiplication-missing-number and division-missing-number pools, then randomly selects from both.
- Three-number addition:
  - Generates `a+b+c=x`.
  - In `l20` mode, the total must be at most 20.
- Three-number mixed addition/subtraction:
  - Generates either `a+b-c=x` or `a-b+c=x`.
  - Intermediate and final results are constrained to avoid negative results.
  - In `l20` mode, the final result must be at most 20.
- Three-number addition missing number:
  - Generates `a+b+c=result` and randomly hides one of the three addends or the result.
  - In `l20` mode, addends are single-digit and the total must be at most 20.
- Greater-than/less-than:
  - Generates pairs as `aob`, where `o` marks the blank comparison operator.
  - Numbers are generated in the selected digit/range mode.
- Distributive property near numbers:
  - Generates near-base multiplication problems, such as `600 x 99 = 600 x (100 - 1)`.
  - The near number is generated as a base plus or minus a small offset.
  - The answer is the final product after applying the distributive property.

## PDF Generation

- The frontend sends a JSON payload to `https://api.blankmath.com/`.
- Payload fields include:
  - `equations`: generated equation strings;
  - `template`: usually `horizontal` or `vertical`;
  - `countPerPage`: selected problem count;
  - `includeAnswerKey`: currently sent only by mixed addition/subtraction missing-number worksheets.
- The backend returns a plain-text PDF URL.
- The backend renders PDFs with ReportLab on US letter pages.
- The PDF title is `BlankMath.com`.
- Each page includes the logo/header image from `backend/template/logo.jpg`.
- Horizontal PDFs:
  - insert spacing around operators and equals signs;
  - render `*` as `×` and `/` as `÷`;
  - render missing numbers as rounded rectangles;
  - render comparison blanks as smaller rounded rectangles.
- Vertical PDFs:
  - stack equation tokens vertically;
  - render `*` as `×` and `/` as `÷`;
  - use an underline/blank for the answer position.
- Distributive property PDFs:
  - use a dedicated guided-step panel;
  - show the original multiplication and rewritten distributive expression;
  - provide blanks for each partial product and final combination.
- The backend selects a layout based on template and problem count:
  - horizontal layouts for approximately 30 or 52 problems;
  - vertical layouts for approximately 30, 49, or 56 problems;
  - three-number layouts for 20, 30, or 50 problems.
- If `includeAnswerKey` is true, the backend solves equations containing `x` with SymPy and appends solved versions after the original problems.
- Generated PDFs are uploaded to S3 bucket `r.blankmath.com` under a SHA-1 hash filename.
- The public PDF URL is `https://r.blankmath.com/{hash}.pdf`.

## Backend API

- The deployed backend is an AWS Lambda function named `blankmath`.
- The Lambda handler accepts an API Gateway-style event with a JSON string in `event.body`.
- A successful response has:
  - status code `201`;
  - `Content-Type: text/plain`;
  - `Access-Control-Allow-Origin: *`;
  - body containing the generated PDF URL.
- Backend dependencies are `reportlab` and `sympy`; Lambda deployment also relies on `boto3` from the runtime or package.
- Backend packaging is performed with a Docker packager that builds `backend/deploy.zip`.

## Build, Test, and Deploy

- Frontend stack:
  - React 17;
  - TypeScript;
  - Redux and React Redux;
  - React Router;
  - Material UI;
  - Reactstrap / Bootstrap;
  - Font Awesome icons;
  - Axios.
- Frontend commands:
  - `npm start`;
  - `npm run build`;
  - `npm test -- --passWithNoTests`;
  - `npm run deploy`.
- Frontend CI runs on pushes and pull requests touching `math_ui/**`.
- Frontend CI uses Node 16, runs `npm ci`, builds, tests, and deploys with `gh-pages -d build`.
- Backend CI runs on pushes and pull requests touching `backend/**`.
- Backend CI builds the packager Docker image, produces `deploy.zip`, and deploys it to AWS Lambda.

## Existing Quirks To Preserve Or Revisit

- Several labels and names are misspelled in the current UI/code, including `Minus`, `Comparision`, and `Substraction`.
- The home-page link for `/add_three_numbers` and `/add_three_numbers_mn` lacks a leading slash in card data, but routing still works from the home page.
- Some digit options are shown by the shared `NumberOfDigits` component even when a generator does not explicitly handle every option.
- Some page components carry `problemDirection` state but do not expose a layout control.
- Greater-than/less-than maps `sheetNumber` from `addThreeNumbersData` instead of its own reducer state.
- Backend support for `vertical_div` is stubbed and not exposed by the current frontend.
- The PDF backend has an API documentation link in `backend/README.md` pointing to SwaggerHub.

## Planned Features

### Additional Math Properties

Math-property worksheets should teach arithmetic strategies, not only ask
students to compute an isolated expression. The first implemented worksheet is
distributive property near-number multiplication. Future math-property
worksheets could include:

- distributive property by splitting one factor, such as `7 x 23 = 7 x (20 + 3)`;
- factoring out a common factor, such as `6 x 8 + 6 x 2 = 6 x (8 + 2)`;
- commutative and associative property practice, if they can be made useful
  rather than purely definitional.
