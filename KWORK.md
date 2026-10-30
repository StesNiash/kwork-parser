# KWORK

## Карточка 2. Парсер сайта → CSV / Excel

**Цена:** от 1 500 ₽  
**Срок:** 1–2 дня  
**Репозиторий:** `kwork-parser`

### Что входит

- разбор одного сайта или раздела по согласованным полям;
- до 5–7 полей: название, цена, ссылка, артикул и т.п.;
- пагинация по переданным URL;
- удаление дублей;
- выгрузка в CSV и XLSX;
- отчёт: сколько страниц обработано, сколько карточек найдено, сколько пропущено;
- инструкция запуска и ограничения.

### Что нужно от покупателя

- ссылки на страницы или сохранённые HTML-файлы;
- список нужных полей;
- подтверждение, что парсинг источника разрешён;
- пример желаемого CSV/XLSX.

### Что не входит

- обход CAPTCHA, авторизации, платных подписок и антибот-защит;
- парсинг сайтов, где это запрещено правилами;
- рендер JavaScript-приложений;
- круглосуточный мониторинг и расписание;
- Google Sheets, CRM и Telegram-уведомления;
- поддержка произвольного числа сайтов в одной цене.

### Дополнительно

- несколько сайтов или сложная структура — отдельная оценка;
- регулярный запуск — отдельная задача;
- выгрузка в Google Sheets — карточка 6 и отдельный репозиторий.

### FAQ

**Вы можете спарсить любой сайт?** Нет. Сначала проверяем правила сайта и доступность данных.

**Сайт на JavaScript?** Базовый парсер не исполняет JS; нужен отдельный браузерный сценарий.

**Данные придут в Excel?** Да, CSV и XLSX; для XLSX нужен `openpyxl` из `requirements.txt`.

## Обложка (не копировать в карточку)

> Это промпт для генератора изображений, а не текст объявления. В Kwork его публиковать не нужно.

**Промпт для ChatGPT / Gemini:**

> 4:3 editorial tech illustration for a website-to-spreadsheet parser service. On the left, a stack of clean website product cards with selector brackets and a magnifier; in the middle, a subtle funnel; on the right, a polished spreadsheet with rows and a small CSV/XLSX file icon. Deep blue background, cyan and warm orange accents, soft glow, thin grid lines, professional vector-3D hybrid, high contrast, generous negative space, centered composition that survives a square crop, no text, no letters, no logos, no watermarks, no real person, crisp details.

**Коротко по-русски:** карточки сайта → воронка → аккуратная таблица; синий, циан и оранжевый; без текста, логотипов и брендов.

**Параметры:** 1200×900, 4:3; таблица и карточки не обрезаны по краям.

**Негатив:** text, typography, letters, brand logo, watermark, signature, real person, messy cables, cluttered composition, low contrast, distorted UI.
