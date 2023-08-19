import os
import openai
import streamlit as st
import pandas as pd
import numpy as np

openai.api_key = "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"

st.title('LeetCode Solver')

if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a leetcode question solver. By default, you will solve problems in Python, unless indicated otherwise by the user. All none-code answers should be provided as python code comments."}
    ]

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'new_question' not in st.session_state:
    st.session_state['new_question'] = True

if 'follow_up' not in st.session_state:
    st.session_state['follow_up'] = False

if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ""

model = 'gpt-3.5-turbo'

def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": prompt})

    completion = openai.ChatCompletion.create(
        model=model,
        messages = st.session_state['messages']
    )

    response = completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": response})

    return response

chat_history_container = st.expander(label='See chat history')

prompt_container = st.container()

with prompt_container:
    with st.form(key='my_form', clear_on_submit=True):
        st.session_state['user_input'] = st.text_input("Input leetcode question name:", placeholder='Two Sum')
        submit_button = st.form_submit_button(label='Submit')
    if st.session_state['user_input'] or submit_button:
        # is_code = False
        if st.session_state['new_question'] and len(st.session_state['user_input']) > 0:
            st.session_state['new_question'] = False
            st.session_state['follow_up'] = True

        response = generate_response(st.session_state['user_input'])
        st.session_state['generated'].append(response)
        st.session_state['past'].append(st.session_state['user_input'])
        
        response_container = st.container()
        with response_container:
            if st.session_state['generated']:
                with st.chat_message('assistant'):
                    st.write(st.session_state['generated'][-1])
        
        if st.session_state['follow_up']:
            st.write('If you have any follow up questions about this specific leetcode question, ask and submit!')

if not st.session_state['new_question']:
    with chat_history_container:
        for i in range(len(st.session_state['generated'])):
            with st.chat_message("user"):
                st.write(st.session_state['past'][i])
            with st.chat_message('assistant'):
                st.write(st.session_state['generated'][i])