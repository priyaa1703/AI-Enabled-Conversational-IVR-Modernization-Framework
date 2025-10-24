Start-Process powershell -ArgumentList "uvicorn backend:app --reload"
Start-Sleep -Seconds 3
Start-Process powershell -ArgumentList "C:\Users\Ashwin\ngrok.exe http 8000"
