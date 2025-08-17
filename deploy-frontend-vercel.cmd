@echo off
REM Deploy do Frontend React no Vercel

echo 🚀 Deploy do Frontend React - Investment Simulation System
echo =========================================================

echo ✅ Seu frontend React já está pronto em:
echo    - Pasta: frontend/
echo    - Integração Supabase: Configurada
echo    - Componentes: React + TypeScript + Tailwind
echo.

echo 📋 Para fazer deploy no Vercel:
echo.
echo 1. Acesse: https://vercel.com
echo 2. Faça login com GitHub
echo 3. Clique "New Project"
echo 4. Selecione: Lulucsqa/investment-simulation
echo 5. Configure:
echo    - Framework Preset: Vite
echo    - Root Directory: frontend
echo    - Build Command: npm run build
echo    - Output Directory: dist
echo.
echo 6. Adicione variáveis de ambiente:
echo    VITE_SUPABASE_URL=https://kjcqoxlusfcndmdtjsks.supabase.co
echo    VITE_SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtqY3FveGx1c2ZjbmRtZHRqc2tzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ0OTY2MzEsImV4cCI6MjA3MDA3MjYzMX0.p77UoH_KZfaDV4AFDiRbaGELm5epLUx6HMyVpaljZJg
echo    VITE_API_URL=https://investment-simulation-api-xr7m.onrender.com
echo.
echo 7. Clique "Deploy"
echo.
echo 🌐 Seu frontend estará em:
echo    https://investment-simulation-frontend.vercel.app
echo.
echo 💡 Vantagens do Vercel:
echo    ✅ Deploy automático do GitHub
echo    ✅ CDN global ultra-rápido
echo    ✅ HTTPS gratuito
echo    ✅ Preview de Pull Requests
echo    ✅ Domínio personalizado gratuito
echo.
pause