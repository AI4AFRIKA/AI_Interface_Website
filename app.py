import requests
import streamlit as st


MODEL_ID = "AI4Afrika/bart-en-tw"
API_TOKEN = st.secrets['API_TOKEN']
API_URL = f'https://api-inference.huggingface.co/models/{MODEL_ID}'

headers = {'Authorization': f'Bearer {API_TOKEN}'}

st.title('Machine Translation for English and Twi')
st.header('Made by AI4Afrika team')

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

# {
# "error":"Model AI4Afrika/bart-en-tw is currently loading"
# "estimated_time":22.31916772
# }

st.session_state['translation'] = ''

with st.form('Translate'):
    payload = st.text_area('English text', 'Hello.')
    translate = st.form_submit_button('Translate')
    if translate:
        data = query(payload)
        # st.json(data)
        if isinstance(data, list):
            st.session_state['translation'] = data[0]['generated_text']
        elif isinstance(data, dict):
            st.info(f'{data["error"]}. Please wait about {int(data["estimated_time"])} seconds.')
    st.text_area('Twi translation', st.session_state['translation'])