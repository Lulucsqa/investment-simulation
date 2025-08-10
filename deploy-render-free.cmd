@echo off
REM Deploy 100% gratuito no Render

echo 🚀 Deploy 100%% GRATUITO no Render - Investment Simulation System
echo ================================================================

echo.
echo ✅ Render oferece:
echo    - Plano gratuito permanente
echo    - 750 horas/mês (suficiente para uso pessoal)
echo    - HTTPS automático
echo    - Deploy via GitHub
echo.

echo ⚠️  Limitações do plano gratuito:
echo    - App "dorme" após 15 minutos sem uso
echo    - Pode demorar 30s para "acordar"
echo    - Perfeito para desenvolvimento e demonstrações
echo.

echo 📋 Passos para deploy:
echo.
echo 1. Acesse: https://render.com/
echo 2. Clique em "Get Started for Free"
echo 3. Conecte sua conta GitHub
echo 4. Clique em "New +" e selecione "Web Service"
echo 5. Selecione o repositório: Lulucsqa/investment-simulation
echo 6. Configure:
echo    - Name: investment-simulation
echo    - Environment: Python 3
echo    - Build Command: pip install -r requirements.txt
echo    - Start Command: uvicorn backend.api:app --host 0.0.0.0 --port $PORT
echo 7. Clique em "Create Web Service"
echo.

echo 🌐 Sua aplicação estará disponível em:
echo    https://investment-simulation.onrender.com
echo.

echo 💰 Custo: 100%% GRATUITO
echo.

set /p choice="Pressione Enter para abrir Render no navegador..."
start https://render.com/

pause