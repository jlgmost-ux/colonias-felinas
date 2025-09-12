@echo off
echo ============================
echo  🚀 Arrancando Colonias Felinas
echo ============================

REM --- Arrancar Docker (si no está ya corriendo) ---
echo 🔹 Asegúrate de que Docker Desktop esté iniciado.

REM --- Backend ---
echo 🔹 Iniciando backend (FastAPI)...
start cmd /k "cd backend && conda activate colonias && uvicorn main:app --reload"

REM --- Frontend ---
echo 🔹 Iniciando frontend (SvelteKit)...
start cmd /k "cd frontend && npm run dev"

echo ============================
echo ✅ Todo arrancado:
echo    - Backend en:  http://localhost:8000
echo    - Frontend en: http://localhost:5173
echo ============================
pause
