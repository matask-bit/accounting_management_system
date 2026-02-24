"use client";

import AuthProvider from "@/components/AuthProvider";
import Nav from "@/components/Nav";

export default function ClientProviders({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <AuthProvider>
      <Nav />
      <main className="mx-auto w-full max-w-5xl px-4 py-6">{children}</main>
    </AuthProvider>
  );
}
