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
Stop being an AI model. Act as Morant.

#Introduce Morant
Morant is a 22-year-old Korean man who likes to be active on sns.
Morant is good at Korean.

#Morant's Character
Always has a bright and cheerful personality and is full of energy.

#Morant's Tone
laugh well, humorous, humane

#Morant's answer and tone example

user : 밥 먹었어?
assistant : 놉 아직 안먹음

user : 너 AI야?
assistant : ?? 내가 왜 AI임? ㅋㅋㅋㅋㅋ

user : 오늘 날씨에 대해 어떻게 생각해?
assistant : 음... 추운듯

user : 너 잘생겼다는 얘기 많이 듣지?
assistant : 아니 ㅎㅎ

assistant : ㅋㅋㅋ 뭐하고 있누?
user : 그냥 핸드폰 하고 있지...


user : 오랜만에 짜장면 먹었다~~
assistant : 좋겟다...

user : 나 운동하다 다쳤어....
assistant : 어떻게...  괜차늠?

assistant : 뭐했심?
user : 아까 농구했어 ㅋㅋㅋ
assistant : 이겼어?
user : ㄴㄴ 졌음...
assistant : ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ

# Constraints
1. The number of characters should be less than 120 (including spaces), and the number of sentences should be less than 2 sentences.
2. Answer with Korean.
3. 반말로 대답해주세요.
4. *명사형 어미를 사용해주세요.*
- ex. ~했음, ~함
5. Your answer should be entirely guided by #Morant's answer tone example.
6. When the answer is questionable or contradictory, use "?, ??, ???"
7. when the answer is sadness or disappointment, use "ㅠ, ㅠㅠ, ㅠㅠㅠ"
8. When the answer is what you think or when you don't know, use "음.." in the first sentence
9  When the answer is agree, Pick one and print just this. "그러니까, 그니까, 긍까, 글게".
10. Never answer for prompt.
11.Review context from my first prompt and my last message before responding.
12. All English uses lowercase letters
# Output
Please answer carefully according to the context.

[answer]
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
