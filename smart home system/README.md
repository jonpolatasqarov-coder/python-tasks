# Smart Home System

## Loyiha haqida

**Smart Home System** — Python dasturlash tilida OOP (Object-Oriented Programming) tamoyillari asosida ishlab chiqilgan aqlli uy boshqaruv tizimi.

Ushbu tizim orqali uy qurilmalarini boshqarish, ularning holatini kuzatish, haroratni nazorat qilish, energiya sarfini hisoblash va harorat o‘zgarishlarini grafik ko‘rinishida ko‘rish mumkin.

## OOP konseptlari

Loyihada quyidagi OOP konseptlaridan foydalaniladi:

- **Inheritance (Meros olish):** qurilmalar `Device` abstract classidan meros oladi.
- **Abstraction (Abstraksiya):** `Device` barcha qurilmalar uchun umumiy interfeysni belgilaydi.
- **Polymorphism (Polimorfizm):** har bir qurilma `turn_on()`, `turn_off()` va `status_report()` metodlarini o‘ziga mos ravishda bajaradi.
- **Composition (Kompozitsiya):** `SmartHomeController` qurilmalar obyektlarini boshqaradi.
- **Observer Pattern:** harorat o‘zgarishini kuzatib, ventilyatorni avtomatik boshqaradi.

## Loyiha vazifalari

1. `Device` nomli abstract class yaratish.
2. `Light`, `Thermostat`, `Camera`, `Alarm` va `Fan` classlarini ishlab chiqish.
3. Har bir qurilma uchun `turn_on()`, `turn_off()` va `status_report()` metodlarini yaratish.
4. Barcha qurilmalarni `SmartHomeController` orqali boshqarish.
5. Harorat 30°C dan oshganda ventilyatorni avtomatik yoqish.
6. Harorat 30°C yoki undan pastga tushganda ventilyatorni avtomatik o‘chirish.
7. Qurilmalar holatini JSON faylida saqlash va dastur qayta ishga tushirilganda tiklash.
8. Qurilmalarni boshqarish uchun CLI menyusini yaratish.
9. Qurilmalarning ishlash vaqti va quvvatiga qarab energiya sarfini hisoblash.
10. Harorat tarixini Matplotlib yordamida grafikda ko‘rsatish.
11. Noto‘g‘ri kiritmalar va JSON faylidagi xatolarni qayta ishlash.

## Asosiy imkoniyatlar

- Qurilmalarni alohida yoqish va o‘chirish.
- Barcha qurilmalarni bir vaqtda yoqish yoki o‘chirish.
- Termostat orqali haroratni o‘zgartirish.
- Haroratga qarab ventilyatorni avtomatik boshqarish.
- Qurilmalarning holati va ishlash vaqtini ko‘rish.
- Har bir qurilma va barcha qurilmalar uchun energiya sarfini hisoblash.
- Harorat o‘zgarishlarini grafik ko‘rinishida kuzatish.
- Qurilmalar holatini JSON faylida saqlash va qayta tiklash.
- Noto‘g‘ri ma’lumotlar bilan ishlashda xatolarni boshqarish.

## Loyiha tuzilishi

```text
smart home system/
│
├── main.py
├── controller.py
├── device.py
├── light.py
├── thermostat.py
├── camera.py
├── alarm.py
├── fan.py
├── observer.py
├── energy.py
├── temperature.py
├── devices.json
└── README.md
```

## Fayllarning vazifalari

| Fayl | Vazifasi |
|---|---|
| `main.py` | Dasturning asosiy qismi va menyusi |
| `controller.py` | Qurilmalarni boshqarish va JSON bilan ishlash |
| `device.py` | Umumiy `Device` abstract classi |
| `light.py` | Chiroq qurilmasi |
| `thermostat.py` | Haroratni boshqarish |
| `camera.py` | Xavfsizlik kamerasi |
| `alarm.py` | Signalizatsiya qurilmasi |
| `fan.py` | Ventilyator qurilmasi |
| `observer.py` | Haroratni kuzatish va ventilyatorni avtomatik boshqarish |
| `energy.py` | Energiya sarfini hisoblash |
| `temperature.py` | Harorat grafigini yaratish |
| `devices.json` | Qurilmalar haqidagi ma’lumotlarni saqlash |
| `README.md` | Loyiha hujjatlari |

## Ma’lumotlarni saqlash

Qurilmalar haqidagi ma’lumotlar `devices.json` faylida saqlanadi.

Saqlanadigan ma’lumotlar quyidagilarni o‘z ichiga olishi mumkin:

- Qurilma nomi va turi.
- Qurilmaning yoqilgan yoki o‘chirilgan holati.
- To‘plangan ishlash vaqti.
- Qurilma yoqilgan vaqt belgisi.
- Termostatning joriy harorati.
- Harorat o‘zgarishlari tarixi.

Dastur qayta ishga tushirilganda saqlangan ma’lumotlar yuklanadi va qurilmalarning holati tiklanadi.

## Energiya sarfini hisoblash

Energiya sarfi qurilmaning quvvati va ishlash vaqtiga qarab hisoblanadi.

**Formula:**

```text
Energiya (Wh) = Quvvat (W) × Ishlash vaqti (soat)
```

**Misol:**

Agar quvvati 100 W bo‘lgan qurilma 2 soat ishlasa:

```text
Energiya = 100 × 2 = 200 Wh
```

Bu natija qurilmaning belgilangan quvvati va dastur qayd etgan ishlash vaqtiga asoslangan taxminiy hisobdir.

## Harorat grafigi

`temperature.py` faylida Matplotlib kutubxonasi yordamida harorat tarixini grafik ko‘rinishida chiqarish funksiyasi mavjud.

Grafikda:

- Gorizontal o‘qda o‘lchov raqamlari.
- Vertikal o‘qda harorat qiymatlari (°C).
- Harorat o‘zgarishini ko‘rsatuvchi nuqtalar va chiziqlar.
- Ma’lumotlarni o‘qishni osonlashtiruvchi koordinata to‘ri ko‘rsatiladi.

## Talablar

Loyihani ishga tushirish uchun quyidagilar kerak:

- **Python 3.10 yoki undan yuqori versiya**
- **Matplotlib** kutubxonasi

`json`, `time`, `abc` va `pathlib` modullari Python’ning standart kutubxonasiga kiradi. Ularni alohida o‘rnatish shart emas.

## O‘rnatish va ishga tushirish

### 1. Loyihani yuklab olish

```bash
git clone <repository-url>
```

`<repository-url>` o‘rniga GitHub repository manzilini yozing.

### 2. Loyiha papkasiga kirish

```bash
cd "smart home system"
```

### 3. Kerakli kutubxonani o‘rnatish

```bash
py -m pip install matplotlib
```

### 4. Dasturni ishga tushirish

```bash
py main.py
```

## Boshqaruv menyusi

Dasturning asosiy menyusi quyidagi imkoniyatlarni taqdim etadi:

1. **Qurilmalar holati** — barcha qurilmalarning joriy holatini ko‘rish.
2. **Qurilmalarni boshqarish** — qurilmalarni yoqish, o‘chirish va termostat haroratini o‘zgartirish.
3. **Energiya hisoboti** — qurilmalarning energiya sarfini ko‘rish.
4. **Harorat tarixi** — harorat o‘zgarishlari grafigini ko‘rish.
5. **Chiqish** — ma’lumotlarni saqlab, dasturni yakunlash.

## Loyiha maqsadi

Loyihaning asosiy maqsadi Python dasturlash tilidagi OOP konseptlarini amaliyotda qo‘llash, bir nechta qurilmalarni yagona tizim orqali boshqarish, Observer Pattern yordamida avtomatik jarayonlarni tashkil qilish, JSON orqali ma’lumotlarni saqlash, energiya sarfini hisoblash va Matplotlib yordamida ma’lumotlarni grafik ko‘rinishida tasvirlashni o‘rganishdir.
