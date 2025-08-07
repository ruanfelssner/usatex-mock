@echo off
echo ====================================================
echo            USATEX - SISTEMA DE ATUALIZACAO
echo ====================================================
echo.
echo Escolha uma opcao:
echo.
echo [1] Processamento completo (recomendado)
echo [2] Preview das mudancas
echo [3] Apenas validar imagens
echo [4] Buscar duplicatas
echo [5] Apenas mockups
echo [0] Sair
echo.
set /p opcao="Digite sua opcao: "

if "%opcao%"=="1" (
    echo.
    echo Executando processamento completo...
    python update.py
) else if "%opcao%"=="2" (
    echo.
    echo Mostrando preview das mudancas...
    python update.py --preview
) else if "%opcao%"=="3" (
    echo.
    echo Validando imagens...
    python update.py --validate
) else if "%opcao%"=="4" (
    echo.
    echo Buscando duplicatas...
    python update.py --duplicates
) else if "%opcao%"=="5" (
    echo.
    echo Atualizando mockups...
    python update.py --mockups
) else if "%opcao%"=="0" (
    echo Saindo...
    exit /b 0
) else (
    echo Opcao invalida!
)

echo.
echo ====================================================
echo                  OPERACAO CONCLUIDA
echo ====================================================
pause
