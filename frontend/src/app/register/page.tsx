"use client";

import { useState } from "react";
import { useAuth } from "@/components/AuthProvider";

export default function RegisterPage() {
  const { register } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await register(email, password, fullName || undefined);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-md rounded border bg-white p-6">
      <h1 className="text-xl font-semibold">Register</h1>
      <p className="mt-1 text-sm text-gray-500">
        Create your account. If you already registered this email, use Login instead.
      </p>
      {error && <div className="mt-3 rounded bg-red-50 p-2 text-sm text-red-700">{error}</div>}
      <form className="mt-4 space-y-3" onSubmit={onSubmit}>
        <label className="block text-sm">
          Full name (optional)
          <input
            className="mt-1 w-full rounded border px-3 py-2"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
          />
        </label>
        <label className="block text-sm">
          Email
          <input
            className="mt-1 w-full rounded border px-3 py-2"
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </label>
        <label className="block text-sm">
          Password
          <input
            className="mt-1 w-full rounded border px-3 py-2"
            type="password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </label>
        <button
          className="w-full rounded bg-blue-600 px-4 py-2 text-white disabled:opacity-60"
          disabled={loading}
        >
          {loading ? "Creating..." : "Register"}
        </button>
      </form>
    </div>
  );
}
