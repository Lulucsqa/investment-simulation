@echo off
REM Deploy no Render com Supabase já configurado

echo 🚀 Deploy no Render - Sistema Já Configurado com Supabase
echo =========================================================
echo.

echo ✅ Seu projeto já tem:
echo    - Supabase configurado: kjcqoxlusfcndmdtjsks.supabase.co
echo    - Frontend React com integração
echo    - Backend Python com API
echo    - Todas as credenciais configuradas
echo.

echo 📋 Para fazer deploy no Render:
echo.
echo 1. Acesse: https://render.com
echo 2. Clique "New +" → "Web Service"
echo 3. Conecte: https://github.com/Lulucsqa/investment-simulation
echo.
echo 4. Configure o serviço:
echo    Name: investment-simulation-api
echo    Environment: Python 3
echo    Build Command: pip install -r requirements.txt
echo    Start Command: uvicorn backend.api:app --host 0.0.0.0 --port $PORT
echo    Plan: Free
echo.
echo 5. Adicione estas variáveis de ambiente:
echo    SUPABASE_URL=https://kjcqoxlusfcndmdtjsks.supabase.co
echo    SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtqY3FveGx1c2ZjbmRtZHRqc2tzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ0OTY2MzEsImV4cCI6MjA3MDA3MjYzMX0.p77UoH_KZfaDV4AFDiRbaGELm5epLUx6HMyVpaljZJg
echo    ENVIRONMENT=production
echo    DEBUG=false
echo    PYTHONPATH=.
echo.
echo 6. Clique "Create Web Service"
echo.
echo 🌐 Sua aplicação estará em:
echo    https://investment-simulation-api.onrender.com
echo.
echo 📊 Com Supabase integrado, você terá:
echo    ✅ Persistência de todas as simulações
echo    ✅ Histórico por usuário
echo    ✅ Estatísticas de uso
echo    ✅ Dashboard administrativo
echo    ✅ API completa com banco de dados
echo.
echo 🎯 Endpoints disponíveis:
echo    POST /simulate/cdi (salva no banco)
echo    POST /simulate/ipca (salva no banco)
echo    GET /history/usuario@email.com
echo    GET /stats
echo    GET /health/database
echo.
pause