import streamlit as st
import requests

API_BASE_URL = "http://localhost:8000/parse"

st.title("🔍 Парсеры")

# Кнопка для запуска всех парсеров
if st.button("Запустить все парсеры"):
    with st.spinner("Парсинг..."):
        response = requests.get(f"{API_BASE_URL}/")
        if response.ok:
            st.success("Все парсеры запущены!")
            st.json(response.json())
        else:
            st.error(f"Ошибка: {response.status_code} - {response.text}")

# Раздел для запуска конкретного парсера
st.subheader("🚀 Запустить один парсер")

parser_name = st.text_input("Имя парсера")

if st.button("Запустить выбранный парсер"):
    if parser_name.strip():
        with st.spinner("Парсинг..."):
            response = requests.post(API_BASE_URL + "/", json={"parser": parser_name})
            if response.ok:
                st.success("Парсер успешно запущен!")
                st.json(response.json())
            else:
                st.error(f"Ошибка: {response.status_code} - {response.text}")
    else:
        st.warning("Введите имя парсера.")
