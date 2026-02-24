"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import RequireAuth from "@/components/RequireAuth";
import { apiFetch } from "@/lib/api";
import type { Invoice } from "@/lib/types";

export default function InvoicesPage() {
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    apiFetch("/invoices")
      .then((data) => setInvoices(data))
      .catch((err) => setError(err instanceof Error ? err.message : "Failed"));
  }, []);

  return (
    <RequireAuth>
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-semibold">Invoices</h1>
          <Link href="/invoices/new" className="rounded bg-blue-600 px-4 py-2 text-white">
            New invoice
          </Link>
        </div>
        <p className="text-sm text-gray-600">
          Draft invoices are editable. Finalized invoices are locked and used for tax estimates.
        </p>
        {error && <div className="rounded bg-red-50 p-2 text-sm text-red-700">{error}</div>}
        <div className="rounded border bg-white">
          <div className="grid grid-cols-5 gap-2 border-b px-4 py-2 text-sm font-semibold">
            <div>Number</div>
            <div>Status</div>
            <div>Issue date</div>
            <div>Total</div>
            <div />
          </div>
          {invoices.map((inv) => (
            <div key={inv.id} className="grid grid-cols-5 gap-2 px-4 py-2 text-sm">
              <div>{inv.number}</div>
              <div>{inv.status}</div>
              <div>{inv.issue_date}</div>
              <div>{inv.total?.toFixed(2)} EUR</div>
              <div>
                <Link className="text-blue-600" href={`/invoices/${inv.id}`}>
                  View
                </Link>
              </div>
            </div>
          ))}
          {!invoices.length && (
            <div className="px-4 py-3 text-sm text-gray-500">
              No invoices yet. Create your first draft invoice.
            </div>
          )}
        </div>
      </div>
    </RequireAuth>
  );
}
