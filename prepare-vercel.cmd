@echo off
REM Preparar projeto para deploy no Vercel

echo 🔧 Preparando projeto para deploy no Vercel
echo ============================================
echo.

REM Verificar estrutura do projeto
echo [INFO] Verificando estrutura do projeto...

if not exist "package.json" (
    echo [ERROR] package.json não encontrado no diretório raiz
    echo [INFO] Copiando package.json do frontend...
    copy "frontend\package.json" "package.json"
)

if not exist "vite.config.ts" (
    echo [INFO] Copiando vite.config.ts do frontend...
    copy "frontend\vite.config.ts" "vite.config.ts"
)

if not exist "tsconfig.json" (
    echo [INFO] Copiando tsconfig.json do frontend...
    copy "frontend\tsconfig.json" "tsconfig.json"
)

if not exist "src" (
    echo [INFO] Copiando pasta src do frontend...
    xcopy "frontend\src" "src" /E /I /Y
)

if not exist "public" (
    echo [INFO] Copiando pasta public do frontend...
    xcopy "frontend\public" "public" /E /I /Y
)

if not exist "index.html" (
    echo [INFO] Copiando index.html do frontend...
    copy "frontend\index.html" "index.html"
)

echo [INFO] Estrutura do projeto preparada ✅
echo.

echo [INFO] Verificando dependências...
if not exist "node_modules" (
    echo [INFO] Instalando dependências...
    npm install
) else (
    echo [INFO] Dependências já instaladas ✅
)

echo.
echo [INFO] Testando build...
npm run build

if %errorlevel% equ 0 (
    echo [INFO] Build teste bem-sucedido ✅
    echo.
    echo 🎉 Projeto preparado para deploy!
    echo.
    echo 📝 Próximos passos:
    echo    1. Execute: vercel login
    echo    2. Execute: vercel --prod
    echo.
) else (
    echo [ERROR] Falha no build teste
    echo Corrija os erros antes de fazer deploy
)

pause