# 📚 Kutubxona Boshqaruv Tizimi (Library Management System)

**OOP konseptlari:** Meros olish (Inheritance), Inkapsulyatsiya (Encapsulation), Fayllar bilan ishlash (File I/O), TF-IDF, Cosine Similarity

## 📋 Loyiha vazifalari

1. `Book`, `User` va `Library` klasslarini yaratish.
2. Foydalanuvchilarga kitoblarni ijaraga olish, qaytarish va ijara muddatini uzaytirish imkoniyatini berish.
3. Kitoblar va foydalanuvchilar haqidagi ma’lumotlarni `books.json` va `users.json` fayllarida saqlash hamda dastur ishga tushganda qayta yuklash.
4. TF-IDF va Cosine Similarity algoritmlari yordamida mazmunan o‘xshash kitoblarni tavsiya qiluvchi `recommend_books()` metodini yaratish.
5. Kitobni qaytarish muddati o‘tganda foydalanuvchini ogohlantirish va email xabarini simulyatsiya qilish.
6. Buyruqlar qatori interfeysi (CLI) orqali kitoblarni qidirish, ro‘yxatini ko‘rish, ijaraga olish va qaytarish menyularini yaratish.
7. Kitoblar statistikasini yuritish, jumladan, eng ko‘p va eng kam ijaraga olingan kitoblarni aniqlash.
8. `Admin` klassi yordamida kitoblarni qo‘shish, boshqarish va foydalanuvchilarni nazorat qilish.
9. Admin paneliga parol orqali kirishni tekshirish.

## 🤖 Kitob tavsiyalari tizimi

Loyihada TF-IDF va Cosine Similarity algoritmlaridan foydalaniladi. Ushbu algoritmlar kitoblarning matnli tavsiflarini tahlil qilib, mazmunan bir-biriga o‘xshash kitoblarni aniqlashga yordam beradi.

`recommend_books()` metodi foydalanuvchiga qiziqishlariga mos kitoblarni tavsiya qilish uchun mo‘ljallangan.

## 💾 Ma’lumotlarni saqlash

Loyiha ma’lumotlarni JSON fayllari orqali saqlaydi:

- `books.json` — kitoblar haqidagi ma’lumotlar.
- `users.json` — foydalanuvchilar haqidagi ma’lumotlar.
- `admin.json` — admin autentifikatsiyasi uchun ma’lumotlar.

Bu usul dastur qayta ishga tushirilganda saqlangan ma’lumotlardan yana foydalanish imkonini beradi.

## 🔐 Admin paneli

Admin paneliga kirish parol orqali tekshiriladi.

- **Admin paroli:** `12345678`
- Yangi kitoblar qo‘shish va mavjud kitoblarni boshqarish.
- Foydalanuvchilarni nazorat qilish.
- Kutubxona ma’lumotlari bilan ishlash.

**Xavfsizlik eslatmasi:** Ushbu parol o‘quv loyihasi uchun ko‘rsatilgan. Haqiqiy loyihada parolni ochiq holda ommaga e’lon qilmaslik kerak.

## ✨ Asosiy imkoniyatlar

- Kitoblarni qidirish va ro‘yxatini ko‘rish.
- Kitoblarni ijaraga olish va qaytarish.
- Ijara muddatini uzaytirish.
- Mazmunan o‘xshash kitoblar tavsiyasini olish.
- Muddati o‘tgan kitoblar haqida ogohlantirish.
- Email xabarlarini simulyatsiya qilish.
- Eng ko‘p va eng kam ijaraga olingan kitoblar statistikasini ko‘rish.
- Admin paneli orqali kitoblar va foydalanuvchilarni boshqarish.
- Ma’lumotlarni JSON fayllarida saqlash va qayta yuklash.

## 📦 Talablar

Loyihani ishga tushirish uchun quyidagilar kerak:

- Python 3.
- `scikit-learn` tashqi kutubxonasi.

`json`, `datetime`, `hashlib` va `hmac` modullari Python standart kutubxonasiga kiradi. Ularni alohida o‘rnatish shart emas.

## ⚙️ O‘rnatish va ishga tushirish

**1.** Repository'ni yuklab oling yoki clone qiling.

**2.** Terminalni loyiha papkasida oching.

**3.** Kerakli kutubxonani o‘rnating:

```bash
py -m pip install scikit-learn
```

**4.** Dasturni ishga tushiring:

```bash
py main.py
```

## 🎯 Loyihaning maqsadi

Ushbu loyiha Python dasturlash tilida OOP tamoyillarini, JSON fayllari bilan ishlashni, foydalanuvchi ma’lumotlarini boshqarishni va mashinaviy o‘rganishda qo‘llaniladigan matnlarni tahlil qilish usullarini amaliy o‘rganish uchun yaratilgan.
