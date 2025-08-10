@echo off
REM Deploy para Render - Investment Simulation System

echo 🚀 Investment Simulation System - Render Deployment
echo ===================================================
echo.

echo Render é uma excelente escolha para deploy! 
echo.
echo 📋 Passos para deploy no Render:
echo.
echo 1. Acesse: https://render.com
echo 2. Crie uma conta gratuita (se não tiver)
echo 3. Clique em "New +" no dashboard
echo 4. Selecione "Web Service"
echo 5. Conecte seu repositório GitHub:
echo    https://github.com/Lulucsqa/investment-simulation
echo.
echo 6. Configure o serviço:
echo    - Name: investment-simulation-api
echo    - Environment: Python 3
echo    - Build Command: pip install -r requirements.txt
echo    - Start Command: uvicorn backend.api:app --host 0.0.0.0 --port $PORT
echo    - Plan: Free (para começar)
echo.
echo 7. Adicione variáveis de ambiente:
echo    - ENVIRONMENT = production
echo    - DEBUG = false
echo    - PYTHONPATH = .
echo.
echo 8. Clique "Create Web Service"
echo.
echo ⏱️  O deploy levará cerca de 2-3 minutos
echo.
echo 🌐 Sua aplicação estará disponível em:
echo    https://investment-simulation-api.onrender.com
echo.
echo 📊 URLs importantes:
echo    API: https://seu-app.onrender.com/
echo    Docs: https://seu-app.onrender.com/docs
echo    Health: https://seu-app.onrender.com/
echo.
echo 💡 Vantagens do Render:
echo    ✅ Deploy automático do GitHub
echo    ✅ HTTPS gratuito
echo    ✅ Logs em tempo real
echo    ✅ Fácil configuração
echo    ✅ Plano gratuito generoso
echo.
echo 🔧 Para deploy automático via arquivo render.yaml:
echo    O arquivo render.yaml já foi criado no seu projeto
echo    Basta fazer commit e push para o GitHub
echo.
pause