export type User = {
  id: string;
  email: string;
  full_name?: string | null;
};

export type Client = {
  id: string;
  name: string;
  country_code: string;
  vat_id?: string | null;
  email?: string | null;
  address?: string | null;
};

export type Invoice = {
  id: string;
  client_id: string;
  number: string;
  issue_date: string;
  due_date?: string | null;
  status: "draft" | "finalized";
  subtotal: number;
  vat_total: number;
  total: number;
};

export type InvoiceLine = {
  id: string;
  invoice_id: string;
  description: string;
  quantity: number;
  unit_price: number;
  vat_rate: number;
  line_subtotal: number;
  vat_amount: number;
  line_total: number;
};

export type DashboardSummary = {
  total_income: number;
  total_expenses: number;
  profit: number;
  estimated_taxes: number;
};
