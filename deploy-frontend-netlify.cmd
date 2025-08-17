@echo off
REM Deploy do Frontend React no Netlify

echo 🚀 Deploy do Frontend React no Netlify
echo =======================================

echo 📋 Para fazer deploy no Netlify:
echo.
echo 1. Acesse: https://netlify.com
echo 2. Faça login com GitHub
echo 3. Clique "New site from Git"
echo 4. Selecione: Lulucsqa/investment-simulation
echo 5. Configure:
echo    - Base directory: frontend
echo    - Build command: npm run build
echo    - Publish directory: frontend/dist
echo.
echo 6. Adicione variáveis de ambiente:
echo    VITE_SUPABASE_URL=https://kjcqoxlusfcndmdtjsks.supabase.co
echo    VITE_SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtqY3FveGx1c2ZjbmRtZHRqc2tzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ0OTY2MzEsImV4cCI6MjA3MDA3MjYzMX0.p77UoH_KZfaDV4AFDiRbaGELm5epLUx6HMyVpaljZJg
echo    VITE_API_URL=https://investment-simulation-api-xr7m.onrender.com
echo.
echo 7. Clique "Deploy site"
echo.
echo 🌐 Seu frontend estará em:
echo    https://investment-simulation.netlify.app
echo.
pause