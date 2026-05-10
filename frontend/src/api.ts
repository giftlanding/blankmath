export type GenerateWorksheetRequest = {
  worksheetType: string;
  options: Record<string, string | number | boolean>;
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

  const payload = await response.json() as GenerateWorksheetResponse;

  if (!response.ok) {
    throw new Error(payload.message || payload.error || "Worksheet generation failed.");
  }

  return payload;
}
