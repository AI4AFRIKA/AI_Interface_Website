import requests
import streamlit as st

API_TOKEN = st.secrets['API_TOKEN']
G_TRANS_API_TOKEN = st.secrets['G_TRANS_API_TOKEN']
headers = {'Authorization': f'Bearer {API_TOKEN}'}

st.title('Interact with AI4Afrika NLP models')

def detect_lang(message):
    url = f'https://translation.googleapis.com/language/translate/v2/detect?key={G_TRANS_API_TOKEN}&q={message}'
    response = requests.get(url)
    return response.json()

def translate_src_to_en(message, src_lang):
    url = f'https://www.googleapis.com/language/translate/v2?key={G_TRANS_API_TOKEN}&source={src_lang}&target=en&q={message}'
    response = requests.get(url)
    return response.json()

def translate_en_to_src(message, src_lang):
    url = f'https://www.googleapis.com/language/translate/v2?key={G_TRANS_API_TOKEN}&source=en&target={src_lang}&q={message}'
    response = requests.get(url)
    return response.json()

def query(payload, model_id):
    API_URL = f'https://api-inference.huggingface.co/models/{model_id}'
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

task = st.sidebar.radio('Tasks', [
    # 'Machine translation',
    'Health chatbot'
])
st.header(task)

if task == 'Machine translation':
    st.session_state['translation'] = ''

    with st.form('Translate'):
        payload = st.text_area('English text', 'Hello.')
        translate = st.form_submit_button('Translate')
        if translate:
            data = query({
                'inputs': payload,
                'parameters': {
                    'max_length': 1000,
                }
            }, 'AI4Afrika/bart-en-tw')
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
        response = detect_lang(message)
        lang = response['data']['detections'][0][0]['language'][:2]
        message_en = message
        if lang != 'en':
            response = translate_src_to_en(message, lang)
            message_en = response['data']['translations'][0]['translatedText']
        st.session_state['history'].append(message)
        response = query({
            'inputs': message_en,
            'parameters': {
                'max_length': 500,
            }
        }, 'AI4Afrika/health-chatbot')
        reply = None
        if isinstance(response, list):
            reply = response[0]['generated_text'][len(message) + 1:]
            if lang != 'en':
                response = translate_en_to_src(reply, lang)
                reply = response['data']['translations'][0]['translatedText']
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