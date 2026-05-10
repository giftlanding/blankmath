# Blankmath Frontend

This is the React/Vite frontend for the Blankmath rewrite.

## Commands

```sh
npm install
npm run dev
npm run build
npm test
```

## Cloudflare Pages

The production Pages project should build with:

- root directory: `frontend`
- build command: `npm run build`
- output directory: `dist`

The browser calls `/api/generate`. Cloudflare Pages Functions proxy that request
to the Lambda Function URL with the internal token that Terraform stores as
Pages environment variables.
