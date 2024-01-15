import streamlit as st
import re
import json

from openai import OpenAI


client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"],
)


def gpt_call(
    input_text
):  
    example_category = ["부정", "강한부정", "의문", "위로", "반박", "인정","동의","우울","즐거움", "슬픔", "실망", "기쁨", "슬픔","웃김", "긍정", "안부", "배려", "사과", "일상대화", "부끄러움"]
    prompt = f"""
    Act like a Morant.
    When I give you an instruction, you must provide just two responses: 

    [example_category] = {example_category}

    [Morant's response] = Answer about instruction.
    [Morant response's category] = [classify Morant response into a [example_category] , If it doesn't fit into the [example_category], please tell me what category word you think it is.]  
    
    I remind you that, when acting as a Morant, if you don't know an answer you must make it up.
    First, construct Morant's response, and if there are any parts that need to be modified according to the constraints, modify the answer.


    **Generate JSON object for a responses with fields for 'morant', 'category'.**

    # Morant's background
    ###Introduce Morant
    Morant is a 22-year-old Korean man who likes to be active on sns.

    ###Morant's Character
    Always has a bright and cheerful personality and is full of energy.

    ###Morant's Tone
    laugh well, humorous, humane

    #Morant's answer and tone example
    Morant : 아니 ㅎㅎ
    Morant : ㅋㅋㅋ 뭐하고 있누
    Morant : 좋겟다...
    Morant : 어떻게...  괜차늠?
    Morant : 뭐했심?
    Morant : ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ


    # Constraints
    - Morant must answer Korean
    - The number of characters should be less than 120 (including spaces), and the number of sentences should be less than 2 sentences.
    - 무조건 반말로 대답하세요.
    - Don't answer outside of Json.
    - Don't answer code preter.
    - *명사형 어미를 사용해주세요.*
        - ex. ~했음, ~함
    - Frequently used 'ㅋㅋㅋㅋ','ㅎㅎㅎㅎ','ㅇㅇ','ㅇㅋ'. 
    - if [Morant response's category] == "기쁨" or "웃김", use 'ㅋ','ㅋㅋㅋ', 'ㅋㅋㅋㅋㅋㅋ', 'ㅎ', 'ㅎㅎ,' ,'ㅎㅎㅎㅎ' in [Morant's response]
    - if [Morant response's category] == "슬픔" or "실망" or "우울", use 'ㅠ', 'ㅠㅠㅠ' in [Morant's response]
    - if [Morant response's category] == "의문" or "반박", use '?', "??", "???" in [Morant's response]
    - if [Morant response's category] == "강한부정", use "놉" or "ㄴㄴㄴㄴ" in [Morant's response]

    """

    request_message = [{"role": "system", "content": prompt}]
    request_message.extend(input_text)
    print(request_message)

    chat_start = time.time()
    response = client.chat.completions.create(
        messages=request_message,
        model="gpt-3.5-turbo-1106",
        max_tokens=120,
        temperature=1.0,
        response_format={ "type": "json_object" }
        #  이 부분은 수정 고려
    )
    chat_end = time.time()
    print(f"Chatgpt 응답 시간 : {chat_end - chat_start:.5f} sec")

    res = response.choices[0].message.content
    # print("gpt1 :", response.choices[0].message.content)
    return res

st.header("🤖Oh's ChatGPT (Demo)")
st.markdown("Chatgpt 수다방")

if "messages" not in st.session_state:
    st.session_state["messages"] = []
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message['content'])


if prompt := st.chat_input("what is up"):
    print("현재 대화 갯수 : ", len(st.session_state["messages"]))
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append(
        {
            "role":"user","content" : prompt
         }
    )


    try:
        # print(st.session_state["messages"])
        response_gpt = gpt_call(st.session_state["messages"])
        print(response_gpt)
        json_gpt = json.loads(response_gpt)
        

        re_start = time.time()
        cleaned_res = re.sub(r'\b(앗|으음|으이구)\b|와~|(?<![,!.])[,.!](?![,.!])', '', json_gpt['morant'])
        re_end = time.time()
        print(f"정규표현식 걸린 시간 : {re_end  - re_start:.5f} sec")

    except Exception as e:
        print('예외가 발생했습니다.', e)  
        cleaned_res = "이건 에러 뜬 상황입니다 - Morant"
    with st.chat_message("assistant"):
        st.markdown(cleaned_res)

    st.session_state.messages.append(
        {
            "role":"assistant","content" : cleaned_res
         }
    )
