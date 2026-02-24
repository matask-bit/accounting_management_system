from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.database import Base
import app.models  # noqa: F401
from app.routers import auth, users, tax_profiles, clients, invoices, invoice_lines, payments, expenses, tax, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Freelancer Accounting SaaS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tax_profiles.router)
app.include_router(clients.router)
app.include_router(invoices.router)
app.include_router(invoice_lines.router)
app.include_router(payments.router)
app.include_router(expenses.router)
app.include_router(tax.router)
app.include_router(dashboard.router)