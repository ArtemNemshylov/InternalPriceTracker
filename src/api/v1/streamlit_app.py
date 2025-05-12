import streamlit as st
import requests
from datetime import datetime

API_BASE_URL = "http://localhost:8000/parse"

st.set_page_config(page_title="Парсери", page_icon="🕸️")
st.title("🔍 Парсери")

parser_names = []
with st.spinner("Завантаження парсерів..."):
    try:
        response = requests.get(f"{API_BASE_URL}/list")
        if response.ok:
            parser_names = response.json().get("parsers", [])
        else:
            st.error("❌ Не вдалося отримати список парсерів")
    except Exception as e:
        st.error(f"❌ Помилка запиту: {str(e)}")

# 👉 Запуск усіх парсерів
st.subheader("🧨 Запустити всі парсери")

if st.button("🔁 Запустити всі"):
    with st.spinner("Парсинг..."):
        response = requests.get(f"{API_BASE_URL}/")
        if response.ok:
            result = response.json()
            st.success("✅ Усі парсери завершилися")
            st.json(result)

            if "excel" in result:
                excel_path = result["excel"]
                excel_url = f"{API_BASE_URL}/download"

                excel_response = requests.get(excel_url)
                if excel_response.ok:
                    st.download_button(
                        label="📥 Завантажити Excel (всі парсери)",
                        data=excel_response.content,
                        file_name=excel_path.split("/")[-1],
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    st.warning("⚠️ Excel-файл не знайдено або ще не готовий.")
        else:
            st.error(f"❌ Помилка: {response.status_code} - {response.text}")

# 👉 Запуск одного парсера
st.subheader("🎯 Запустити конкретний парсер")

if parser_names:
    selected_parser = st.selectbox("Оберіть парсер", parser_names)

    if st.button("▶️ Запустити обраний"):
        with st.spinner("Парсинг..."):
            response = requests.post(f"{API_BASE_URL}/", json={"parser": selected_parser})
            if response.ok:
                result = response.json()
                st.success("✅ Парсер завершився")
                st.json(result)

                if "excel" in result:
                    filename = result["excel"].split("/")[-1]
                    download_url = f"{API_BASE_URL}/download/{selected_parser}"

                    download_response = requests.get(download_url)
                    if download_response.ok:
                        st.download_button(
                            label="📥 Завантажити Excel (цей парсер)",
                            data=download_response.content,
                            file_name=filename,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    else:
                        st.warning("⚠️ Excel-файл не знайдено або ще не готовий.")
            else:
                st.error(f"❌ Помилка: {response.status_code} - {response.text}")
else:
    st.warning("⚠️ Немає доступних парсерів")
