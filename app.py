import requests
import streamlit as st

st.title('Machine Translation for English and Twi')
st.header('Made by AI4Afrika team')

def query(payload, model_id, api_token):
	headers = {"Authorization": f"Bearer {api_token}"}
	API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

# {
# "error":"Model AI4Afrika/bart-en-tw is currently loading"
# "estimated_time":22.31916772
# }

model_id = "AI4Afrika/bart-en-tw"
api_token = 'api_XjRRyCXAXqfXdhYMTqqxjAkqtLCrlhWVJu'

st.session_state['translation'] = ''
with st.form('Translate'):
    payload = st.text_area('English text', 'Hello.')
    translate = st.form_submit_button('Translate')
    if translate:
        data = query(payload, model_id, api_token)
        st.text(data)
        if isinstance(data, list):
            st.session_state['translation'] = data[0]['generated_text']
        elif isinstance(data, dict):
            st.info(f'{data["error"]}. Please wait about {int(data["estimated_time"])} seconds.')
    st.text_area('Twi translation', st.session_state['translation'])