import pytesseract
import requests
import gradio as gr
import pytesseract
from pdf2image import convert_from_path
import pandas as pd
import json

# Путь к Tesseract, если Windows
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\minee\OneDrive\Desktop\SPOP\Tesseract-OCR\tesseract.exe'
API_URL = "http://localhost:1234/v1/chat/completions"


def process_pdf(pdf_path):
    # Шаг 1: Конвертируем PDF в изображения (страницы)
    images = convert_from_path(pdf_path)

    # Шаг 2: OCR для каждой страницы
    text = ""
    for img in images:
        page_text = pytesseract.image_to_string(img, lang='rus')  # для русских документов
        text += page_text + "\n"

    # Шаг 3: Отправляем текст в LM Studio
    payload = {
        "model": "phi-3.1-mini-128k-instruct",
        "messages": [
            {
                "role": "system",
                "content": """Ты юридический ассистент. Получаешь OCR-текст судебного документа и возвращаешь JSON со следующими полями, если они найдены:

    {
      "наименование суда": "",
      "взыскатель": "",
      "юридический адрес взыскателя": "",
      "телефон взыскателя": "",
      "ИНН взыскателя": "",
      "адрес взыскателя для корреспонденции": "",
      "должник": "",
      "адрес должника": "",
      "дата рождения должника": "",
      "место рождения должника": "",
      "паспорт серия должника": "",
      "паспорт номер должника": "",
      "паспорт дата выдачи": "",
      "паспорт орган выдачи": "",
      "ИНН должника": "",
      "СНИЛС должника": "",
      "сущность взыскания": "",
      "адрес взыскания": "",
      "пропорциональный порядок взыскания": "",
      "доли взыскания": "",
      "солидарный порядок взыскания": "",
      "наименование услуги": "",
      "долг": "",
      "сумма долга": "",
      "начало периода долга": "",
      "конец периода долга": "",
      "пени": "",
      "сумма пени": "",
      "начало периода пени": "",
      "конец периода пени": "",
      "процент": "",
      "сумма по процентам": "",
      "начало периода по процентам": "",
      "конец периода по процентам": "",
      "штраф": "",
      "сумма штрафа": "",
      "начало периода штрафа": "",
      "конец периода штрафа": "",
      "иное взыскание": "",
      "сумма иного взыскания": "",
      "начало периода иного взыскания": "",
      "конец периода иного взыскания": "",
      "общая сумма взыскания": "",
      "госпошлина": "",
      "приложение": ""
    }

    Если какое-то значение отсутствует, верни пустую строку для него.
    Ответ строго в JSON-формате."""
            },
            {
                "role": "user",
                "content": text  # вставляется распознанный текст из PDF
            }
        ],
        "temperature": 0.1
    }

    response = requests.post(API_URL, json=payload)
    result = response.json()['choices'][0]['message']['content']

    return result


# --- Интерфейс ---

def export_csv(text):
    json_output = json.loads(text)
    df = pd.DataFrame(json_output.items(), columns=["Поле", "Значение"])
    df.to_csv("result.csv", index=False)
    return "result.csv"


def export_excel(text):
    json_output = json.loads(text)
    df = pd.DataFrame(json_output.items(), columns=["Поле", "Значение"])
    df.to_excel("result.xlsx", index=False)
    return "result.xlsx"


with gr.Blocks() as demo:
    with gr.Row():
        pdf_input = gr.File(label="Загрузите PDF")

    output_data = gr.Textbox(label="Извлечённые данные")

    with gr.Row():
        export_csv_btn = gr.Button("Скачать CSV")
        export_excel_btn = gr.Button("Скачать Excel")

    pdf_input.change(fn=process_pdf, inputs=pdf_input, outputs=output_data)

    # Экспорт
    export_csv_btn.click(fn=export_csv, inputs=[output_data], outputs=gr.File())
    export_excel_btn.click(fn=export_excel, inputs=[output_data], outputs=gr.File())

demo.launch()
