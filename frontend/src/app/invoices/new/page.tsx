"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import RequireAuth from "@/components/RequireAuth";
import { apiFetch } from "@/lib/api";
import type { Client } from "@/lib/types";

export default function NewInvoicePage() {
  const router = useRouter();
  const [clients, setClients] = useState<Client[]>([]);
  const [clientId, setClientId] = useState("");
  const [number, setNumber] = useState("");
  const [issueDate, setIssueDate] = useState("");
  const [dueDate, setDueDate] = useState("");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    apiFetch("/clients")
      .then((data) => setClients(data))
      .catch((err) => setError(err instanceof Error ? err.message : "Failed"));
  }, []);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      const invoice = await apiFetch("/invoices", {
        method: "POST",
        body: JSON.stringify({
          client_id: clientId,
          number,
          issue_date: issueDate,
          due_date: dueDate || null,
        }),
      });
      router.push(`/invoices/${invoice.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  return (
    <RequireAuth>
      <div className="space-y-4">
        <h1 className="text-2xl font-semibold">Create Invoice (Draft)</h1>
        {error && <div className="rounded bg-red-50 p-2 text-sm text-red-700">{error}</div>}
        <form className="rounded border bg-white p-4 space-y-3" onSubmit={submit}>
          <label className="block text-sm">
            Client
            <select
              className="mt-1 w-full rounded border px-3 py-2"
              required
              value={clientId}
              onChange={(e) => setClientId(e.target.value)}
            >
              <option value="">Select client</option>
              {clients.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name}
                </option>
              ))}
            </select>
          </label>
          <label className="block text-sm">
            Invoice number
            <input
              className="mt-1 w-full rounded border px-3 py-2"
              required
              value={number}
              onChange={(e) => setNumber(e.target.value)}
            />
          </label>
          <div className="grid gap-3 sm:grid-cols-2">
            <label className="block text-sm">
              Issue date
              <input
                className="mt-1 w-full rounded border px-3 py-2"
                type="date"
                required
                value={issueDate}
                onChange={(e) => setIssueDate(e.target.value)}
              />
            </label>
            <label className="block text-sm">
              Due date (optional)
              <input
                className="mt-1 w-full rounded border px-3 py-2"
                type="date"
                value={dueDate}
                onChange={(e) => setDueDate(e.target.value)}
              />
            </label>
          </div>
          <button className="rounded bg-blue-600 px-4 py-2 text-white">
            Create draft
          </button>
        </form>
      </div>
    </RequireAuth>
  );
}
