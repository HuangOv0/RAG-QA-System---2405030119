@echo off
echo ====================================
echo RAG智能问答系统 - 启动脚本
echo ====================================
echo.

echo 检查Python环境...
python --version
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.10+
    pause
    exit /b 1
)

echo.
echo 检查依赖包...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo 错误: 依赖包安装失败
        pause
        exit /b 1
    )
)

echo.
echo 检查Ollama服务...
ollama list >nul 2>&1
if errorlevel 1 (
    echo 警告: 未找到Ollama，请先安装并启动Ollama服务
    echo 下载地址: https://ollama.com/
    echo.
    echo 是否继续启动应用？ (Y/N)
    set /p continue="请输入选择: "
    if /i not "%continue%"=="Y" (
        pause
        exit /b 1
    )
)

echo.
echo 启动RAG智能问答系统...
echo.
streamlit run app.py

pause