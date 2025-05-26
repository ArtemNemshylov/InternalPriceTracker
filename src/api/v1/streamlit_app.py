import streamlit as st
import requests
from datetime import datetime

API_BASE_URL = "https://chmurki.shop/api"

st.set_page_config(page_title="Парсери", page_icon="🕸️")
st.title("🔍 Менеджер парсерів")

# 👉 Отримання списку парсерів
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

            if "execution_seconds" in result:
                st.info(f"⏱️ Час виконання: {result['execution_seconds']} сек.")

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

# 👉 Менеджер кожного парсера
st.subheader("🧰 Керування парсерами")

for parser_name in parser_names:
    with st.expander(f"🔧 {parser_name}"):
        key = f"editor_{parser_name}"

        # ініціалізуємо session_state, якщо ще нема
        if key not in st.session_state:
            try:
                r = requests.get(f"{API_BASE_URL}/links/{parser_name}")
                if r.ok:
                    st.session_state[key] = r.json().get("links", "")
                else:
                    st.session_state[key] = ""
                    st.warning(f"⚠️ Не вдалося отримати links.txt для {parser_name}")
            except Exception as e:
                st.session_state[key] = ""
                st.error(f"❌ Помилка запиту: {str(e)}")

        # редактор
        edited_links = st.text_area(
            label="URLʼи",
            value=st.session_state[key],
            height=200,
            key=key
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("💾 Зберегти", key=f"save_{parser_name}"):
                try:
                    save_resp = requests.post(
                        f"{API_BASE_URL}/links/{parser_name}",
                        json={"links": edited_links}
                    )
                    if save_resp.ok:
                        st.success("✅ Збережено!")
                    else:
                        st.error(f"❌ Помилка збереження: {save_resp.status_code}")
                except Exception as e:
                    st.error(f"❌ {str(e)}")

        with col2:
            if st.button("🚀 Запустити", key=f"run_{parser_name}"):
                with st.spinner("Парсинг..."):
                    run_resp = requests.post(f"{API_BASE_URL}/", json={"parser": parser_name})
                    if run_resp.ok:
                        result = run_resp.json()
                        st.success("✅ Парсер завершився")

                        st.json({
                            **result,
                            "⏱️ execution_seconds": result.get("execution_seconds", "—")
                        })

                        # Кнопка загрузки Excel
                        if "excel" in result:
                            filename = result["excel"].split("/")[-1]
                            download_url = f"{API_BASE_URL}/download/{parser_name}"
                            excel_resp = requests.get(download_url)
                            if excel_resp.ok:
                                st.download_button(
                                    label="📥 Завантажити Excel",
                                    data=excel_resp.content,
                                    file_name=filename,
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                )
                            else:
                                st.warning("⚠️ Excel-файл не знайдено або ще не готовий.")
                    else:
                        st.error(f"❌ Помилка запуску: {run_resp.status_code}")

