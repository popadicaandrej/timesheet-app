-- Migration: UNIQUE on users.phone_number + migrate timesheets.name -> users (for old environments)
-- Safe to run: no duplicate users, JOIN-based update, NULL-safe. Idempotent where possible.

-- 1) Add UNIQUE constraint on users.phone_number (multiple NULLs allowed in PostgreSQL)
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint
    WHERE conname = 'uq_users_phone_number' AND conrelid = 'public.users'::regclass
  ) THEN
    ALTER TABLE users ADD CONSTRAINT uq_users_phone_number UNIQUE (phone_number);
  END IF;
END $$;

-- 2) Migrate existing timesheets.name into users (only if column still exists in old environments)
DO $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_schema = 'public' AND table_name = 'timesheets' AND column_name = 'name'
  ) THEN
    -- Insert missing users from distinct timesheets.name (no duplicates)
    INSERT INTO users (name, phone_number)
    SELECT DISTINCT t.name, NULL
    FROM timesheets t
    WHERE t.name IS NOT NULL
      AND NOT EXISTS (SELECT 1 FROM users u WHERE u.name = t.name);

    -- Update timesheets.user_id by matching users.name (JOIN, NULL-safe)
    UPDATE timesheets t
    SET user_id = u.id
    FROM users u
    WHERE u.name = t.name
      AND t.name IS NOT NULL;
  END IF;
END $$;
