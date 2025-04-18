
Веб-приложение на Python для извлечения текста из PDF

-- Описание --

Этот проект — веб-приложение на Python с использованием Gradio, которое позволяет загружать PDF-файлы (например, судебные документы), извлекать из них текст с помощью OCR (Tesseract), а затем анализировать этот текст с помощью локальной языковой модели (LM Studio). В результате приложение возвращает структурированный JSON с ключевыми юридическими данными.


----

-- Как это работает --

1. Загрузка PDF
Пользователь загружает PDF-файл через веб-интерфейс.


2. Распознавание текста (OCR)
PDF конвертируется в изображения (по страницам), затем pytesseract распознаёт текст на русском языке.


3. Обработка текста языковой моделью
Извлечённый текст отправляется в локальный сервер LM Studio по адресу http://localhost:1234/v1/chat/completions. Модель (phi-3.1-mini-128k-instruct) получает промпт в роли юридического ассистента и возвращает JSON с запрошенными полями (суд, взыскатель, должник, суммы и периоды и т.д.).


4. Отображение результата
Ответ в формате JSON отображается на экране и может быть экспортирован в CSV или Excel файл.




----

-- Зависимости --

Python 3.8+

pytesseract

requests

gradio

pdf2image

pandas

openpyxl (для Excel экспорта)

poppler (для работы pdf2image)


----


-- Примечание --

Обязательно установите Tesseract OCR и укажите путь в pytesseract.pytesseract.tesseract_cmd.

Убедитесь, что LM Studio запущен и слушает на localhost:1234.

