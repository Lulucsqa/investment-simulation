@echo off
echo 🚀 Deploy Rápido no Vercel
echo ==========================
echo.

echo [1/3] Verificando build...
npm run build
if %errorlevel% neq 0 (
    echo ❌ Erro no build - corrija antes de continuar
    pause
    exit /b 1
)

echo ✅ Build OK
echo.

echo [2/3] Fazendo login no Vercel...
echo (Se já estiver logado, será pulado)
vercel login

echo.
echo [3/3] Fazendo deploy...
vercel --prod

echo.
echo 🎉 Deploy concluído!
echo Sua aplicação está online na URL mostrada acima
echo.
pause