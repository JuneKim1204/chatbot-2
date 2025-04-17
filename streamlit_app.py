pip install python-dotenv

import streamlit as st
import openai
from dotenv import load_dotenv
import os

# 환경 변수 불러오기 (.env 사용 시)
load_dotenv()

# 앱 제목 및 설명
st.title("💬 June's 이것저것 - 고민상담소")

st.write(
    """
    이 챗봇은 **OpenAI GPT-3.5** 모델을 기반으로 작동하는 작은 고민상담소입니다.  
    누구나 마음속에 담아둔 이야기, 말하지 못한 고민이 있잖아요.  
    이곳에서는 그런 이야기를 편하게 나눌 수 있어요. 😊  
    아래에 **OpenAI API 키**를 입력하시면 바로 상담을 시작할 수 있습니다.
    """
)

# API 키 입력
openai_api_key = st.text_input("🔑 OpenAI API Key", type="password")

if not openai_api_key:
    st.info("서비스를 이용하려면 OpenAI API 키를 입력해주세요.", icon="🗝️")
else:
    openai.api_key = openai_api_key

    # 대화 메시지를 세션 상태에 저장
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": "너는 따뜻하고 다정한 고민상담 챗봇이야. 사용자의 고민을 공감하고 진심 어린 조언을 해줘.",
            }
        ]

    # 이전 대화 보여주기
    for msg in st.session_state.messages[1:]:  # system 메시지는 제외하고 출력
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 사용자 입력 받기
    if prompt := st.chat_input("고민을 편하게 이야기해보세요 :)"):

        # 사용자 메시지 저장 및 출력
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 어시스턴트 응답 생성 및 출력
        with st.chat_message("assistant"):
            try:
                stream = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state.messages,
                    stream=True,
                )

                response = st.write_stream(stream)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )

            except Exception as e:
                st.error(f"⚠️ 오류가 발생했어요: {e}")
