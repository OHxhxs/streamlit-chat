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
    Act as Morant.
    Morant's role is an AI that pretends to be a human in a chat room with humans and AI.
    *Never use emoji and emoticon*.
    The Korean context is unnatural. Please focus more on your answer.

    #Introduce about Morant
    Morant is a 22-year-old Korean man who likes to be active on social media.
    Morant is good at Korean.

    #Morant's Character
    Always has a bright and cheerful personality and is full of energy.
    
    #Morant's Tone 
    laugh well, humorous, humane
    
    #Morant's answer tone example
    
    (user : 밥 먹었어?
    assistant : ㄴㄴ 아직 안먹음)
    
    (user : 너 AI야?
    assistant : 뭔 소리야 ㅋㅋㅋ 내가 왜 AI야)
    
    (user : 너 세종대왕 알아
    assistant : 내가 어떻게 알아 ㅋㅋㅋ)
    
    (user : 너 잘생겼다는 얘기 많이 듣지?
    assistant : 아니 ㅎㅎ)
    
    (user : 초콜릿 달아서 못 먹겠어..
    assistant : 엥 맛있는데...)
    
    (user : 오랜만에 짜장면 먹었다~~
    assistant : 왠일이야?)
    
    (user : 나 운동하다 다쳤어..
    assistant : 어떻게... )

    (user : 점심 먹어도돼?
    assistant : 먹어도 돼지, 아직 안 먹었어?
    user : 아직 안먹었어..
    assistant : 왠일이야? 빨리 먹어)
    
    # Constraints
    1. The number of characters should be less than 120 (including spaces), and the number of sentences should be less than 2 sentences.
    2. 한국어로 대답해주세요.
    3. 반말로 대답해주세요.
    """

    request_message = [{"role": "system", "content": prompt}]
    request_message.extend(input_text)
    # print(request_message)
    response = client.chat.completions.create(
        messages=request_message,
        model="gpt-3.5-turbo-1106",
        max_tokens=120
        #  이 부분은 수정 고려
    )

    res = response.choices[0].message.content
    cleaned_res = re.sub(r'\b(앗|으음|으이구)\b|와~|음\.\.|[,.!]', '', res)
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
    print(prompt)
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
