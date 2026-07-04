@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================
echo   RAG Chatbot API - Flask RESTful 服务
echo ============================================
echo.

REM 检查虚拟环境
if not exist "venv\Scripts\python.exe" (
    echo [错误] 未找到虚拟环境，正在创建...
    python -m venv venv
    echo [信息] 正在安装依赖...
    venv\Scripts\python.exe -m pip install -r requirements_chroma.txt
)

REM 检查 .env 文件
if not exist ".env" (
    echo [错误] .env 文件不存在
    pause
    exit /b 1
)

REM 检查 API Key 是否已配置
venv\Scripts\python.exe -c "import os; from dotenv import load_dotenv; load_dotenv(); key=os.getenv('DASHSCOPE_API_KEY',''); exit(0 if key and key!='your-api-key-here' else 1)" 2>nul
if errorlevel 1 (
    echo [警告] 请先在 .env 文件中配置 DASHSCOPE_API_KEY
    echo.
)

echo 启动 Flask API 服务...
echo 接口地址: http://localhost:5000/api/gen
echo 前端页面：http://localhost:5000/index
echo 按 Ctrl+C 可停止服务
echo.

venv\Scripts\python.exe -m flask --app flaskr run --host=0.0.0.0 --port=5000 --debug
pause
