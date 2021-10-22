import requests
import streamlit as st

API_TOKEN = st.secrets['API_TOKEN']
headers = {'Authorization': f'Bearer {API_TOKEN}'}

st.title('Interact with AI4Afrika NLP models')

def query(payload, model_id):
    API_URL = f'https://api-inference.huggingface.co/models/{model_id}'
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

task = st.sidebar.radio('Tasks', ['Machine translation', 'Health chatbot'])
st.header(task)

if task == 'Machine translation':
    st.session_state['translation'] = ''

    with st.form('Translate'):
        payload = st.text_area('English text', 'Hello.')
        translate = st.form_submit_button('Translate')
        if translate:
            data = query(payload, 'AI4Afrika/bart-en-tw')
            # st.json(data)
            if isinstance(data, list):
                st.session_state['translation'] = data[0]['generated_text']
            elif isinstance(data, dict):
                st.info(f'{data["error"]}. Please wait about {int(data["estimated_time"])} seconds.')
        st.text_area('Twi translation', st.session_state['translation'])
elif task == 'Health chatbot':
    l, r = st.columns([3, 2])
    if 'history' not in st.session_state:
        st.session_state['history'] = []
    with r:
        message = st.text_area('Type your message', 'What is the menstrual cycle?')
        send = st.button('Send')
        clear = st.button('Clear history')
    if clear:
        st.session_state['history'] = []
    elif send:
        st.session_state['history'].append(message)
        response = query({
            'inputs': message,
            'parameters': {
                'max_length': 500
            }
        }, 'AI4Afrika/health-chatbot')
        reply = None
        if isinstance(response, list):
            reply = response[0]['generated_text'][len(message) + 1:]
        elif isinstance(response, dict):
            reply = f'{response["error"]}. Please wait about {int(response["estimated_time"])} seconds.'
        st.session_state['history'].append(reply)
    with l:
        st.text('History')
        for i, h in enumerate(st.session_state['history']):
            if i % 2 == 0:
                st.markdown(f'User:\n{h}')
            else:
                st.markdown(f'Chatbot:\n{h}')