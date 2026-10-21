# ⚽ Turnir Boshqaruv Tizimi (Tournament System)

Python dasturlash tilida yaratilgan, futbol turnirlarini tashkil qilish, o‘yinlarni simulyatsiya qilish va natijalarni kuzatish tizimi.

## 🧠 OOP Konseptlari

- **Class Inheritance** — `Person` klassidan `Player` va `Referee` klasslarini yaratish.
- **Encapsulation** — o‘yinchilar, turnirlar va natijalar ma’lumotlarini klasslar orqali boshqarish.
- **Polymorphism** — turli turnir strategiyalarini alohida metodlar orqali amalga oshirish.
- **Strategy Pattern** — `RoundRobinStrategy` va `KnockoutStrategy` yordamida turnir formatlarini boshqarish.
- **State Pattern** — o‘yinchining sport formasini `GoodForm`, `NormalForm` va `BadForm` klasslari orqali ifodalash.
- **File I/O** — turnir natijalarini CSV va JSON fayllarida saqlash.

## 📋 Vazifalar

1. `Person`, `Player`, `Referee`, `Match`, `Tournament` va `Admin` klasslarini yaratish.
2. Ikki xil turnir formatini amalga oshirish:
   - `Round Robin` — har bir ishtirokchi boshqa barcha ishtirokchilar bilan o‘ynaydi.
   - `Knockout` — mag‘lub bo‘lgan ishtirokchi turnirdan chiqib ketadi.
3. O‘yin natijalarini tasodifiy gol simulyatsiyasi orqali hisoblash.
4. G‘alaba, durang va mag‘lubiyat asosida ochkolarni hisoblash.
5. Gollar soni, o‘tkazib yuborilgan gollar, gol farqi va quruq o‘yinlar statistikasini yuritish.
6. O‘yinchining sport formasini natijalarga qarab yangilash.
7. `Referee` klassi orqali o‘yinlarni boshqarish va hakam boshqargan o‘yinlar sonini hisoblash.
8. `Admin` orqali o‘yinchilarni ro‘yxatdan o‘tkazish va turnir jarayonini boshqarish.
9. Turnir jadvalini va Knockout raundlari natijalarini ko‘rsatish.
10. Turnir yakunida chempion, eng yaxshi to‘purar, eng yaxshi o‘yinchi va eng ko‘p quruq o‘yin o‘tkazgan ishtirokchilarni aniqlash.
11. O‘yin natijalarini CSV fayllarida, turnir statistikalarini esa JSON fayllarida saqlash.

## ✨ Asosiy imkoniyatlar

- **O‘yinchilarni boshqarish:** 16 tagacha o‘yinchini ro‘yxatdan o‘tkazish.
- **Turnir formatini tanlash:** Round Robin yoki Knockout.
- **O‘yinlarni simulyatsiya qilish:** o‘yinchilar formasiga bog‘liq ehtimollar asosida gol hisoblash.
- **Turnir jadvali:** ochkolar, g‘alabalar, duranglar, mag‘lubiyatlar va gol statistikasi.
- **Sport formasi:** yaxshi, normal va yomon formani natijalarga qarab yangilash.
- **Knockout raundlari:** g‘oliblarni keyingi raundga o‘tkazish va duranglarni hal qilish.
- **Mukofotlar:** chempion, eng yaxshi to‘purar, eng yaxshi o‘yinchi va eng ko‘p quruq o‘yin natijalarini aniqlash.
- **Ma’lumotlarni saqlash:** o‘yin natijalari va turnir jadvallarini fayllarga yozish.
- **CLI interfeysi:** menyu orqali turnirni boshqarish.

## 📁 Natijalar saqlanadigan fayllar

- `round_robin_matches.csv` — Round Robin turniridagi o‘yinlar va natijalar.
- `knockout_matches.csv` — Knockout turniridagi o‘yinlar va natijalar.
- `standings.json` — Round Robin turnirining statistik jadvali.
- `knockout_standings.json` — Knockout turniri yakuniy statistikasi.

## 📦 Talablar

- Python 3.10 yoki undan yangi versiya tavsiya etiladi.
- Qo‘shimcha tashqi kutubxonalarni o‘rnatish talab qilinmaydi.

### Foydalanilgan standart modullar

- `random` — o‘yin natijalarini tasodifiy simulyatsiya qilish.
- `csv` — o‘yin natijalarini CSV formatida saqlash.
- `json` — turnir statistikalarini JSON formatida saqlash.
- `os` — fayllar mavjudligini va hajmini tekshirish.

## ⚙️ O‘rnatish va ishga tushirish

1. Repository’ni yuklab oling yoki clone qiling.
2. Terminalni loyiha papkasida oching.
3. Dasturni ishga tushiring:

   ```bash
   py main.py
   ```

## 🎮 Foydalanish

Dastur ishga tushgach, menyu orqali quyidagi amallarni bajarish mumkin:

1. O‘yinchilarni qo‘shish.
2. Turnir formatini tanlash va turnirni boshlash.
3. Turnir o‘yinlarini o‘tkazish.
4. Turnir jadvali va natijalarini ko‘rish.
5. Mukofotlarni ko‘rish.
6. Turnirni yakunlash va ma’lumotlarni saqlash.
7. Dasturdan chiqish.

## 🎯 Loyiha maqsadi

Obyektga yo‘naltirilgan dasturlash, klasslar o‘rtasidagi meros olish, Strategy va State dizayn patternlari, statistik hisob-kitoblar hamda fayllar bilan ishlash ko‘nikmalarini rivojlantirish.

