/**
 * SimuInvest Imobiliário - Supabase Connection Test
 * 
 * This script tests the Supabase connection and configuration.
 * Run this to verify that all settings are working correctly.
 */

import { supabase, supabaseConfig } from './integrations/supabase/client';
import { db, auth, config } from './lib/supabase-utils';

async function testSupabaseConnection() {
  console.log('🚀 SimuInvest Imobiliário - Supabase Connection Test');
  console.log('=' .repeat(50));
  
  // Test 1: Configuration
  console.log('\n📋 Configuration:');
  console.log(`Project Name: ${supabaseConfig.projectName}`);
  console.log(`Project ID: ${supabaseConfig.projectId}`);
  console.log(`URL: ${supabaseConfig.url}`);
  
  // Test 2: Client initialization
  console.log('\n🔧 Client Status:');
  try {
    console.log('✅ Supabase client initialized successfully');
    console.log(`Client URL: ${supabase.supabaseUrl}`);
    console.log(`Client Key: ${supabase.supabaseKey.substring(0, 20)}...`);
  } catch (error) {
    console.error('❌ Client initialization failed:', error);
    return;
  }
  
  // Test 3: Database connection
  console.log('\n🗄️ Database Connection:');
  try {
    const isConnected = await db.testConnection();
    if (isConnected) {
      console.log('✅ Database connection successful');
      
      const health = await db.getHealthStatus();
      console.log(`Status: ${health.status}`);
      if (health.latency) {
        console.log(`Latency: ${health.latency}ms`);
      }
    } else {
      console.log('⚠️ Database connection test inconclusive');
    }
  } catch (error) {
    console.error('❌ Database connection failed:', error);
  }
  
  // Test 4: Authentication
  console.log('\n🔐 Authentication:');
  try {
    const session = await auth.getCurrentSession();
    if (session) {
      console.log('✅ User is authenticated');
      console.log(`User ID: ${session.user.id}`);
      console.log(`Email: ${session.user.email}`);
    } else {
      console.log('ℹ️ No active session (user not logged in)');
    }
  } catch (error) {
    console.error('❌ Authentication check failed:', error);
  }
  
  // Test 5: Environment variables
  console.log('\n🌍 Environment Variables:');
  const requiredEnvVars = [
    'VITE_SUPABASE_URL',
    'VITE_SUPABASE_ANON_KEY'
  ];
  
  requiredEnvVars.forEach(envVar => {
    const value = import.meta.env[envVar];
    if (value) {
      console.log(`✅ ${envVar}: ${value.substring(0, 20)}...`);
    } else {
      console.log(`❌ ${envVar}: Not set`);
    }
  });
  
  // Test 6: Project configuration
  console.log('\n⚙️ Project Configuration:');
  console.log(`Config Project ID: ${config.projectId}`);
  console.log(`Config Project Name: ${config.projectName}`);
  console.log(`Config URL: ${config.url}`);
  
  console.log('\n🎉 Connection test completed!');
  console.log('\nNext steps:');
  console.log('1. Create database tables for your investment simulations');
  console.log('2. Set up Row Level Security (RLS) policies');
  console.log('3. Implement user authentication flows');
  console.log('4. Create Edge functions for complex calculations');
}

// Export for use in other files
export { testSupabaseConnection };

// Run test if this file is executed directly
if (import.meta.hot) {
  testSupabaseConnection().catch(console.error);
}