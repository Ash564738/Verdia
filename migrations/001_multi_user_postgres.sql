-- Smart Plant Care AI - PostgreSQL multi-user schema
-- Run automatically with init SQL or before application startup.

CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  name TEXT NOT NULL,
  role TEXT NOT NULL DEFAULT 'USER',
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS plants (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  species TEXT NOT NULL,
  variety TEXT,
  started_at TEXT,
  location TEXT,
  notes TEXT,
  image_path TEXT,
  status TEXT NOT NULL DEFAULT 'active',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS diseases (
  id TEXT PRIMARY KEY,
  code TEXT UNIQUE NOT NULL,
  plant TEXT NOT NULL,
  name TEXT NOT NULL,
  name_vi TEXT NOT NULL,
  pathogen TEXT,
  symptoms TEXT NOT NULL,
  conditions TEXT NOT NULL,
  treatment TEXT NOT NULL,
  prevention TEXT NOT NULL,
  image_url TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS diagnoses (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  plant_id TEXT REFERENCES plants(id) ON DELETE SET NULL,
  filename TEXT,
  image_path TEXT,
  plant TEXT NOT NULL,
  disease_code TEXT NOT NULL,
  status TEXT NOT NULL,
  confidence DOUBLE PRECISION NOT NULL,
  top_predictions TEXT NOT NULL,
  recommendation TEXT NOT NULL,
  model_version TEXT NOT NULL,
  severity TEXT NOT NULL,
  note TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS diagnosis_images (
  id TEXT PRIMARY KEY,
  diagnosis_id TEXT NOT NULL REFERENCES diagnoses(id) ON DELETE CASCADE,
  user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  storage_key TEXT NOT NULL,
  filename TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS scan_predictions (
  id TEXT PRIMARY KEY,
  diagnosis_id TEXT NOT NULL REFERENCES diagnoses(id) ON DELETE CASCADE,
  class_code TEXT NOT NULL,
  class_name TEXT NOT NULL,
  confidence DOUBLE PRECISION NOT NULL,
  rank INTEGER NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS care_logs (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  plant_id TEXT REFERENCES plants(id) ON DELETE SET NULL,
  kind TEXT NOT NULL,
  note TEXT,
  occurred_at TIMESTAMPTZ NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS reminders (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  plant_id TEXT REFERENCES plants(id) ON DELETE SET NULL,
  kind TEXT NOT NULL,
  due_at TIMESTAMPTZ NOT NULL,
  note TEXT,
  completed BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS notifications (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  message TEXT NOT NULL,
  kind TEXT NOT NULL,
  is_read BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS audit_logs (
  id TEXT PRIMARY KEY,
  actor_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  action TEXT NOT NULL,
  target_type TEXT NOT NULL,
  target_id TEXT,
  details TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS feedback (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  diagnosis_id TEXT NOT NULL REFERENCES diagnoses(id) ON DELETE CASCADE,
  rating INTEGER,
  comment TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS model_versions (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  version TEXT UNIQUE NOT NULL,
  status TEXT NOT NULL,
  metrics TEXT NOT NULL,
  architecture TEXT,
  dataset_version TEXT,
  class_count INTEGER,
  weights_path TEXT,
  preprocessing_config TEXT,
  threshold_config TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS model_evaluations (
  id TEXT PRIMARY KEY,
  model_version_id TEXT NOT NULL REFERENCES model_versions(id) ON DELETE CASCADE,
  dataset TEXT NOT NULL,
  accuracy DOUBLE PRECISION,
  top3_accuracy DOUBLE PRECISION,
  macro_precision DOUBLE PRECISION,
  macro_recall DOUBLE PRECISION,
  macro_f1 DOUBLE PRECISION,
  weighted_f1 DOUBLE PRECISION,
  cross_domain_macro_f1 DOUBLE PRECISION,
  ood_auroc DOUBLE PRECISION,
  confusion_matrix TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Optional defense-in-depth policies:
-- Set app.user_id from the authenticated backend, then enable RLS on personal tables.
-- Example:
-- ALTER TABLE plants ENABLE ROW LEVEL SECURITY;
-- CREATE POLICY plants_owner ON plants USING (user_id = current_setting('app.user_id', true));
