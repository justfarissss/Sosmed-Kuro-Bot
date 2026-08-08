# Menggunakan Python versi ringan
FROM python:3.11-slim

# Menentukan direktori kerja di dalam container
WORKDIR /app

# Menyalin requirements dan menginstal library
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin seluruh kode bot (cogs, file utama, dll)
COPY . .

# Perintah utama untuk menjalankan bot
CMD ["python", "bot.py"]