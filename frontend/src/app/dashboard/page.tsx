"use client";

import { useEffect, useState } from "react";
import RequireAuth from "@/components/RequireAuth";
import { apiFetch } from "@/lib/api";
import type { DashboardSummary } from "@/lib/types";

export default function DashboardPage() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [creatingDemo, setCreatingDemo] = useState(false);

  useEffect(() => {
    apiFetch("/dashboard/summary")
      .then((data) => setSummary(data))
      .catch((err) => setError(err instanceof Error ? err.message : "Failed"));
  }, []);

  const createDemoData = async () => {
    const ok = window.confirm(
      "Create demo data? This will add a client, a draft invoice, and one invoice line."
    );
    if (!ok) return;
    setCreatingDemo(true);
    setError(null);
    try {
      const client = await apiFetch("/clients", {
        method: "POST",
        body: JSON.stringify({
          name: "Demo Client",
          country_code: "LT",
          email: "demo@example.com",
          vat_id: "",
          address: "Vilnius",
        }),
      });
      const today = new Date().toISOString().slice(0, 10);
      const invoice = await apiFetch("/invoices", {
        method: "POST",
        body: JSON.stringify({
          client_id: client.id,
          number: `DEMO-${Math.floor(Math.random() * 900 + 100)}`,
          issue_date: today,
          due_date: null,
        }),
      });
      await apiFetch(`/invoices/${invoice.id}/lines`, {
        method: "POST",
        body: JSON.stringify({
          description: "Demo service",
          quantity: 1,
          unit_price: 100,
          vat_rate: 21,
        }),
      });
      const refreshed = await apiFetch("/dashboard/summary");
      setSummary(refreshed);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    } finally {
      setCreatingDemo(false);
    }
  };

  return (
    <RequireAuth>
      <div className="space-y-4">
        <h1 className="text-2xl font-semibold">Dashboard</h1>
        <p className="text-sm text-gray-600">
          Tax amounts are estimates based on finalized invoices and recorded expenses.
        </p>
        {error && <div className="rounded bg-red-50 p-2 text-sm text-red-700">{error}</div>}
        {!summary && !error && <div className="text-sm text-gray-500">Loading...</div>}
        {!summary && error?.toLowerCase().includes("tax profile") && (
          <div className="rounded border bg-white p-4 text-sm text-gray-700">
            No tax profile found. Create one in the backend to see tax estimates.
          </div>
        )}
        {summary && (
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="rounded border bg-white p-4">
              <div className="text-sm text-gray-500">Total income</div>
              <div className="text-xl font-semibold">{summary.total_income.toFixed(2)} EUR</div>
            </div>
            <div className="rounded border bg-white p-4">
              <div className="text-sm text-gray-500">Total expenses</div>
              <div className="text-xl font-semibold">{summary.total_expenses.toFixed(2)} EUR</div>
            </div>
            <div className="rounded border bg-white p-4">
              <div className="text-sm text-gray-500">Profit</div>
              <div className="text-xl font-semibold">{summary.profit.toFixed(2)} EUR</div>
            </div>
            <div className="rounded border bg-white p-4">
              <div className="text-sm text-gray-500">Estimated taxes</div>
              <div className="text-xl font-semibold">{summary.estimated_taxes.toFixed(2)} EUR</div>
              <div className="mt-1 text-xs text-gray-500">Estimates only, not filing-ready.</div>
            </div>
          </div>
        )}
        <div className="rounded border bg-white p-4 text-sm text-gray-600">
          <div className="flex items-center justify-between gap-4">
            <div>
              Want to try the app quickly? Create demo data and explore invoices.
            </div>
            <button
              className="rounded border px-3 py-1 text-sm disabled:opacity-60"
              onClick={createDemoData}
              disabled={creatingDemo}
            >
              {creatingDemo ? "Creating..." : "Try with demo data"}
            </button>
          </div>
        </div>
      </div>
    </RequireAuth>
  );
}
