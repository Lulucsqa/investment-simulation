import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://kjcqoxlusfcndmdtjsks.supabase.co'
const supabaseKey = (import.meta as any).env.VITE_SUPABASE_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtqY3FveGx1c2ZjbmRtZHRqc2tzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ0OTY2MzEsImV4cCI6MjA3MDA3MjYzMX0.p77UoH_KZfaDV4AFDiRbaGELm5epLUx6HMyVpaljZJg'

export const supabase = createClient(supabaseUrl, supabaseKey)