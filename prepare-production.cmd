@echo off
REM Preparar sistema para produção

echo 🚀 Preparando Investment Simulation System para Produção
echo ========================================================
echo.

REM Criar .gitignore se não existir
if not exist ".gitignore" (
    echo [INFO] Criando .gitignore...
    echo __pycache__/ > .gitignore
    echo *.pyc >> .gitignore
    echo .env >> .gitignore
    echo .pytest_cache/ >> .gitignore
    echo outputs/*.jpg >> .gitignore
    echo node_modules/ >> .gitignore
    echo .DS_Store >> .gitignore
    echo Thumbs.db >> .gitignore
)

REM Atualizar requirements.txt
echo [INFO] Atualizando requirements.txt...
pip freeze > requirements.txt

REM Criar arquivo de configuração de produção
echo [INFO] Criando configuração de produção...
echo # Production Environment Variables > .env.production
echo ENVIRONMENT=production >> .env.production
echo DEBUG=false >> .env.production
echo API_HOST=0.0.0.0 >> .env.production
echo API_PORT=8000 >> .env.production
echo CORS_ORIGINS=https://seu-dominio.com >> .env.production

REM Testar se a aplicação funciona
echo [INFO] Testando aplicação...
python -c "from backend.api import app; print('✅ API importada com sucesso')"

if %errorlevel% neq 0 (
    echo [ERROR] Erro ao importar a API. Verifique o código.
    pause
    exit /b 1
)

REM Verificar se todos os arquivos necessários existem
echo [INFO] Verificando arquivos necessários...

set "files=backend/api.py core.py visualization.py main.py requirements.txt Procfile runtime.txt"

for %%f in (%files%) do (
    if exist "%%f" (
        echo ✅ %%f
    ) else (
        echo ❌ %%f - ARQUIVO FALTANDO
    )
)

echo.
echo 🎯 Opções de Deploy Disponíveis:
echo ================================
echo.
echo 1. Heroku (Recomendado - Mais Simples)
echo    Comando: deploy-heroku.cmd
echo.
echo 2. Vercel (Serverless - Rápido)
echo    Comando: deploy-vercel.cmd
echo.
echo 3. Railway (Moderno)
echo    Comando: deploy-railway.cmd
echo.
echo 4. PythonAnywhere (Python Especializado)
echo    Manual: Consulte PRODUCTION_GUIDE.md
echo.
echo 📚 Para instruções detalhadas, consulte: PRODUCTION_GUIDE.md
echo.

set /p choice="Escolha uma opção (1-4) ou pressione Enter para sair: "

if "%choice%"=="1" (
    echo [INFO] Iniciando deploy no Heroku...
    call deploy-heroku.cmd
) else if "%choice%"=="2" (
    echo [INFO] Iniciando deploy no Vercel...
    call deploy-vercel.cmd
) else if "%choice%"=="3" (
    echo [INFO] Iniciando deploy no Railway...
    call deploy-railway.cmd
) else if "%choice%"=="4" (
    echo [INFO] Consulte PRODUCTION_GUIDE.md para instruções do PythonAnywhere
    start PRODUCTION_GUIDE.md
) else (
    echo [INFO] Preparação concluída. Execute um dos scripts de deploy quando estiver pronto.
)

echo.
echo ✅ Sistema preparado para produção!
pause