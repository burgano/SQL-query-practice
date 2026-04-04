@echo off
python3 -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt -q
python3 app.py
