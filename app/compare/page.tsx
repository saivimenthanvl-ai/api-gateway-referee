"use client";

import { useState } from "react";

export default function ComparePage() {
  const [result, setResult] = useState<any>(null);

  async function compare() {
  console.log("COMPARE CLICKED - BEFORE FETCH");

  const res = await fetch("/api/compare", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      budget: "low",
      latency: "medium",
      opsTolerance: "low",
    }),
  });

  console.log("FETCH DONE", res.status);

  const data = await res.json();
  console.log("DATA", data);

  setResult(data);
}
  return (
    <main style={{ padding: "2rem", maxWidth: "800px" }}>
      <h1>Referee: API Gateway Options</h1>

      <p>
        Click compare to evaluate AWS API Gateway options using
        predefined constraints:
      </p>

      <ul>
        <li>Budget: Low</li>
        <li>Latency: Medium</li>
        <li>Ops tolerance: Low</li>
      </ul>

      <button type="button" onClick={compare}>
        Compare
      </button>

      {result && (
        <>
          <h3>Referee Decision</h3>

          <p>
            <strong>Winner:</strong> {result.explanation?.winner}
          </p>

          <p>
            <strong>Why:</strong> {result.explanation?.why}
          </p>

          <p>
            <strong>What you give up:</strong>
          </p>

          <ul>
            {result.explanation?.whatYouGiveUp?.map(
              (item: string, i: number) => (
                <li key={i}>{item}</li>
              )
            )}
          </ul>

          <p>
            <em>{result.explanation?.refereeNote}</em>
          </p>

          <details>
            <summary>View full scoring data (JSON)</summary>
            <pre>{JSON.stringify(result, null, 2)}</pre>
          </details>
        </>
      )}
    </main>
  );
}
