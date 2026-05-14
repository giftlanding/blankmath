import react from "@vitejs/plugin-react";
import { defineConfig } from "vitest/config";
import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

const rootLocalEnv = readLocalEnv(resolve(process.cwd(), "../.env.local"));
const lambdaFunctionUrl = process.env.LAMBDA_FUNCTION_URL ?? rootLocalEnv.LAMBDA_FUNCTION_URL;
const internalApiToken = process.env.INTERNAL_API_TOKEN ?? rootLocalEnv.INTERNAL_API_TOKEN;
const enableLocalApiProxy = Boolean(
  lambdaFunctionUrl &&
  internalApiToken &&
  process.env.BLANKMATH_DISABLE_LOCAL_API_PROXY !== "1",
);

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: enableLocalApiProxy
      ? {
          "/api/generate": {
            target: lambdaFunctionUrl,
            changeOrigin: true,
            rewrite: () => "",
            headers: {
              "x-blankmath-internal-token": internalApiToken,
            },
          },
        }
      : undefined,
  },
  test: {
    exclude: ["tests/e2e/**", "node_modules/**", "dist/**"],
  },
});

function readLocalEnv(path: string): Record<string, string> {
  if (!existsSync(path)) {
    return {};
  }

  return Object.fromEntries(
    readFileSync(path, "utf8")
      .split(/\r?\n/)
      .map((line) => line.trim())
      .filter((line) => line && !line.startsWith("#"))
      .map((line) => line.replace(/^export\s+/, ""))
      .map((line) => {
        const separator = line.indexOf("=");
        if (separator === -1) {
          return ["", ""];
        }
        const key = line.slice(0, separator).trim();
        const value = line.slice(separator + 1).trim().replace(/^["']|["']$/g, "");
        return [key, value];
      })
      .filter(([key]) => key),
  );
}
