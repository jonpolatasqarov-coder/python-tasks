# 🏨 Hotel Booking System (OOP + Calendar)

Python dasturlash tilida ishlab chiqilgan mehmonxona bron qilish tizimi. Loyiha OOP konseptlari, kalendar asosida bronlarni boshqarish, VIP chegirmalar, refund hisoblash, daromad hisobotlari va log yozuvlarini o‘z ichiga oladi.

## 📌 Loyihaning vazifalari

1. `Room`, `Customer`, `Booking` va `Hotel` classlarini yaratish.
2. Xonalar turi, narxi, band kunlari va qulayliklarini boshqarish.
3. `datetime` yordamida bron sanalarini tekshirish.
4. Decorator yordamida VIP mijozlarga chegirma berish.
5. Bron bekor qilinganda qaytariladigan summani hisoblash.
6. Kunlik va oylik daromad hisobotlarini yaratish.
7. Xonalarni narxi, qulayliklari va joylashuvi bo‘yicha qidirish.
8. Bronlar haqidagi loglarni faylga yozish va ularni ko‘rish.

## ✨ Asosiy imkoniyatlar

- **Xonalarni boshqarish:** xona raqami, turi, narxi, joylashuvi, qulayliklari va mavjudligini ko‘rish.
- **Mijozlarni boshqarish:** mijoz ma’lumotlarini saqlash va ularga ID biriktirish.
- **Xonani bron qilish:** kirish va chiqish sanalarini belgilash.
- **Bandlikni tekshirish:** mavjud bronlar asosida xona bandligini aniqlash.
- **VIP chegirmasi:** decorator yordamida VIP mijozlar uchun chegirma hisoblash.
- **Bronni bekor qilish:** foydalanilmagan tunlar uchun refund hisoblash.
- **Bronni yakunlash:** muddati tugagan bronlarni yakunlash.
- **Xonalarni qidirish:** narx, qulaylik va joylashuv bo‘yicha filterlash.
- **Band kunlar taqvimi:** xonalarning o‘tgan va kelajakdagi band sanalarini ko‘rish.
- **Daromad hisoboti:** kunlik va oylik tushumlarni hisoblash.
- **Loglar:** bron yaratilishi va bekor qilinishini `hotel.log` faylida qayd etish.
- **Ma’lumotlarni saqlash:** JSON fayllari orqali ma’lumotlarni dastur qayta ishga tushganda ham saqlash.
- **Kiritilgan ma’lumotlarni tekshirish:** noto‘g‘ri qiymatlarni aniqlash.

## 🧠 OOP konseptlari

| Konsept | Loyihadagi qo‘llanilishi |
|---|---|
| Class va Object | `Room`, `Customer`, `Booking`, `Hotel` |
| Composition | `Booking` obyektida mijoz, xona va bron sanalaridan foydalanish |
| Encapsulation | Ma’lumotlar va ularga tegishli methodlarni classlarda tashkil qilish |
| Decorator | VIP chegirmasini hisoblash |
| Polymorphism | Loyihada amalda qo‘llangan bo‘lsa, tegishli methodlar orqali turli obyektlar bilan ishlash |

## 📂 Loyiha tuzilishi

```text
hotel-booking-system/
│
├── main.py
├── room.py
├── customer.py
├── booking.py
├── hotel.py
├── decorators.py
│
├── rooms.json
├── customers.json
├── bookings.json
├── hotel.log
│
└── README.md
```

### Python fayllari

- `main.py` — asosiy menyu va foydalanuvchi bilan muloqot.
- `room.py` — xona ma’lumotlari va xona bilan bog‘liq methodlar.
- `customer.py` — mijoz ma’lumotlari va VIP holati.
- `booking.py` — bron sanalari, davomiyligi va narx hisob-kitoblari.
- `hotel.py` — bronlarni boshqarish, qidiruv, refund va daromad hisobotlari.
- `decorators.py` — VIP chegirmasi uchun decorator.

### Ma’lumot fayllari

- `rooms.json` — xonalar ma’lumotlari.
- `customers.json` — mijozlar ma’lumotlari.
- `bookings.json` — bronlar va ularning holatlari.
- `hotel.log` — tizim faoliyati yozuvlari.

## 🛠️ Ishlatilgan texnologiyalar

- Python 3
- `datetime` va `timedelta`
- `json`
- `logging`
- Custom decorators
- Fayllar bilan ishlash

## 📋 Talablar (Requirements)

- Python 3 o‘rnatilgan bo‘lishi kerak.
- Windows, Linux yoki macOS operatsion tizimlarida ishlatish mumkin.
- Python standart kutubxonalari ishlatiladi.
- Oddiy terminal interfeysi uchun qo‘shimcha paket o‘rnatish talab qilinmaydi.

## ⚙️ O‘rnatish va ishga tushirish

### 1. Loyihani yuklab olish

```bash
git clone <repository-url>
```

### 2. Loyiha papkasiga kirish

```bash
cd hotel-booking-system
```

### 3. Dasturni ishga tushirish

```bash
py main.py
```

Agar `py` buyrug‘i mavjud bo‘lmasa, `python main.py` buyrug‘idan foydalanish mumkin.

## 🖥️ Asosiy menyu

```text
1. Show Rooms
2. Reception
3. Book Room
4. Cancel Booking
5. Search Rooms
6. Show Booked Days
7. Revenue Report
8. View Logs
9. Complete Booking
0. Exit
```

## 🎯 Loyiha maqsadi

Ushbu loyiha mehmonxona bron qilish jarayonini modellashtirish orqali Python dasturlash tilidagi OOP, sanalar bilan ishlash, JSON orqali ma’lumotlarni saqlash, decoratorlar, refund hisoblash, daromad hisobotlari va logging bo‘yicha amaliy ko‘nikmalarni mustahkamlash uchun ishlab chiqilgan.

---

**Loyiha nomi:** Hotel Booking System  
**Dasturlash tili:** Python 3  
**Asosiy yo‘nalishlar:** OOP, Calendar, JSON, Booking Management