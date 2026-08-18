import streamlit as st
from groq import Groq

st.set_page_config(page_title="Tezeloğlu AI v3.0", page_icon="🤖")

st.title("TEZELOĞLU AI v3.0")
st.caption("v3.0 Assistant • Tezeloğlu Technology")

# Groq API Bağlantısı
groq_api_key = "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"
client = Groq(api_key=groq_api_key)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Merhaba! Ben Muhsin Bera Tezel tarafından geliştirilen Tezeloğlu AI v3.0. Güçlendirilmiş altyapımla hizmetinizdeyim!"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Bir şeyler yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            system_instruction = {
                "role": "system",
                "content": "Sen Tezeloğlu AI v3.0 asistanısın. Muhsin Bera Tezel (Tezeloğlu Teknoloji) tarafından geliştirildin. Yanıtların son derece net, doğru ve kibar olmalı."
            }
            full_messages = [system_instruction] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=full_messages,
                temperature=0.3
            )
            response = completion.choices[0].message.content
        except Exception as e:
            response = f"Hata oluştu: {str(e)}"
            
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
