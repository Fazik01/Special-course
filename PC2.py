import streamlit as st
import requests
from PIL import Image

st.title("Классификация изображений")

uploaded_file = st.file_uploader("Загрузите изображение", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Загруженное изображение", use_column_width=True)

    if st.button("Распознать"):
        with st.spinner("Обработка..."):
            try:
                # Читаем содержимое загруженного файла
                file_content = uploaded_file.getvalue()

                # Отправляем запрос на API
                response = requests.post(
                    "http://127.0.0.1:8000/predict/",
                    files={"file": (uploaded_file.name, file_content, "image/jpeg")},
                )

                # Обработка ответа
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"Класс: {result['class']}")
                    st.info(f"Точность: {result['confidence']:.2f}")
                else:
                    st.error(f"Ошибка: {response.text}")
            except Exception as e:
                st.error(f"Не удалось подключиться к API: {e}")
