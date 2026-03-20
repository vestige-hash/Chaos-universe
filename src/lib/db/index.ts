import { neon } from '@neondatabase/serverless';
import { drizzle } from 'drizzle-orm/neon-http';
import { getEnv } from '@/lib/env';
import * as schema from './schema';

function createDb() {
  const env = getEnv();
  if (!env.DATABASE_URL) {
    throw new Error('DATABASE_URL is required for database operations');
  }

  const sql = neon(env.DATABASE_URL);
  return drizzle(sql, { schema });
}

// Lazy initialization — only connects when actually used
let _db: ReturnType<typeof createDb> | null = null;

export function getDb() {
  if (!_db) {
    _db = createDb();
  }
  return _db;
}
