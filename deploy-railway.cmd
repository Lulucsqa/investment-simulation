@echo off
REM Deploy para Railway - Investment Simulation System

echo 🚀 Deploy para Railway - Investment Simulation System
echo ====================================================
echo.

REM Verificar se Node.js está instalado
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js não está instalado
    echo.
    echo 📥 Instale o Node.js:
    echo    1. Acesse: https://nodejs.org/
    echo    2. Baixe e instale a versão LTS
    echo    3. Execute este script novamente
    echo.
    pause
    exit /b 1
)

echo [INFO] Node.js encontrado ✅
echo.

REM Instalar Railway CLI
echo [INFO] Instalando Railway CLI...
npm install -g @railway/cli

REM Login no Railway
echo.
echo [INFO] Fazendo login no Railway...
railway login

REM Criar projeto
echo.
echo [INFO] Criando projeto no Railway...
railway init

REM Deploy
echo.
echo [INFO] Fazendo deploy para o Railway...
railway up

echo.
echo 🎉 Deploy concluído!
echo.
echo 📊 Sua aplicação estará disponível na URL fornecida pelo Railway
echo.
echo 📝 Comandos úteis:
echo    Ver status: railway status
echo    Ver logs: railway logs
echo    Abrir dashboard: railway open
echo.
pause