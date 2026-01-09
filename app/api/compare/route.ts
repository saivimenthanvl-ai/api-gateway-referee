import { NextResponse } from "next/server";

export async function POST(req: Request) {
  return NextResponse.json({
    explanation: {
      winner: "API Gateway HTTP API",
      why:
        "HTTP API offers lower cost and simpler operations under low-budget and low-ops constraints.",
      whatYouGiveUp: [
        "Limited features compared to REST API",
        "No native API keys or usage plans",
      ],
      refereeNote:
        "If you need advanced features like usage plans or API keys, REST API may be the better choice.",
    },
  });
}
