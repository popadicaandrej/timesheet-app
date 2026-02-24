-- Migration: Add users table and link timesheets to users
-- Run this after the initial timesheets table exists.

-- 1) Create users table
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  phone_number TEXT
);

-- 2) Insert the 7 users (phone_number NULL)
INSERT INTO users (name, phone_number) VALUES
  ('Lazar Đorđević', NULL),
  ('Danilo Bajić', NULL),
  ('Vuk Stanković', NULL),
  ('Relja Diklić', NULL),
  ('Dušan Stojanović', NULL),
  ('Vuk Knežević', NULL),
  ('Mila Dobrić', NULL);

-- 3) Modify timesheets: add user_id, add FK, remove name
ALTER TABLE timesheets
  ADD COLUMN IF NOT EXISTS user_id INTEGER;

ALTER TABLE timesheets
  ADD CONSTRAINT fk_timesheets_user
  FOREIGN KEY (user_id) REFERENCES users(id);

ALTER TABLE timesheets
  DROP COLUMN IF EXISTS name;
