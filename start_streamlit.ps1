$email = ""
$proc = Start-Process -FilePath "streamlit" -ArgumentList "run", "streamlit_app.py", "--server.port", "8501", "--server.headless", "true" -PassThru -WindowStyle Hidden
Start-Sleep 5
if (!$proc.HasExited) {
    Write-Host "Streamlit应用已启动，请在浏览器中访问 http://localhost:8501"
}
