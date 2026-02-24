-- Manual constraints for integrity (run once)
ALTER TABLE invoices
  ALTER COLUMN status SET NOT NULL;

ALTER TABLE invoice_lines
  ADD CONSTRAINT invoice_lines_quantity_positive CHECK (quantity > 0),
  ADD CONSTRAINT invoice_lines_vat_rate_nonnegative CHECK (vat_rate >= 0);

ALTER TABLE payments
  ALTER COLUMN invoice_id SET NOT NULL,
  ALTER COLUMN amount SET NOT NULL,
  ADD CONSTRAINT payments_amount_positive CHECK (amount > 0);

ALTER TABLE expenses
  ALTER COLUMN amount SET NOT NULL,
  ADD CONSTRAINT expenses_amount_positive CHECK (amount > 0);
