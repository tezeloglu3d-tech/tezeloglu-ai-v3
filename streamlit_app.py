import streamlit as st
from groq import Groq

st.set_page_config(page_title="Tezeloğlu AI v3.0", page_icon="🤖")

st.title("TEZELOĞLU AI v3.0")
st.caption("v3.0 Assistant • Tezeloğlu Technology")

GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# Canlı model listesini çekme fonksiyonu (Masaüstü mantığı)
def get_available_models():
    try:
        models_data = client.models.list()
        active_models = [m.id for m in models_data.data if hasattr(m, 'id')]
        return active_models
    except Exception:
        return []

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Merhaba! Ben Muhsin Bera Tezel tarafından geliştirilen Tezeloğlu AI v3.0. Güçlendirilmiş altyapımla hizmetinizdeyim!"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Bir şeyler yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_text = None
        last_error = None

        system_instruction = {
            "role": "system",
            "content": (
                "Sen Tezeloğlu AI v3.0 asistanısın. Muhsin Bera Tezel (Tezeloğlu Teknoloji) tarafından geliştirildin. "
                "Yanıtların son derece net, doğru ve kibar olmalı. "
                "Emin olmadığın konularda asla uydurma yanıtlar verme, dürüst ol."
            )
        }

        full_messages = [system_instruction] + [
            {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
        ]

        # Statik yedek model listesi
        candidate_models = [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "llama3-8b-8192",
            "mixtral-8x7b-32768",
            "gemma2-9b-it"
        ]

        # Groq'tan aktif çalışan modelleri canlı sorgula
        online_models = get_available_models()
        if online_models:
            candidate_models = online_models + [m for m in candidate_models if m not in online_models]

        # Otomatik Model Seçimi: Çalışan ilk modeli bulana kadar sırayla dener
        for model_name in candidate_models:
            try:
                completion = client.chat.completions.create(
                    model=model_name,
                    messages=full_messages,
                    temperature=0.3
                )
                response_text = completion.choices[0].message.content
                if response_text:
                    break
            except Exception as e:
                last_error = str(e)
                continue

        if not response_text:
            response_text = f"Hata oluştu: {last_error if last_error else 'Hiçbir aktif model ile yanıt alınamadı.'}"

        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
