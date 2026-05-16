export type GenerateWorksheetRequest = {
  worksheetType: string;
  options: Record<string, string | number | boolean>;
  analytics?: {
    gaClientId?: string;
  };
};

export type GenerateWorksheetResponse = {
  url?: string;
  error?: string;
  message?: string;
};

export async function generateWorksheet(request: GenerateWorksheetRequest): Promise<GenerateWorksheetResponse> {
  const response = await fetch("/api/generate", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(request),
  });

  const payload = await parseGenerateResponse(response);

  if (!response.ok) {
    throw new Error(payload.message || payload.error || "Worksheet generation failed.");
  }

  return payload;
}

export function getGoogleAnalyticsClientId(): string | undefined {
  if (typeof document === "undefined") {
    return undefined;
  }

  const cookie = document.cookie
    .split("; ")
    .find((entry) => entry.startsWith("_ga="));
  const value = cookie?.split("=")[1];
  if (!value) {
    return undefined;
  }

  const parts = decodeURIComponent(value).split(".");
  if (parts.length < 4) {
    return undefined;
  }

  return `${parts[parts.length - 2]}.${parts[parts.length - 1]}`;
}

async function parseGenerateResponse(response: Response): Promise<GenerateWorksheetResponse> {
  const text = await response.text();
  if (!text.trim()) {
    return {
      error: "empty_response",
      message: `Worksheet generation failed with an empty response (HTTP ${response.status}).`,
    };
  }

  try {
    return JSON.parse(text) as GenerateWorksheetResponse;
  } catch {
    return {
      error: "invalid_response",
      message: `Worksheet generation returned a non-JSON response (HTTP ${response.status}).`,
    };
  }
}
