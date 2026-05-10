interface Env {
  LAMBDA_FUNCTION_URL: string;
  INTERNAL_API_TOKEN: string;
}

export const onRequestPost: PagesFunction<Env> = async ({ request, env }) => {
  if (!env.LAMBDA_FUNCTION_URL || !env.INTERNAL_API_TOKEN) {
    return jsonResponse(500, { error: "missing_backend_config" });
  }

  const body = await request.text();
  const upstream = await fetch(env.LAMBDA_FUNCTION_URL, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "x-blankmath-internal-token": env.INTERNAL_API_TOKEN,
    },
    body,
  });

  return new Response(upstream.body, {
    status: upstream.status,
    headers: {
      "content-type": upstream.headers.get("content-type") ?? "application/json",
    },
  });
};

export const onRequest: PagesFunction<Env> = async () => {
  return jsonResponse(405, { error: "method_not_allowed" });
};

function jsonResponse(status: number, body: unknown): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json" },
  });
}
