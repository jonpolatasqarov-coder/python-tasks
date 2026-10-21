# 🚗 Avtomobil Ijarasi Tizimi (Car Rental System)

Python dasturlash tilida yaratilgan, transport vositalarini ijaraga berish va boshqarish tizimi.

## 🧠 OOP Konseptlari

- Abstract Base Class
- Class Inheritance
- Method Overriding
- Encapsulation
- File I/O

## 📋 Vazifalar

1. `Vehicle` abstract classini hamda undan voris oluvchi `Car`, `Truck` va `Bike` klasslarini yaratish.
2. Har bir transport turi uchun `rent()`, `return_vehicle()` va `calculate_rent()` metodlarini amalga oshirish.
3. Har bir ijara va qaytarish jarayonini `rental.log` fayliga yozib borish.
4. Transport vositalarini nomi, turi va kunlik narxi bo‘yicha qidirish imkoniyatini yaratish.
5. Transport ijaraga berilganda va qaytarilganda uning mavjudlik holatini yangilash.
6. Oldingi ijara soniga asoslangan chegirma tizimini amalga oshirish.
7. `FleetManager` klassi orqali transport vositalari, mijozlar va ijara jarayonlarini boshqarish.
8. Transport vositalari, mijozlar va ijara ma’lumotlarini JSON fayllarida saqlash va qayta yuklash.

## ✨ Asosiy imkoniyatlar

- **Transport vositalarini boshqarish:** avtomobil, yuk mashinasi va mototsikllarni boshqarish.
- **Transport qidirish:** nomi, turi va maksimal kunlik narxi bo‘yicha qidirish.
- **Ijara tizimi:** mavjud transport vositalarini belgilangan muddatga ijaraga olish.
- **Qaytarish tizimi:** ijaradagi transport vositalarini qaytarish va mavjudlik holatini yangilash.
- **Mijozlarni boshqarish:** mijozlarni ro‘yxatdan o‘tkazish va ijara tarixini saqlash.
- **Chegirmalar tizimi:** oldingi ijaralar soniga asoslangan chegirmalarni qo‘llash.
- **Ijara tarixi:** ijara muddati, narxi va kutilayotgan qaytarish sanasini kuzatish.
- **Log yuritish:** ijara va qaytarish jarayonlarini `rental.log` fayliga yozish.
- **Ma’lumotlarni saqlash:** JSON fayllari orqali ma’lumotlarni saqlash va qayta yuklash.

## 📁 Ma’lumotlar fayllari

- `vehicles.json` — transport vositalari va ularning mavjudlik holati.
- `customers.json` — mijozlar va ularning ijara statistikasi.
- `rentals.json` — ijara yozuvlari va qaytarish holati.
- `rental.log` — ijara va qaytarish jarayonlari jurnali.

## 📦 Talablar

- Python 3.10 yoki undan yangi versiya tavsiya etiladi.
- Loyihaning asosiy funksiyalarini ishlatish uchun qo‘shimcha Python kutubxonalarini o‘rnatish talab qilinmaydi.

### Foydalanilgan modullar

- `json` — ma’lumotlarni JSON formatida saqlash va o‘qish.
- `datetime` — ijara va qaytarish sanalarini hisoblash.
- `timedelta` — ijara muddatini hisoblash.

Ushbu modullar Python standart kutubxonasiga kiradi.

## ⚙️ O‘rnatish va ishga tushirish

1. Repository’ni yuklab oling yoki clone qiling.
2. Terminalni loyiha papkasida oching.
3. Dasturni quyidagi buyruq orqali ishga tushiring:

   ```bash
   py main.py
   ```

## 🛠️ Foydalanilgan texnologiyalar

- Python
- Obyektga yo‘naltirilgan dasturlash (OOP)
- JSON
- Fayllar bilan ishlash (File I/O)
- Buyruqlar qatori interfeysi (CLI)

## 🎯 Loyiha maqsadi

Python yordamida transport vositalarini ijaraga berish tizimini yaratish orqali obyektga yo‘naltirilgan dasturlash, meros olish, metodlarni qayta aniqlash, fayllar bilan ishlash va ma’lumotlarni saqlash ko‘nikmalarini rivojlantirish.