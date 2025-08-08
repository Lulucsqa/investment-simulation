# SimuInvest Imobiliário - Supabase Configuration

## 🎯 Project Overview

**SimuInvest Imobiliário** is a comprehensive investment simulation system that analyzes and compares different real estate investment strategies against traditional fixed-income investments.

### Project Details
- **Name:** SimuInvest Imobiliário
- **Project ID:** kjcqoxlusfcndmdtjsks
- **URL:** https://kjcqoxlusfcndmdtjsks.supabase.co
- **Database Password:** Alberteinstein@1981

## 🔧 Configuration Files

### Environment Variables (`.env.local`)
```bash
VITE_SUPABASE_URL=https://kjcqoxlusfcndmdtjsks.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_JWT_SECRET=7Cxns9USCJFx/+QFAvvmWGq1DsRa8pUlOXpsZY0l/UY...
SUPABASE_ACCESS_TOKEN=sbp_3dbb8ad69d3a74c6ba92e371c6ff61e1a7a1b219
DATABASE_PASSWORD=Alberteinstein@1981
```

### Supabase Config (`supabase/config.toml`)
Complete configuration for local development with all services enabled.

### Client Configuration (`src/integrations/supabase/client.ts`)
- Environment variable-based configuration
- Type-safe database operations
- Automatic authentication persistence
- PKCE flow for enhanced security

## 🚀 Quick Start

### 1. Install Dependencies
```bash
npm install @supabase/supabase-js
npm install -g @supabase/cli
```

### 2. Link Project
```bash
supabase link --project-ref kjcqoxlusfcndmdtjsks
```

### 3. Test Connection
```bash
npm run dev
# Then import and run the test function:
# import { testSupabaseConnection } from './src/test-supabase';
# testSupabaseConnection();
```

## 📊 Available Utilities

### Authentication (`src/lib/supabase-utils.ts`)
- `auth.getCurrentUser()` - Get current user
- `auth.signIn(email, password)` - Sign in user
- `auth.signUp(email, password)` - Register user
- `auth.signOut()` - Sign out user
- `auth.resetPassword(email)` - Reset password

### Database Operations
- `db.testConnection()` - Test database connectivity
- `db.getHealthStatus()` - Get database health metrics

### Storage Operations
- `storage.uploadFile()` - Upload files
- `storage.downloadFile()` - Download files
- `storage.getPublicUrl()` - Get public URLs
- `storage.deleteFile()` - Delete files

### Real-time Features
- `realtime.subscribeToTable()` - Subscribe to table changes
- `realtime.unsubscribe()` - Unsubscribe from channels

## 🔐 Security Configuration

### API Keys
- **Anon Key:** Safe for browser use with RLS enabled
- **Service Role Key:** Server-side only, never expose to client
- **JWT Secret:** For local development and token validation

### Row Level Security (RLS)
RLS should be enabled for all tables in production:
```sql
ALTER TABLE your_table ENABLE ROW LEVEL SECURITY;
```

### SSL Configuration
- SSL is enabled and authorized for this PC
- All connections use HTTPS/SSL encryption

## 🛠️ CLI Commands

### Project Management
```bash
# Link project
supabase link --project-ref kjcqoxlusfcndmdtjsks

# Start local development
supabase start

# Stop local services
supabase stop

# Reset local database
supabase db reset
```

### Migrations
```bash
# Create new migration
supabase migration new "migration-name"

# Push changes to remote
supabase db push

# Pull changes from remote
supabase db pull
```

### Edge Functions
```bash
# Create new function
supabase functions new function-name

# Deploy function
supabase functions deploy function-name --project-ref kjcqoxlusfcndmdtjsks

# Test function locally
supabase functions serve
```

### Type Generation
```bash
# Generate TypeScript types
supabase gen types typescript --project-id kjcqoxlusfcndmdtjsks > src/integrations/supabase/types.ts
```

## 📁 File Structure

```
invest-plan-optimize-main/
├── .env.local                          # Environment variables
├── .supabaserc                         # CLI configuration
├── supabase/
│   ├── config.toml                     # Supabase configuration
│   └── migrations/                     # Database migrations
├── src/
│   ├── integrations/supabase/
│   │   ├── client.ts                   # Supabase client
│   │   └── types.ts                    # Generated types
│   ├── lib/
│   │   └── supabase-utils.ts          # Utility functions
│   └── test-supabase.ts               # Connection test
├── setup-supabase.md                  # Setup guide
└── SUPABASE_README.md                 # This file
```

## 🧪 Testing

### Connection Test
Run the connection test to verify everything is working:
```typescript
import { testSupabaseConnection } from './src/test-supabase';
testSupabaseConnection();
```

### Health Check
```typescript
import { db } from './src/lib/supabase-utils';
const health = await db.getHealthStatus();
console.log(health);
```

## 🔄 Next Steps

1. **Database Schema:** Create tables for investment simulations
2. **Authentication:** Implement user registration and login flows
3. **RLS Policies:** Set up Row Level Security for data protection
4. **Edge Functions:** Create functions for complex calculations
5. **Real-time:** Implement live updates for simulation results
6. **Storage:** Set up file storage for reports and charts

## 📞 Support

For Supabase-related issues:
- Check the [Supabase Documentation](https://supabase.com/docs)
- Use the connection test script to diagnose problems
- Verify environment variables are correctly set
- Ensure RLS policies are properly configured

## 🔒 Security Checklist

- [ ] Environment variables are not committed to git
- [ ] RLS is enabled on all tables
- [ ] Service role key is never exposed to client
- [ ] SSL/HTTPS is used for all connections
- [ ] Authentication flows are properly implemented
- [ ] Database passwords are secure and rotated regularly

---

**Project:** SimuInvest Imobiliário  
**Supabase Project ID:** kjcqoxlusfcndmdtjsks  
**Last Updated:** January 2025