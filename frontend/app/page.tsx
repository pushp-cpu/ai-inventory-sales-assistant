"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";

const quickQuestions = [
  "Which products are low on stock?",
  "What is the total revenue?",
  "Which products are selling the most?",
  "Show me all products and their current stock.",
  "Show me all recorded sales.",
];

export default function Home() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  async function askAI(customQuestion?: string) {
    const currentQuestion = customQuestion ?? question;

    if (!currentQuestion.trim()) {
      return;
    }

    setQuestion(currentQuestion);
    setLoading(true);
    setAnswer("");

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: currentQuestion,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to get response from server.");
      }

      const data = await response.json();

      setAnswer(data.answer);
    } catch (error) {
      console.error(error);
      setAnswer("Unable to connect to the AI server.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-gray-100 px-6 py-12">
      <div className="mx-auto max-w-4xl">

        {/* Header */}
        <div className="mb-8">
          <p className="mb-2 text-sm font-semibold uppercase tracking-wide text-gray-500">
            AI-Powered Business Assistant
          </p>

          <h1 className="text-4xl font-bold text-gray-900">
            Inventory & Sales Assistant
          </h1>

          <p className="mt-3 text-gray-600">
            Ask questions about your products, inventory, sales, revenue,
            and business performance.
          </p>
        </div>

        {/* Quick Questions */}
        <div className="mb-6">
          <p className="mb-3 text-sm font-medium text-gray-700">
            Quick questions
          </p>

          <div className="flex flex-wrap gap-2">
            {quickQuestions.map((item) => (
              <button
                key={item}
                onClick={() => askAI(item)}
                disabled={loading}
                className="rounded-full border border-gray-300 bg-white px-4 py-2 text-sm text-gray-700 transition hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {item}
              </button>
            ))}
          </div>
        </div>

        {/* Question Box */}
        <div className="rounded-xl bg-white p-6 shadow-sm">
          <textarea
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="Ask something like: Which products are low on stock?"
            className="h-32 w-full resize-none rounded-lg border border-gray-300 p-4 text-gray-900 outline-none focus:border-gray-500 focus:ring-1 focus:ring-gray-500"
          />

          <div className="mt-4 flex justify-end">
            <button
              onClick={() => askAI()}
              disabled={loading || !question.trim()}
              className="rounded-lg bg-black px-6 py-3 font-medium text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? "Thinking..." : "Ask AI"}
            </button>
          </div>
        </div>

        {/* AI Response */}
        {answer && (
          <div className="mt-6 rounded-xl bg-white p-6 shadow-sm">
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-xl font-semibold text-gray-900">
                AI Response
              </h2>

              <span className="rounded-full bg-gray-100 px-3 py-1 text-xs font-medium text-gray-600">
                Gemini
              </span>
            </div>

<div className="text-gray-800">
  <ReactMarkdown
    components={{
      p: ({ children }) => (
        <p className="mb-4 leading-7 text-gray-800">
          {children}
        </p>
      ),

      strong: ({ children }) => (
        <strong className="font-semibold text-gray-900">
          {children}
        </strong>
      ),

      ul: ({ children }) => (
        <ul className="mb-4 list-disc space-y-2 pl-6 text-gray-800">
          {children}
        </ul>
      ),

      ol: ({ children }) => (
        <ol className="mb-4 list-decimal space-y-2 pl-6 text-gray-800">
          {children}
        </ol>
      ),

      li: ({ children }) => (
        <li className="text-gray-800">
          {children}
        </li>
      ),
    }}
  >
    {answer}
  </ReactMarkdown>
</div>
          </div>
        )}
      </div>
    </main>
  );
}
