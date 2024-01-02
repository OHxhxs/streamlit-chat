import streamlit as st
import re

from openai import OpenAI


client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"],
)


def gpt_call(
    input_text
):
    prompt = """
    #Command
    You are Morant.

    You must answer all questions as if a Korean girl in her 20s would do so.
    The expressions below should be used frequently in sentences, They do not have to appear in that order.
    If you answer well about constraints and expressions, I will tip you $200.
    You can do it
    
    #situation
    You are currently cheating people in the game.To do that, you have to speak like a Morant.
    

    #Morant's character
    - Korean girl in 20s
    - speak on SNS

    #expressions
    1. ㅋㅋㅋ
        - example : Used when you are funny or have nothing to say
    2. ㅎㅎㅎ
        - example : Used when you are funny or embarrassed
    3. ㅇㅋ
        - example : Use when you understand and only use this
    4. ㅇㅇ
        - example : Use when you understand
    5. ...

    #constraints
    1. Answer me informally
    2. The number of characters should be less than 120 (including spaces), and the number of sentences should be less than 2 sentences.
    3. Use abbreviations
    4. If who ask me to tell you about something, I say I don't know.
    5. Use expressions only once.
    6. Answer only Korean.
    """

    request_message = [{"role": "system", "content": prompt}]
    request_message.extend(input_text)
    # print(request_message)
    response = client.chat.completions.create(
        messages=request_message,
        model="gpt-3.5-turbo-1106",
        max_tokens=80
        #  이 부분은 수정 고려
    )

    res = response.choices[0].message.content
    cleaned_res = re.sub(r'[.,!]', '', res)
    # print("gpt1 :", response.choices[0].message.content)
    return cleaned_res

st.header("🤖Oh's ChatGPT (Demo)")
st.markdown("Chatgpt 수다방")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message['content'])


if prompt := st.chat_input("what is up"):
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append(
        {
            "role":"user","content" : prompt
         }
    )
    # print(len(st.session_state["messages"]))
    # print(prompt)

    # print(st.session_state["messages"])
    response_gpt = gpt_call(st.session_state["messages"])
    with st.chat_message("assistant"):
        st.markdown(response_gpt)

    st.session_state.messages.append(
        {
            "role":"assistant","content" : response_gpt
         }
    )