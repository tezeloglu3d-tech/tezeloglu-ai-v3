import streamlit as st
import urllib.request
import json

st.set_page_config(page_title="Tezeloğlu AI v3.0", page_icon="🤖")

st.title("TEZELOĞLU AI v3.0")
st.caption("v3.0 Assistant • Tezeloğlu Technology")

GROQ_API_KEY = "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"

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
        try:
            payload = {
                "model": "llama3-8b-8192",
                "messages": [
                    {
                        "role": "system",
                        "content": "Sen Tezeloğlu AI v3.0 asistanısın. Muhsin Bera Tezel (Tezeloğlu Teknoloji) tarafından geliştirildin. Yanıtların son derece net, doğru ve kibar olmalı."
                    }
                ] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                "temperature": 0.3
            }
            
            req = urllib.request.Request(
                "https://api.groq.com/openai/v1/chat/completions",
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0"
                }
            )
            
            with urllib.request.urlopen(req) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                reply = res_data["choices"][0]["message"]["content"]
                
        except Exception as e:
            reply = f"Hata oluştu: {str(e)}"

        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
