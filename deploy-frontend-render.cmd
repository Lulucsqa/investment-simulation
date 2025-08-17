@echo off
REM Deploy do Frontend React no Render

echo 🚀 Deploy do Frontend React no Render
echo ======================================

echo 📋 Para fazer deploy no Render:
echo.
echo 1. No dashboard do Render, clique "New +"
echo 2. Selecione "Static Site"
echo 3. Conecte: Lulucsqa/investment-simulation
echo 4. Configure:
echo    - Name: investment-simulation-frontend
echo    - Root Directory: frontend
echo    - Build Command: npm run build
echo    - Publish Directory: frontend/dist
echo.
echo 5. Adicione variáveis de ambiente:
echo    VITE_SUPABASE_URL=https://kjcqoxlusfcndmdtjsks.supabase.co
echo    VITE_SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtqY3FveGx1c2ZjbmRtZHRqc2tzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ0OTY2MzEsImV4cCI6MjA3MDA3MjYzMX0.p77UoH_KZfaDV4AFDiRbaGELm5epLUx6HMyVpaljZJg
echo    VITE_API_URL=https://investment-simulation-api-xr7m.onrender.com
echo.
echo 6. Clique "Create Static Site"
echo.
echo 🌐 Seu frontend estará em:
echo    https://investment-simulation-frontend.onrender.com
echo.
pause