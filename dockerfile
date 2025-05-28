# Rasm sifatida Python 3.10 dan foydalanamiz
FROM python:3.10
RUN pip install --upgrade pip
# Loyihani ichki katalogga nusxalash
WORKDIR /app

# requirements.txt faylini konteynerga qo‘shamiz
COPY requirements.txt .

# Zarur kutubxonalarni o‘rnatamiz
RUN pip install --no-cache-dir -r requirements.txt


# Boshqa barcha fayllarni konteynerga nusxalaymiz
COPY . .

# Django uchun port
EXPOSE 8000

# Loyihani ishga tushirish
CMD ["python", "manage.py", "runserver", " 0.0.0.0:8000"]
