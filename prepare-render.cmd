@echo off
REM Preparar para deploy no Render

echo 🚀 Preparando Investment Simulation System para Render
echo ======================================================
echo.

echo [INFO] Verificando arquivos necessários para Render...
echo.

REM Verificar arquivos essenciais
set "files=backend/api.py core.py visualization.py main.py requirements.txt render.yaml"

for %%f in (%files%) do (
    if exist "%%f" (
        echo ✅ %%f
    ) else (
        echo ❌ %%f - ARQUIVO FALTANDO
    )
)

echo.
echo [INFO] Testando importação da API...
python -c "from backend.api import app; print('✅ API importada com sucesso')"

if %errorlevel% neq 0 (
    echo [ERROR] Erro ao importar a API. Verifique o código.
    pause
    exit /b 1
)

echo.
echo [INFO] Verificando dependências...
pip check >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Todas as dependências estão corretas
) else (
    echo ⚠️  Algumas dependências podem ter conflitos
)

echo.
echo 🎯 Seu sistema está pronto para deploy no Render!
echo.
echo 📋 Próximos passos:
echo.
echo 1. Faça commit das mudanças:
echo    git add .
echo    git commit -m "Add Render deployment configuration"
echo    git push origin master
echo.
echo 2. Acesse: https://render.com
echo.
echo 3. Clique "New +" → "Web Service"
echo.
echo 4. Conecte o repositório:
echo    https://github.com/Lulucsqa/investment-simulation
echo.
echo 5. Use estas configurações:
echo    Name: investment-simulation-api
echo    Environment: Python 3
echo    Build Command: pip install -r requirements.txt
echo    Start Command: uvicorn backend.api:app --host 0.0.0.0 --port $PORT
echo    Plan: Free
echo.
echo 6. Adicione variáveis de ambiente:
echo    ENVIRONMENT = production
echo    DEBUG = false
echo    PYTHONPATH = .
echo.
echo 7. Clique "Create Web Service"
echo.
echo 🌐 Sua aplicação estará em:
echo    https://investment-simulation-api.onrender.com
echo.
echo 💡 Vantagens do Render:
echo    ✅ 750 horas gratuitas/mês
echo    ✅ Deploy automático do GitHub
echo    ✅ HTTPS gratuito
echo    ✅ Logs em tempo real
echo    ✅ Interface moderna
echo.
pause