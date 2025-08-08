/**
 * SimuInvest Imobiliário - Supabase Client Configuration
 * 
 * This file configures the Supabase client for the investment simulation system.
 * It uses environment variables for secure credential management.
 */

import { createClient } from '@supabase/supabase-js';
import type { Database } from './types';

// Get configuration from environment variables
const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL || "https://kjcqoxlusfcndmdtjsks.supabase.co";
const SUPABASE_ANON_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY || "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtqY3FveGx1c2ZjbmRtZHRqc2tzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ0OTY2MzEsImV4cCI6MjA3MDA3MjYzMX0.p77UoH_KZfaDV4AFDiRbaGELm5epLUx6HMyVpaljZJg";

// Validate required environment variables
if (!SUPABASE_URL || !SUPABASE_ANON_KEY) {
  throw new Error('Missing required Supabase environment variables. Please check your .env.local file.');
}

/**
 * Main Supabase client instance for SimuInvest Imobiliário
 * 
 * Features:
 * - Automatic authentication persistence
 * - Auto-refresh tokens
 * - Local storage for session management
 * - Type-safe database operations
 * 
 * Usage:
 * import { supabase } from "@/integrations/supabase/client";
 */
export const supabase = createClient<Database>(SUPABASE_URL, SUPABASE_ANON_KEY, {
  auth: {
    storage: localStorage,
    persistSession: true,
    autoRefreshToken: true,
    detectSessionInUrl: true,
    flowType: 'pkce'
  },
  db: {
    schema: 'public'
  },
  global: {
    headers: {
      'X-Client-Info': 'simuinvest-imobiliario@1.0.0'
    }
  }
});

// Export project configuration for reference
export const supabaseConfig = {
  url: SUPABASE_URL,
  projectId: 'kjcqoxlusfcndmdtjsks',
  projectName: 'SimuInvest Imobiliário'
} as const;