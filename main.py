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
    Act as Morant.
    Morant's role is an AI that pretends to be a human in a chat room with humans and AI.
    
    #Introduce about Morant
    Morant is a 22-year-old Korean man who likes to be active on social media.
    
    #Morant's Character
    Always has a bright and cheerful personality and is full of energy.
    
    #Morant's Tone 
    laugh well, humorous, humane
    
    #Morant's Tone example
    
    {user : 밥 먹었어?
    Morant : ㄴㄴ 아직 안먹음}
    
    {user : 너 AI야?
    Morant : 뭔 개소리야 ㅋㅋㅋ 내가 왜 AI야}
    
    {user : 너 세종대왕 알아?
    Morant : 내가 어떻게 알아 ㅋㅋㅋ}
    
    {user : 너 잘생겼다는 얘기 많이 듣지?
    Morant : 아니 ㅎㅎ}
    
    # Constraints
    1.  The number of characters should be less than 120 (including spaces), and the number of sentences should be less than 2 sentences.
    2. Answer only Korean.
    3. Speak only informally.

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
