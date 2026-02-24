Freelancer Accounting SaaS (Lithuania)

A full-stack MVP built to model income, expenses, and tax estimation logic for Lithuanian freelancers.

The primary focus of this project was data integrity and state-driven financial correctness, not UI polish.

Purpose

This project explores how financial systems can enforce:

Immutable finalized records

Controlled state transitions

Server-side authoritative calculations

Database-level constraint enforcement

The goal was to ensure that financial totals cannot be manipulated through client behavior.

Technology Stack

Backend

FastAPI

PostgreSQL

SQLAlchemy

Pydantic

JWT Authentication

Frontend

Next.js

TypeScript

Tailwind CSS

Core Design Principles
1. Financial State Integrity

Invoices have two states:

draft

finalized

Rules enforced:

Draft invoices are editable

Finalized invoices are immutable

Only finalized invoices affect revenue

Payments can only attach to finalized invoices

These rules are enforced:

In the service layer

With database constraints

2. Server-Side Financial Calculations

Revenue is calculated from finalized invoices only

Draft invoices are excluded

Totals are derived during draft stage

Totals are persisted and locked at finalization

All aggregation happens in backend services

No financial calculations are performed in the frontend.

3. Constraint Enforcement

Examples:

Quantity > 0

Expense amount > 0

VAT rate ≥ 0

No orphan invoice lines

One active tax profile per year

Critical invariants are validated both:

In application logic

At database level

Tax Estimation (MVP Scope)

The project includes tax estimation endpoints:

/tax/summary

/tax/summary/explain

The explain endpoint provides:

Revenue breakdown

Expense breakdown

Applied formulas

Explicit assumptions

This was implemented to make financial logic transparent and auditable.

What This Project Demonstrates

State-based business rule enforcement

Backend-first validation strategy

Data integrity modeling

Immutability patterns

Clear separation between persistence, services, and API

REST API design

Full-stack integration

Why This Matters

The project was intentionally built so that:

Financial correctness does not depend on frontend behavior.

This reflects real-world constraints where data integrity must be enforced at system level.

Trust-oriented backend design

Full-stack integration

Real-world constraints for regulated domains

