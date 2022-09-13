mkdir -p ~/.streamlit/

echo "[theme]
primaryColor = '#f94144'
backgroundColor = '#202124'
secondaryBackgroundColor = '#2c2f38'
textColor = '#ffffff'
font = 'sans serif'
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml