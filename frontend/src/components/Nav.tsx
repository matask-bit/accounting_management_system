"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/components/AuthProvider";

const navItems = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/clients", label: "Clients" },
  { href: "/invoices", label: "Invoices" },
];

export default function Nav() {
  const pathname = usePathname();
  const { token, user, logout } = useAuth();

  return (
    <header className="border-b bg-white">
      <div className="mx-auto flex w-full max-w-5xl items-center justify-between px-4 py-4">
        <Link href="/" className="text-lg font-semibold">
          Freelancer Accounting
        </Link>
        <nav className="flex items-center gap-4 text-sm">
          {token &&
            navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={`${
                  pathname === item.href ? "font-semibold text-blue-600" : "text-gray-700"
                }`}
              >
                {item.label}
              </Link>
            ))}
          {token ? (
            <div className="flex items-center gap-3">
              <span className="text-gray-500">{user?.email}</span>
              <button
                onClick={logout}
                className="rounded border px-3 py-1 text-sm"
              >
                Logout
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-3">
              <Link href="/login" className="text-gray-700">
                Login
              </Link>
              <Link href="/register" className="rounded border px-3 py-1 text-sm">
                Register
              </Link>
            </div>
          )}
        </nav>
      </div>
    </header>
  );
}
