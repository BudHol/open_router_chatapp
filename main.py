from langchain_openrouter import ChatOpenRouter
import streamlit as st 
import numpy as np 
import random 
import time
import os 


os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'



st.title("OpenRouter Chatbot") 
with st.sidebar:
    st.title("Quick Settings")
    st.space("small")
    st.write("Configure API Keys")
    openrouter_input = st.text_input("OpenRouter API Key")
    langchain_input = st.text_input("Langchain API Key")
    st.space("xsmall")
    option = st.selectbox("Select Model/Context", ["Nvidia Nemotron 3 Nano Omni (Reasoning)", "Minimax M2.5", "Nvidia Nemotron 3 Super"])

os.environ["OPENROUTER_API_KEY"] = openrouter_input
os.environ['LANGCHAIN_API_KEY'] = langchain_input

def model_call(option):
    if option == "Nvidia Nemotron 3 Nano Omni": 
        return "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free" 
    if option == "Meta Llama 3.2B": 
        return "minimax/minimax-m2.5:free" 
    else: 
        return "nvidia/nemotron-3-super-120b-a12b:free"
    
def waiting_mesg():
    while True: 
        response = random.choice(
                [
                    "Thinking..",
                    "Generating...", 
                    "Locking in for this one...",
                ]) 
        yield response
        
         



def response_call(prompt,context):
    model = ChatOpenRouter(
    model=model_call(option),
    temperature=0.8,
    )
    if context: 
        query = f"Conversation history: {context} \n New user query: {prompt}"
    else: 
        query = prompt
    response = model.invoke(query) 
    result = response.content 

    for char in result: 
        yield char 
        time.sleep(0.01)


if "messages" not in st.session_state: 
    st.session_state.messages = [] 

for message in st.session_state.messages: 
    with st.chat_message(message["role"]): 
        st.markdown(message["content"])

if prompt := st.chat_input("Say something"): 
    n = len(st.session_state.messages)
    if n != 0: 
        x = st.session_state.messages[n-1]["content"]
    else: 
        x = None
    with st.chat_message("user"): 
        st.markdown(prompt)
    st.session_state.messages.append({"role":"user","content":prompt}) 

    with st.chat_message("assistant"): 
        with st.spinner(next(waiting_mesg())):

            response = st.write_stream(response_call(prompt,x))
    st.session_state.messages.append({"role":"assistant","content":response})

