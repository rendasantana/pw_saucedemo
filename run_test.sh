#!/bin/bash

# Jalankan pytest dan hasilkan report.html
pytest tests --html=reports/report.html --self-contained-html -s

# Jalankan validasi otomatis setelah selesai
python validate_report.py
