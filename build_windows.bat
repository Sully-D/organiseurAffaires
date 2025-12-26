@echo off
echo Building Organiseur d'Affaires for Windows...
echo.

python -m pip install pyinstaller
if %errorlevel% neq 0 (
    echo Error installing PyInstaller. Make sure Python is added to PATH.
    pause
    exit /b
)

echo.
echo Running PyInstaller...
pyinstaller organiseur.spec --clean --noconfirm

if %errorlevel% neq 0 (
    echo Build FAILED!
    pause
    exit /b
)

echo.
echo Build SUCCESSFUL!
echo The executable is located in the "dist\OrganiseurAffaires" folder.
echo.
pause
