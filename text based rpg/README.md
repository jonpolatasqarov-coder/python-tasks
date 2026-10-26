# Text-Based RPG Game Engine

Python dasturlash tilida yaratilgan matnli RPG o‘yini. Loyiha Object-Oriented Programming (OOP), State Pattern, Composition, dushman AI tizimi, topshiriqlar va o‘yin jarayonini saqlash mexanizmlarini amalda qo‘llash uchun ishlab chiqilgan.

## Asosiy imkoniyatlar

- **OOP:** Class, Inheritance va Composition konseptlaridan foydalanish.
- **Player tizimi:** Sog‘liq (HP), kuch (Strength), himoya (Defense) va Inventory.
- **Jang tizimi:** `attack()`, `defend()` va `use_item()` metodlari orqali jang qilish.
- **State Pattern:** O‘yinchining holatlarini `HealthyState`, `PoisonedState` va `DeadState` orqali boshqarish.
- **Quest tizimi:** Buyum topish, dushmanni mag‘lub etish va hududni o‘rganish topshiriqlari.
- **Enemy AI:** Dushmanning hujum qilishi yoki jangdan chekinishi.
- **Inventory:** Health Potion va Ancient Key kabi buyumlarni yig‘ish va ishlatish.
- **Logging:** O‘yin harakatlarini vaqt va o‘yinchi ismi bilan `log.txt` fayliga yozish.
- **Save/Load:** O‘yin jarayonini JSON formatida saqlash va qayta yuklash.
- **Defend Cooldown:** Himoyalanish harakatini takrorlashdan oldin kutish mexanizmi.

## Ishlatilgan texnologiyalar

- Python 3
- Object-Oriented Programming (OOP)
- JSON
- File Handling
- Exception Handling
- State Pattern
- Basic Enemy AI

## Kerakli kutubxonalar

Loyiha Python’ning ichki (standard) kutubxonalaridan foydalanadi. Ularni `pip` orqali alohida o‘rnatish talab qilinmaydi.

| Kutubxona | Vazifasi |
|---|---|
| `datetime` | Sana va vaqtni qayd etish |
| `json` | O‘yin ma’lumotlarini JSON formatida saqlash va yuklash |
| `os` | Fayl va papkalar bilan ishlash |
| `random` | Tasodifiy tanlovlar va AI harakatlari |
| `re` | Fayl nomlarini tekshirish va xavfsiz formatlash |

*Eslatma: `random` va `re` tegishli kodda ishlatilgan bo‘lsa, ushbu ro‘yxatda qoldiriladi. `pickle` ishlatilmasa, uni o‘rnatish yoki import qilish shart emas.*

## Loyiha tuzilishi

```text
text based rpg/
├── main.py
├── game.py
├── character.py
├── player.py
├── enemy.py
├── item.py
├── quest.py
├── world.py
├── states.py
├── save_system.py
├── log.txt
└── README.md
```

- `main.py` — asosiy menyu va o‘yin boshqaruvi.
- `game.py` — o‘yin jarayoni, janglar, topshiriqlar va loglar.
- `character.py` — umumiy Character klassi.
- `player.py` — o‘yinchi statistikasi, inventari va holatlari.
- `enemy.py` — dushman va uning AI harakatlari.
- `item.py` — buyumlar va ulardan foydalanish.
- `quest.py` — topshiriqlarni boshqarish.
- `world.py` — o‘yin dunyosi va uning obyektlari.
- `states.py` — o‘yinchi holatlari.
- `save_system.py` — o‘yinni saqlash va yuklash.
- `log.txt` — o‘yin harakatlari jurnali.

## O‘rnatish va ishga tushirish

### Talablar

- Python 3 o‘rnatilgan bo‘lishi kerak.
- Terminal yoki Command Prompt kerak bo‘ladi.

### Ishga tushirish

1. Loyihani kompyuteringizga yuklab oling.
2. Terminal orqali loyiha papkasiga kiring.
3. Quyidagi buyruqni bajaring:

```bash
py main.py
```

## O‘yin menyusi

### Asosiy menyu

- **1. New Game** — yangi o‘yin boshlash.
- **2. Load Game** — saqlangan o‘yinni yuklash.
- **0. Exit** — o‘yindan chiqish.

### O‘yin ichidagi menyu

- **1. Start Battle** — dushman bilan jang boshlash.
- **2. Explore** — hududni o‘rganish va topshiriqlarni bajarish.
- **3. Show Status** — o‘yinchi va dushman statistikalarini ko‘rish.
- **4. Show World** — dunyo, dushmanlar, buyumlar va topshiriqlarni ko‘rish.
- **5. Save Game** — o‘yin jarayonini saqlash.
- **0. Main Menu** — asosiy menyuga qaytish.

### Jangdagi harakatlar

- **Attack** — dushmanga hujum qilish.
- **Defend** — himoyani vaqtincha oshirish.
- **Use Potion** — Health Potion yordamida HP tiklash.
- **0. Back** — jang menyusidan chiqish.

## OOP konseptlari

### Class

Loyihada `Player`, `Enemy`, `Item`, `Quest` va `World` kabi klasslar mavjud.

### Inheritance

`Player` va `Enemy` umumiy `Character` klassidan meros oladi. Bu umumiy xususiyatlar va metodlardan qayta foydalanish imkonini beradi.

### Composition

O‘yin dunyosi o‘yinchilar, dushmanlar, buyumlar va topshiriqlarni birlashtiradi. Bu obyektlarning o‘zaro ishlashini tashkil qiladi.

### State Pattern

O‘yinchining holatiga qarab tegishli xatti-harakatni bajarish uchun alohida state klasslaridan foydalaniladi.

## Player State tizimi

- **HealthyState:** O‘yinchining HP ko‘rsatkichi maksimal HP ning 50% dan yuqori bo‘lganda.
- **PoisonedState:** HP maksimal qiymatning 50% yoki undan pastiga tushganda faollashadi. State effekti qo‘llanganda o‘yinchi 5 HP yo‘qotadi.
- **DeadState:** HP 0 ga tushganda faollashadi. O‘yinchi jangni davom ettira olmaydi.

## Quest tizimi

O‘yinda quyidagi turdagi topshiriqlar mavjud:

1. **Find Item** — kerakli buyumni topish.
2. **Kill Monster** — dushmanni mag‘lub etish.
3. **Explore Zone** — belgilangan hududni o‘rganish.

Topshiriqlar ketma-ket bajariladi. Barcha topshiriqlar bajarilganda o‘yin g‘alaba bilan yakunlanadi.

## Enemy AI

Dushman oddiy strategik algoritm asosida harakat qiladi. Vaziyatga qarab hujum qilishi yoki jangdan chekinishi mumkin. Chekingan dushman keyingi jangda qaytishi va kuchliroq bo‘lishi mumkin.

## Logging tizimi

O‘yin davomida qayd etiladigan harakatlar `log.txt` fayliga yoziladi. Har bir yozuvda quyidagilar ko‘rsatiladi:

- Sana va vaqt.
- O‘yinchi ismi.
- Bajarilgan harakat yoki o‘yin hodisasi.

Log fayli yangi o‘yin boshlanganda avtomatik ravishda tozalanmaydi, shuning uchun avvalgi yozuvlar ham saqlanib qoladi.

## Save/Load tizimi

O‘yin ma’lumotlari JSON formatida saqlanadi va keyinchalik qayta yuklanishi mumkin. Saqlash tizimi quyidagi ma’lumotlarni saqlash uchun mo‘ljallangan:

- O‘yinchi statistikasi va inventari.
- Dushman statistikasi va holati.
- Topshiriqlarning bajarilish holati.
- O‘yin dunyosi va buyumlar.
- O‘yin jarayonining holati.

## Loyihaning maqsadi

Ushbu loyiha orqali quyidagi dasturlash ko‘nikmalari amalda qo‘llanadi:

- Class va Inheritance.
- Composition.
- State Pattern.
- Turn-based combat.
- Oddiy Enemy AI.
- JSON orqali ma’lumotlarni saqlash va yuklash.
- Fayllar bilan ishlash.
- Logging va xatolarni qayta ishlash.