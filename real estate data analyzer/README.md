# 🏠 Real Estate Data Analyzer

Python dasturlash tilida yaratilgan, ko‘chmas mulk ma’lumotlarini tahlil qilish, filtrlash va vizualizatsiya qilish tizimi.

## 🧠 OOP Konseptlari

- Class va Object
- Class Inheritance
- Method Overriding
- Encapsulation
- Strategy Pattern
- File I/O

## 📋 Vazifalar

1. CSV formatidagi ko‘chmas mulk ma’lumotlarini `Property`, `Apartment` va `House` klasslari orqali modellashtirish.
2. Har bir ko‘chmas mulk uchun `calculate_price_per_m2()` metodini yaratish.
3. Pandas yordamida o‘rtacha narx, eng qimmat hudud va sotilgan obyektlar sonini aniqlash.
4. `FilterStrategy` orqali narx, maydon, hudud va xonalar soni bo‘yicha filtrlashni amalga oshirish.
5. Matplotlib va Seaborn yordamida ma’lumotlarni vizualizatsiya qilish.
6. Har bir filtrlash natijasini `.xlsx` fayliga eksport qilish.
7. CLI orqali ma’lumotlarni tahlil qilish, filtrlash va eksport qilishni boshqarish.
8. Bonus: Linear Regression yordamida ko‘chmas mulk narxini bashorat qiluvchi `price_predictor()` funksiyasini yaratish.

## ✨ Asosiy imkoniyatlar

- **Ko‘chmas mulkni modellashtirish:** `Property`, `Apartment` va `House` klasslari orqali obyektlarni boshqarish.
- **Narxni hisoblash:** har bir obyekt uchun bir kvadrat metr narxini aniqlash.
- **Statistik tahlil:** Pandas yordamida narxlar va hududlar bo‘yicha statistik ma’lumotlarni olish.
- **Ko‘chmas mulkni filtrlash:** narx, maydon, hudud va xonalar soni bo‘yicha qidirish.
- **Bir nechta filtrdan foydalanish:** Strategy Pattern yordamida turli filtrlash shartlarini birlashtirish.
- **Grafiklar yaratish:** hududlar bo‘yicha o‘rtacha narxlar, obyektlar soni va narx bilan maydon o‘rtasidagi bog‘liqlikni ko‘rsatish.
- **Excel eksport:** filtrlash natijalarini `.xlsx` formatida saqlash.
- **Narxni bashorat qilish:** Linear Regression yordamida ko‘chmas mulkning taxminiy narxini hisoblash.
- **CLI boshqaruvi:** dastur funksiyalarini terminal orqali tanlash va bajarish.

## 📁 Ma’lumotlar fayli

- `properties.csv` — ko‘chmas mulk obyektlari haqidagi ma’lumotlar.

CSV faylida quyidagi ustunlar mavjud:

| Ustun | Tavsifi |
|---|---|
| `id` | Obyekt identifikatori |
| `type` | Ko‘chmas mulk turi |
| `district` | Joylashgan hudud |
| `area` | Maydon, m² |
| `rooms` | Xonalar soni |
| `price` | Umumiy narx |
| `status` | Obyektning holati |

## 📦 Talablar

- Python 3.10 yoki undan yangi versiya tavsiya etiladi.
- Kerakli kutubxonalarni o‘rnatish talab qilinadi.

### Foydalanilgan kutubxonalar

- `pandas` — ma’lumotlarni qayta ishlash va tahlil qilish.
- `matplotlib` — grafiklar yaratish.
- `seaborn` — statistik grafiklarni vizualizatsiya qilish.
- `openpyxl` — Excel fayllarini yaratish va saqlash.
- `scikit-learn` — Linear Regression modelini yaratish va baholash.

## ⚙️ O‘rnatish va ishga tushirish

### 1. Kerakli kutubxonalarni o‘rnatish

```bash
py -m pip install pandas matplotlib seaborn openpyxl scikit-learn
```

### 2. Dasturni ishga tushirish

Terminalda loyiha papkasini oching va quyidagi buyruqni bajaring:

```bash
py main.py
```

## 🛠️ Foydalanilgan texnologiyalar

- Python
- Obyektga yo‘naltirilgan dasturlash (OOP)
- Pandas
- Strategy Pattern
- Matplotlib
- Seaborn
- Scikit-learn
- CSV va Excel
- Buyruqlar qatori interfeysi (CLI)

## 🎯 Loyiha maqsadi

Python yordamida ko‘chmas mulk ma’lumotlarini tahlil qilish tizimini yaratish orqali OOP, meros olish, Strategy Pattern, ma’lumotlarni qayta ishlash, vizualizatsiya va mashinaviy o‘rganish bo‘yicha amaliy ko‘nikmalarni rivojlantirish.
