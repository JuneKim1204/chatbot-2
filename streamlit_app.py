import streamlit as st
from openai import OpenAI

# 타이틀 및 설명
st.title("💬 June's 이것저것 - 고민상담소")
st.write(
    """
    이 챗봇은 **OpenAI GPT-3.5** 모델을 기반으로 작동하는 작은 고민상담소입니다.  
    마음속 이야기를 털어놓고 싶다면 언제든 편하게 말 걸어보세요. 😊  
    아래에 OpenAI API 키를 입력하시면 바로 시작할 수 있어요.
    """
)

# API 키 입력
api_key = st.text_input("🔑 OpenAI API Key", type="password")

if not api_key:
    st.info("서비스를 사용하려면 OpenAI API 키를 입력해주세요.", icon="🗝️")
else:
    client = OpenAI(api_key=api_key)

    # 세션 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "너는 다정하고 따뜻한 고민상담 챗봇이야. 사용자의 고민을 공감하고 진심으로 위로해줘."}
        ]

    # 이전 메시지 출력
    for msg in st.session_state.messages[1:]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 사용자 입력 받기
    if prompt := st.chat_input("고민을 편하게 이야기해보세요 :)"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # GPT 응답 생성
        with st.chat_message("assistant"):
            try:
                stream = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state.messages,
                    stream=True,
                )
                response = st.write_stream(stream)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
            except Exception as e:
                st.error(f"❌ 오류가 발생했어요: {e}")
