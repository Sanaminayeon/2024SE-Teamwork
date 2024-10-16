
import streamlit as st
import pandas as pd
from langchain_community.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate

@st.cache_resource
def get_chain():
    llm  = HuggingFacePipeline.from_model_id(
    model_id="THUDM/chatglm3-6b",
    task="text-generation",
    device=0,
    model_kwargs={"trust_remote_code":True,
                #   "temperature":0.9,
                #   "do_sample":True
                  },
    pipeline_kwargs={"max_new_tokens": 5000},
        )
    template = """{question}"""
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm
    return chain

def greet2(name):
    response = get_chain().invoke({"question": name})
    return response

# st.title('🦜🔗 Quickstart App')
st.set_page_config(page_title="Andy Chatbot")
with st.sidebar:
    st.title('Andy Chatbot')
    st.success('API key already provided!', icon='✅')
    replicate_api = st.text_input('Enter Replicate API token:', type='password')
    st.warning('Please enter your credentials!', icon='⚠️')
    st.success('Proceed to entering your prompt message!', icon='👉')
    st.subheader('Models and parameters')
    selected_model = st.sidebar.selectbox('Choose a Llama2 model', ['Llama2-7B', 'Llama2-13B', 'Llama2-70B'], key='selected_model')
    if selected_model == 'Llama2-7B':
        llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    elif selected_model == 'Llama2-13B':
        llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
    else:
        llm = 'replicate/llama70b-v2-chat:e951f18578850b652510200860fc4ea62b3b16fac280f83ff32282f87bbd2e48'
      
    temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.sidebar.slider('max_length', min_value=64, max_value=4096, value=512, step=8)
    st.markdown('📖 Learn how to build this app in this [blog](https://blog.streamlit.io/how-to-build-a-llama-2-chatbot/)!')

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]    

    # Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)


# Function for generating LLaMA2 response
def generate_llama2_response(prompt_input):
    return greet2(prompt_input)

# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_llama2_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)


