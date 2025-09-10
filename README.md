# Pet Shop เว็บไซต์ สร้างด้วย Python Django Framework

## โครงสร้างโปรเจค
```
ecommerce/              # โฟลเดอร์หลักของโปรเจค
├── env/                # Virtual Environment
├── mysite/             # ตัวเว็บไซต์หลัก
├── blog/               # แอพพลิเคชั่น blog
└── db.sqlite3          # ฐานข้อมูล
```

## ขั้นตอนการติดตั้งและรัน Project

### 1. สร้าง Virtual Environment
```bash
# สร้างโฟลเดอร์เพื่อเก็บโปรเจคท์
mkdir ecommerce
cd ecommerce

# สร้าง virtual environment
python -m venv env

# เปิดใช้งาน virtual environment
# สำหรับ Windows
env\Scripts\activate

# สำหรับ Mac/Linux
source env/bin/activate
```

### 2. ติดตั้ง Django
```bash
pip install django
```

### 3. สร้างโปรเจค Django
```bash
django-admin startproject mysite .
```

### 4. สร้าง App
```bash
python manage.py startapp blog
```

### 5. ตั้งค่าฐานข้อมูล
```bash
# สร้างไฟล์การอัพเดทฐานข้อมูล
python manage.py makemigrations

# อัพเดทฐานข้อมูล
python manage.py migrate
```

### 6. สร้าง Superuser (ผู้ดูแลระบบ)
```bash
python manage.py createsuperuser
# ใส่ username
# ใส่ email (หรือกด Enter เพื่อข้าม)
# ใส่ password (password จะไม่โชว์ในหน้านี้)
# ยืนยัน password
```

### 7. รันเซิร์ฟเวอร์
```bash
python manage.py runserver
```

## การเข้าใช้งาน

1. หน้าเว็บไซต์หลัก: http://127.0.0.1:8000/
   - จะเห็นหน้า Welcome to Django

   <img src="https://drive.google.com/uc?export=view&id=1octX1nGpWDM7f0B-qnP-LMdivX9BYETO" alt="Django Welcome Page" width="600"/>

2. หน้า Admin: http://127.0.0.1:8000/admin
   - เข้าสู่ระบบด้วย superuser ที่สร้างไว้

   <img src="https://drive.google.com/uc?export=view&id=1pvaIfz9N1N9P7FlZdsdi2SJTBik__k-f" alt="Django Admin Login" width="600"/>

## หมายเหตุสำคัญ
- ต้องเปิด virtual environment ทุกครั้งก่อนรันโปรเจค
- ถ้าเจอ error ให้ตรวจสอบว่าได้รัน migrate แล้วหรือยัง
- ไฟล์ `db.sqlite3` จะถูกสร้างหลังจากรัน migrate ครั้งแรก

## คำสั่งที่ใช้บ่อย
```bash
# เปิด virtual environment
source env/bin/activate  # (Mac/Linux)
env\Scripts\activate    # (Windows)

# รันเซิร์ฟเวอร์
python manage.py runserver

# ปิด virtual environment
deactivate
```

## การแก้ปัญหาเบื้องต้น

1. ถ้ารันเซิร์ฟเวอร์ไม่ได้:
   - ตรวจสอบว่าเปิด virtual environment แล้ว
   - ตรวจสอบว่าอยู่ในโฟลเดอร์ที่มีไฟล์ manage.py

2. ถ้าเข้า admin ไม่ได้:
   - ตรวจสอบว่ารัน migrate แล้ว
   - ตรวจสอบว่าสร้าง superuser แล้ว

3. ถ้าลืม password superuser:
   ```bash
   python manage.py changepassword username
   ```