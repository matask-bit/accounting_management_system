"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import RequireAuth from "@/components/RequireAuth";
import { apiFetch } from "@/lib/api";
import type { Invoice, InvoiceLine } from "@/lib/types";

type LineForm = {
  description: string;
  quantity: number;
  unit_price: number;
  vat_rate: number;
};

const emptyLine: LineForm = {
  description: "",
  quantity: 1,
  unit_price: 0,
  vat_rate: 0,
};

export default function InvoiceDetailPage() {
  const params = useParams();
  const id = params.id as string;
  const [invoice, setInvoice] = useState<Invoice | null>(null);
  const [lines, setLines] = useState<InvoiceLine[]>([]);
  const [lineForm, setLineForm] = useState<LineForm>(emptyLine);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  const load = () => {
    apiFetch(`/invoices/${id}`)
      .then((data) => setInvoice(data))
      .catch((err) => setError(err instanceof Error ? err.message : "Failed"));
    apiFetch(`/invoices/${id}/lines`)
      .then((data) => setLines(data))
      .catch((err) => setError(err instanceof Error ? err.message : "Failed"));
  };

  useEffect(() => {
    load();
  }, [id]);

  const updateInvoice = async (changes: Partial<Invoice>) => {
    setSaving(true);
    setError(null);
    try {
      await apiFetch(`/invoices/${id}`, {
        method: "PUT",
        body: JSON.stringify({
          number: changes.number,
          issue_date: changes.issue_date,
          due_date: changes.due_date || null,
          client_id: changes.client_id,
        }),
      });
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    } finally {
      setSaving(false);
    }
  };

  const addLine = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      await apiFetch(`/invoices/${id}/lines`, {
        method: "POST",
        body: JSON.stringify(lineForm),
      });
      setLineForm(emptyLine);
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  const removeLine = async (lineId: string) => {
    setError(null);
    try {
      const ok = window.confirm("Delete this line? This cannot be undone.");
      if (!ok) return;
      await apiFetch(`/invoices/${id}/lines/${lineId}`, { method: "DELETE" });
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  const finalize = async () => {
    setSaving(true);
    setError(null);
    try {
      await apiFetch(`/invoices/${id}/finalize`, { method: "POST" });
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    } finally {
      setSaving(false);
    }
  };

  if (!invoice) {
    return (
      <RequireAuth>
        <div className="text-sm text-gray-500">Loading...</div>
      </RequireAuth>
    );
  }

  const isDraft = invoice.status === "draft";

  return (
    <RequireAuth>
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-semibold">Invoice {invoice.number}</h1>
          <span className="text-sm text-gray-500">Status: {invoice.status}</span>
        </div>
        <p className="text-sm text-gray-600">
          Draft invoices can be edited. Finalized invoices are read-only and used for tax estimates.
        </p>
        {!isDraft && (
          <div className="rounded border bg-gray-50 p-3 text-sm text-gray-700">
            This invoice is finalized and cannot be edited.
          </div>
        )}
        {error && <div className="rounded bg-red-50 p-2 text-sm text-red-700">{error}</div>}

        <div className="rounded border bg-white p-4 space-y-3">
          <div className="grid gap-3 sm:grid-cols-2">
            <label className="text-sm">
              Invoice number
              <input
                className="mt-1 w-full rounded border px-3 py-2"
                value={invoice.number}
                disabled={!isDraft}
                onChange={(e) =>
                  setInvoice({ ...invoice, number: e.target.value })
                }
                onBlur={() => updateInvoice(invoice)}
              />
            </label>
            <label className="text-sm">
              Issue date
              <input
                className="mt-1 w-full rounded border px-3 py-2"
                type="date"
                value={invoice.issue_date}
                disabled={!isDraft}
                onChange={(e) =>
                  setInvoice({ ...invoice, issue_date: e.target.value })
                }
                onBlur={() => updateInvoice(invoice)}
              />
            </label>
            <label className="text-sm">
              Due date
              <input
                className="mt-1 w-full rounded border px-3 py-2"
                type="date"
                value={invoice.due_date || ""}
                disabled={!isDraft}
                onChange={(e) =>
                  setInvoice({ ...invoice, due_date: e.target.value })
                }
                onBlur={() => updateInvoice(invoice)}
              />
            </label>
          </div>
        </div>

        <div className="rounded border bg-white">
          <div className="grid grid-cols-6 gap-2 border-b px-4 py-2 text-sm font-semibold">
            <div>Description</div>
            <div>Qty</div>
            <div>Unit</div>
            <div>VAT %</div>
            <div>Total</div>
            <div />
          </div>
          {lines.map((line) => (
            <div key={line.id} className="grid grid-cols-6 gap-2 px-4 py-2 text-sm">
              <div>{line.description}</div>
              <div>{line.quantity}</div>
              <div>{line.unit_price.toFixed(2)}</div>
              <div>{line.vat_rate.toFixed(2)}</div>
              <div>{line.line_total.toFixed(2)}</div>
              <div>
                {isDraft && (
                  <button className="text-red-600" onClick={() => removeLine(line.id)}>
                    Delete
                  </button>
                )}
              </div>
            </div>
          ))}
          {!lines.length && (
            <div className="px-4 py-3 text-sm text-gray-500">No lines yet.</div>
          )}
        </div>

        {isDraft && (
          <form className="rounded border bg-white p-4 space-y-3" onSubmit={addLine}>
            <h2 className="text-lg font-semibold">Add line</h2>
            <div className="grid gap-3 sm:grid-cols-4">
              <label className="text-sm sm:col-span-2">
                Description
                <input
                  className="mt-1 w-full rounded border px-3 py-2"
                  required
                  value={lineForm.description}
                  onChange={(e) => setLineForm({ ...lineForm, description: e.target.value })}
                />
              </label>
              <label className="text-sm">
                Quantity
                <input
                  className="mt-1 w-full rounded border px-3 py-2"
                  type="number"
                  min={1}
                  step={1}
                  required
                  value={lineForm.quantity}
                  onChange={(e) => setLineForm({ ...lineForm, quantity: Number(e.target.value) })}
                />
              </label>
              <label className="text-sm">
                Unit price
                <input
                  className="mt-1 w-full rounded border px-3 py-2"
                  type="number"
                  min={0}
                  step="0.01"
                  required
                  value={lineForm.unit_price}
                  onChange={(e) => setLineForm({ ...lineForm, unit_price: Number(e.target.value) })}
                />
              </label>
              <label className="text-sm">
                VAT rate %
                <input
                  className="mt-1 w-full rounded border px-3 py-2"
                  type="number"
                  min={0}
                  step="0.01"
                  value={lineForm.vat_rate}
                  onChange={(e) => setLineForm({ ...lineForm, vat_rate: Number(e.target.value) })}
                />
              </label>
            </div>
            <button className="rounded bg-blue-600 px-4 py-2 text-white">Add line</button>
          </form>
        )}

        <div className="rounded border bg-white p-4">
          <div className="flex justify-between text-sm">
            <span>Subtotal</span>
            <span>{invoice.subtotal.toFixed(2)} EUR</span>
          </div>
          <div className="flex justify-between text-sm">
            <span>VAT total</span>
            <span>{invoice.vat_total.toFixed(2)} EUR</span>
          </div>
          <div className="flex justify-between text-lg font-semibold">
            <span>Total</span>
            <span>{invoice.total.toFixed(2)} EUR</span>
          </div>
        </div>

        {isDraft && (
          <div className="space-y-2">
            <button
              className="rounded bg-green-600 px-4 py-2 text-white disabled:opacity-60"
              onClick={() => {
                if (!lines.length) {
                  setError("Add at least one line before finalizing.");
                  return;
                }
                finalize();
              }}
              disabled={saving}
            >
              {saving ? "Finalizing..." : "Finalize invoice"}
            </button>
            {!lines.length && (
              <div className="text-xs text-gray-500">
                Finalize is disabled until the invoice has at least one line.
              </div>
            )}
          </div>
        )}
      </div>
    </RequireAuth>
  );
}
