# SimuInvest Imobiliário - Supabase Setup Guide

## Project Configuration

**Project Name:** SimuInvest Imobiliário  
**Project ID:** kjcqoxlusfcndmdtjsks  
**Project URL:** https://kjcqoxlusfcndmdtjsks.supabase.co

## Environment Setup

The project is configured with the following environment variables in `.env.local`:

```bash
VITE_SUPABASE_URL=https://kjcqoxlusfcndmdtjsks.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtqY3FveGx1c2ZjbmRtZHRqc2tzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ0OTY2MzEsImV4cCI6MjA3MDA3MjYzMX0.p77UoH_KZfaDV4AFDiRbaGELm5epLUx6HMyVpaljZJg
```

## CLI Setup Commands

### 1. Link Project
```bash
supabase link --project-ref kjcqoxlusfcndmdtjsks
```

### 2. Create New Migration
```bash
supabase migration new "initial-setup"
```

### 3. Push Database Changes
```bash
supabase db push
```

### 4. Generate Types
```bash
supabase gen types typescript --project-id kjcqoxlusfcndmdtjsks > src/integrations/supabase/types.ts
```

## Edge Functions

### Create Function
```bash
supabase functions new hello-world
```

### Deploy Function
```bash
supabase functions deploy hello-world --project-ref kjcqoxlusfcndmdtjsks
```

### Test Function
```bash
curl -L -X POST 'https://kjcqoxlusfcndmdtjsks.supabase.co/functions/v1/hello-world' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtqY3FveGx1c2ZjbmRtZHRqc2tzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ0OTY2MzEsImV4cCI6MjA3MDA3MjYzMX0.p77UoH_KZfaDV4AFDiRbaGELm5epLUx6HMyVpaljZJg' \
  --data '{"name":"Functions"}'
```

## Database Configuration

- **Password:** Alberteinstein@1981
- **SSL:** Enabled and authorized for this PC
- **Port:** 5432 (default PostgreSQL port)

## Security Notes

- ✅ Row Level Security (RLS) should be enabled for production
- ✅ The anon key is safe for browser use with RLS enabled
- ⚠️ Service role key is for server-side operations only
- ⚠️ Never expose service role key in client-side code

## Quick Start

1. Install Supabase CLI if not already installed:
   ```bash
   npm install -g @supabase/cli
   ```

2. Navigate to the frontend directory:
   ```bash
   cd invest-plan-optimize-main
   ```

3. Link the project:
   ```bash
   supabase link --project-ref kjcqoxlusfcndmdtjsks
   ```

4. Start local development:
   ```bash
   npm run dev
   ```

## Useful Commands

- **Start local Supabase:** `supabase start`
- **Stop local Supabase:** `supabase stop`
- **Reset local database:** `supabase db reset`
- **View logs:** `supabase logs`
- **Open Studio:** `supabase studio`

## Integration Status

✅ Supabase client configured  
✅ Environment variables set  
✅ TypeScript types ready  
✅ Authentication configured  
✅ Project linked  
⏳ Database schema (to be created)  
⏳ RLS policies (to be implemented)  
⏳ Edge functions (to be developed)  

## Next Steps

1. Create database tables for investment simulations
2. Set up Row Level Security policies
3. Implement authentication flows
4. Create Edge functions for complex calculations
5. Set up real-time subscriptions for live updates