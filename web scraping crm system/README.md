# Web Scraping CRM System

## 📌 Loyiha haqida

**Web Scraping CRM System** — Python dasturlash tilida yaratilgan loyiha bo‘lib, veb-saytlardan ma’lumotlarni avtomatik yig‘ish, tozalash, saqlash va CRM tizimi orqali boshqarish uchun mo‘ljallangan.

Loyiha uchta asosiy yo‘nalishda ishlaydi:

- **News Scraper** — BBC RSS orqali yangiliklarni yig‘adi.
- **Product Scraper** — Open Library API orqali kitoblar haqidagi ma’lumotlarni oladi.
- **Social Scraper** — CareerMesh sahifasidan professional profillarni yig‘adi.

Yig‘ilgan ma’lumotlar JSON formatida saqlanadi va CSV formatiga eksport qilinishi mumkin. CRM qismi esa lead’larni boshqarish, ularning statuslarini yangilash, izohlar qo‘shish va tarixini ko‘rish imkonini beradi.

## 🚀 Asosiy imkoniyatlar

- 🌐 **Web Scraping:** turli manbalardan ma’lumotlarni avtomatik yig‘ish.
- 🧱 **Object-Oriented Programming (OOP):** umumiy `Scraper` class va uning vorislaridan foydalanish.
- 🧹 **Data Cleaning:** matnlardagi ortiqcha bo‘sh joylarni tozalash.
- 🔁 **Retry Mechanism:** xatolar yuz berganda qayta urinish mexanizmi.
- 📝 **Logging:** jarayonlar va xatolarni `log.txt` fayliga yozish.
- 💾 **JSON Storage:** yig‘ilgan ma’lumotlarni JSON formatida saqlash.
- 📊 **CSV Export:** ma’lumotlarni CSV formatiga eksport qilish.
- 👥 **CRM Lead Management:** lead’larni qo‘shish va mavjud ma’lumotlarni yangilash.
- 🔎 **Duplicate Detection:** takroriy lead’larni aniqlash va ularning mavjud ma’lumotlarini saqlab qolish.
- 📜 **Lead History:** lead’lar bilan bog‘liq o‘zgarishlar tarixini ko‘rish.
- 🖥️ **CLI Menu:** barcha asosiy funksiyalarni terminal orqali boshqarish.
- ⚠️ **Error Handling:** xatolarni qayta ishlash va foydalanuvchiga xabar berish.

## 🛠️ Ishlatilgan texnologiyalar va kutubxonalar

- **Python** — asosiy dasturlash tili.
- **Requests** — HTTP so‘rovlarini yuborish.
- **BeautifulSoup4** — HTML sahifalarini tahlil qilish.
- **lxml** — HTML/XML ma’lumotlarini parse qilish.
- **Feedparser** — RSS yangiliklarini o‘qish.
- **JSON va CSV** — ma’lumotlarni saqlash va eksport qilish.

## 📂 Loyiha strukturasi

```text
web scraping crm system/
│
├── main.py
├── scraper.py
├── news_scraper.py
├── product_scraper.py
├── social_scraper.py
├── cleaner.py
├── lead_generator.py
├── lead_manager.py
├── storage.py
├── retry.py
├── logger.py
│
├── NewsScraper.json
├── ProductScraper.json
├── SocialScraper.json
├── leads.json
│
├── news.csv
├── products.csv
├── social.csv
├── leads.csv
│
└── log.txt
```

### Asosiy fayllar vazifasi

| Fayl | Vazifasi |
|---|---|
| `main.py` | Asosiy dastur va CLI menyusi |
| `scraper.py` | Umumiy `Scraper` class |
| `news_scraper.py` | Yangiliklarni yig‘ish |
| `product_scraper.py` | Kitoblar haqidagi ma’lumotlarni yig‘ish |
| `social_scraper.py` | Professional profillarni yig‘ish |
| `cleaner.py` | Matnlarni tozalash |
| `lead_generator.py` | Lead yaratish bilan bog‘liq funksiyalar |
| `lead_manager.py` | Lead’larni boshqarish, status, izoh va tarix |
| `storage.py` | JSON va CSV fayllari bilan ishlash |
| `retry.py` | Qayta urinish mexanizmi |
| `logger.py` | Log yozuvlarini saqlash |

## 📦 O‘rnatish

### 1. Repository’ni klonlash

```bash
git clone https://github.com/jonpolatasqarov-coder/python-tasks.git
```

### 2. Project papkasiga kirish

```bash
cd "python-tasks/web scraping crm system"
```

### 3. Kerakli kutubxonalarni o‘rnatish

```bash
py -m pip install requests beautifulsoup4 feedparser lxml
```

## ▶️ Loyihani ishga tushirish

Project papkasi ichida quyidagi buyruqni bajaring:

```bash
py main.py
```

Dastur terminalda menyuni ko‘rsatadi.

## 🖥️ CLI menyusi

| Raqam | Funksiya |
|---|---|
| `1` | Ma’lumotlarni yig‘ishni boshlash |
| `2` | Statistikani ko‘rish |
| `3` | Ma’lumotlarni CSV formatiga eksport qilish |
| `4` | Lead’larni ko‘rish |
| `5` | Lead statusini yangilash |
| `6` | Lead’ga izoh qo‘shish |
| `7` | Lead tarixini ko‘rish |
| `8` | Dasturdan chiqish |

## 📁 Ma’lumotlarni saqlash

Dastur ma’lumotlarni JSON fayllarida saqlaydi:

- `NewsScraper.json` — yangiliklar.
- `ProductScraper.json` — kitoblar.
- `SocialScraper.json` — professional profillar.
- `leads.json` — CRM lead’lari.

CSV eksport funksiyasi quyidagi fayllarni yaratadi yoki yangilaydi:

- `news.csv`
- `products.csv`
- `social.csv`
- `leads.csv`

Jarayon va xatolar haqidagi log yozuvlari `log.txt` faylida saqlanadi.

## 🎯 Loyiha maqsadi

Ushbu loyiha orqali Python’da quyidagi ko‘nikmalarni amaliy qo‘llash ko‘zda tutilgan:

- OOP va inheritance
- Abstract classes
- Web scraping va API bilan ishlash
- Ma’lumotlarni tozalash va saqlash
- Decorator va retry mexanizmi
- Error handling va logging
- JSON/CSV bilan ishlash
- CRM tizimi va lead management
- CLI orqali dastur boshqarish

