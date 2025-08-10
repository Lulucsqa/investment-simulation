@echo off
REM Deploy para Heroku - Investment Simulation System

echo 🚀 Deploy para Heroku - Investment Simulation System
echo ====================================================
echo.

REM Verificar se Heroku CLI está instalado
heroku --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Heroku CLI não está instalado
    echo.
    echo 📥 Instale o Heroku CLI:
    echo    1. Acesse: https://devcenter.heroku.com/articles/heroku-cli
    echo    2. Baixe e instale o Heroku CLI
    echo    3. Execute este script novamente
    echo.
    pause
    exit /b 1
)

echo [INFO] Heroku CLI encontrado ✅
echo.

REM Verificar se Git está instalado
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git não está instalado
    echo.
    echo 📥 Instale o Git:
    echo    1. Acesse: https://git-scm.com/download/win
    echo    2. Baixe e instale o Git
    echo    3. Execute este script novamente
    echo.
    pause
    exit /b 1
)

echo [INFO] Git encontrado ✅
echo.

REM Login no Heroku
echo [INFO] Fazendo login no Heroku...
heroku login

REM Criar aplicação no Heroku
echo.
echo [INFO] Criando aplicação no Heroku...
set /p APP_NAME="Digite o nome da sua aplicação (ex: meu-simulador-investimentos): "

heroku create %APP_NAME%

REM Inicializar repositório Git se necessário
if not exist ".git" (
    echo [INFO] Inicializando repositório Git...
    git init
    git add .
    git commit -m "Initial commit - Investment Simulation System"
)

REM Adicionar remote do Heroku
heroku git:remote -a %APP_NAME%

REM Deploy
echo.
echo [INFO] Fazendo deploy para o Heroku...
git add .
git commit -m "Deploy to production"
git push heroku main

echo.
echo 🎉 Deploy concluído!
echo.
echo 🌐 Sua aplicação está disponível em:
heroku open

echo.
echo 📊 URLs da sua aplicação:
echo    Frontend/API: https://%APP_NAME%.herokuapp.com
echo    Documentação: https://%APP_NAME%.herokuapp.com/docs
echo.
echo 📝 Comandos úteis:
echo    Ver logs: heroku logs --tail
echo    Abrir app: heroku open
echo    Configurar variáveis: heroku config:set VARIABLE=value
echo.
pause