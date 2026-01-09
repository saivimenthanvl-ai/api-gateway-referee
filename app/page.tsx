import Image from "next/image";
import Link from "next/link";

export default function Home() {
  return (
    <main style={{ padding: "2rem", maxWidth: "800px" }}>
      <h1>API Gateway Referee</h1>
      <p>
        A referee-style tool that compares AWS API Gateway options
        and explains trade-offs instead of giving a single answer.
      </p>

      <h3>What this tool does</h3>
      <ul>
        <li>Evaluates REST API, HTTP API, and WebSocket API</li>
        <li>Scores options based on cost, latency, and ops complexity</li>
        <li>Explains <strong>why one option wins</strong> and <strong>what you give up</strong></li>
      </ul>

      <h3>Example referee outcome</h3>
      <p>
        For a <strong>low budget</strong> and <strong>low ops tolerance</strong>,
        the referee typically favors <strong>HTTP API</strong> — but at the cost
        of advanced REST features like usage plans.
      </p>

    <p>
        <Link href="/compare">Run the referee with your own constraints</Link>
      </p>
    </main>
  );
}

