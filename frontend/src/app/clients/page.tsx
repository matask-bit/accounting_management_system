"use client";

import { useEffect, useState } from "react";
import RequireAuth from "@/components/RequireAuth";
import { apiFetch } from "@/lib/api";
import type { Client } from "@/lib/types";

const emptyClient: Omit<Client, "id"> = {
  name: "",
  country_code: "LT",
  vat_id: "",
  email: "",
  address: "",
};

export default function ClientsPage() {
  const [clients, setClients] = useState<Client[]>([]);
  const [form, setForm] = useState<Omit<Client, "id">>(emptyClient);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const load = () =>
    apiFetch("/clients")
      .then((data) => setClients(data))
      .catch((err) => setError(err instanceof Error ? err.message : "Failed"));

  useEffect(() => {
    load();
  }, []);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      if (editingId) {
        await apiFetch(`/clients/${editingId}`, {
          method: "PUT",
          body: JSON.stringify(form),
        });
      } else {
        await apiFetch("/clients", {
          method: "POST",
          body: JSON.stringify(form),
        });
      }
      setForm(emptyClient);
      setEditingId(null);
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  const startEdit = (client: Client) => {
    setEditingId(client.id);
    setForm({
      name: client.name,
      country_code: client.country_code,
      vat_id: client.vat_id || "",
      email: client.email || "",
      address: client.address || "",
    });
  };

  const remove = async (id: string) => {
    setError(null);
    try {
      const ok = window.confirm("Delete this client? This cannot be undone.");
      if (!ok) return;
      await apiFetch(`/clients/${id}`, { method: "DELETE" });
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  return (
    <RequireAuth>
      <div className="space-y-6">
        <h1 className="text-2xl font-semibold">Clients</h1>
        {error && <div className="rounded bg-red-50 p-2 text-sm text-red-700">{error}</div>}

        <form className="rounded border bg-white p-4 space-y-3" onSubmit={submit}>
          <div className="grid gap-3 sm:grid-cols-2">
            <label className="text-sm">
              Name
              <input
                className="mt-1 w-full rounded border px-3 py-2"
                required
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
              />
            </label>
            <label className="text-sm">
              Country code
              <input
                className="mt-1 w-full rounded border px-3 py-2"
                required
                value={form.country_code}
                maxLength={2}
                onChange={(e) => setForm({ ...form, country_code: e.target.value.toUpperCase() })}
              />
            </label>
            <label className="text-sm">
              VAT ID
              <input
                className="mt-1 w-full rounded border px-3 py-2"
                value={form.vat_id || ""}
                onChange={(e) => setForm({ ...form, vat_id: e.target.value })}
              />
            </label>
            <label className="text-sm">
              Email
              <input
                className="mt-1 w-full rounded border px-3 py-2"
                type="email"
                value={form.email || ""}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
              />
            </label>
            <label className="text-sm sm:col-span-2">
              Address
              <input
                className="mt-1 w-full rounded border px-3 py-2"
                value={form.address || ""}
                onChange={(e) => setForm({ ...form, address: e.target.value })}
              />
            </label>
          </div>
          <div className="flex gap-2">
            <button className="rounded bg-blue-600 px-4 py-2 text-white">
              {editingId ? "Update client" : "Add client"}
            </button>
            {editingId && (
              <button
                type="button"
                className="rounded border px-4 py-2"
                onClick={() => {
                  setEditingId(null);
                  setForm(emptyClient);
                }}
              >
                Cancel
              </button>
            )}
          </div>
        </form>

        <div className="rounded border bg-white">
          <div className="grid grid-cols-5 gap-2 border-b px-4 py-2 text-sm font-semibold">
            <div>Name</div>
            <div>Country</div>
            <div>Email</div>
            <div>VAT</div>
            <div />
          </div>
          {clients.map((client) => (
            <div key={client.id} className="grid grid-cols-5 gap-2 px-4 py-2 text-sm">
              <div>{client.name}</div>
              <div>{client.country_code}</div>
              <div>{client.email || "-"}</div>
              <div>{client.vat_id || "-"}</div>
              <div className="flex gap-2">
                <button className="text-blue-600" onClick={() => startEdit(client)}>
                  Edit
                </button>
                <button className="text-red-600" onClick={() => remove(client.id)}>
                  Delete
                </button>
              </div>
            </div>
          ))}
          {!clients.length && (
            <div className="px-4 py-3 text-sm text-gray-500">
              No clients yet. Add your first client above.
            </div>
          )}
        </div>
      </div>
    </RequireAuth>
  );
}
