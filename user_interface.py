import re
import streamlit as st
import requests
import json
import os   
from indexing1 import main_indexing as main_index
def list_document_titles(documents_index_path):
    # Get a list of all files in the directory
    files = [f for f in os.listdir(documents_index_path) if os.path.isfile(os.path.join(documents_index_path, f))]

    # Get the title of each file
    titles = [os.path.splitext(file)[0] for file in files]  # os.path.splitext(file)[0] gets the file name without the extension

    return titles

st.title('_:orange[Avivatec RAG]_ :sunglasses:')

# Sidebar for user inputs
st.sidebar.title("Configuration")
#google_api_key = st.sidebar.text_input("Gemini API Key", "", type="password")
#if st.sidebar.button("Submit"):
with open('.env', 'w') as f:
    f.write(f"GOOGLE_API_KEY=AIzaSyBbtSUAG7E2S60Nq8uL0GPiJuxUODgzzlE")
        # f.write(f"GOOGLE_API_KEY={google_api_key}")

uploaded_file = st.sidebar.file_uploader("Upload de Documentos", type=['txt', 'pdf', 'docx'])

documents_index_path = os.path.join(os.path.expanduser("~"), "documents_index")

if uploaded_file is not None:
    with open(os.path.join(documents_index_path, uploaded_file.name), 'wb') as f:
        f.write(uploaded_file.getbuffer())
    st.sidebar.success('File \'{}\' uploaded successfully.'.format(uploaded_file.name))

    if st.sidebar.button("Indexar Documentos"):
        st.sidebar.text("Indexação em progresso...")
        # Call your indexing function here
        main_index(documents_index_path)
        st.sidebar.text("Indexing completed.")

document_titles = list_document_titles(documents_index_path)
for title in document_titles:
    st.sidebar.text(title)   

question = st.text_input("Faça uma pergunta para seu ChatGPT privado", "")
if st.button("Clique aqui para fazer sua pergunta"):
    st.divider()
    st.markdown("<h3 style='color: black;'>Resposta baseada estritamente nos documentos</h3>", unsafe_allow_html=True)
    st.write("A pergunta foi \"", question+"\"")
    url = "http://localhost:8000/answer"

    payload = json.dumps({
      "query": question
    })
    headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    answer = json.loads(response.text)["answer"]
    rege = re.compile("\[Document\ [0-9]+\]|\[[0-9]+\]")
    m = rege.findall(answer)
    num = []
    for n in m:
        num = num + [int(s) for s in re.findall(r'\b\d+\b', n)]
    st.markdown(answer)
    
    st.divider()
    st.markdown("<h3 style='color: black;'>Resposta do LLM</h3>", unsafe_allow_html=True)
    respLLM = json.loads(response.text)['respostaLLM']
    st.markdown(respLLM)
    
    documents = json.loads(response.text)['context']
    show_docs = []
    for n in num:
        for doc in documents:
            if int(doc['id']) == n:
                show_docs.append(doc)
    
    st.divider()
    st.markdown("<h3 style='color: black;'>Documentos baseados</h3>", unsafe_allow_html=True)
    a = 1244
    for doc in show_docs:
        with st.expander(str(doc['id'])+" - "+doc['path']):
            st.write(doc['content'])
            with open(doc['path'], 'rb') as f:
                st.download_button("Download file", f, file_name=doc['path'].split('/')[-1],key=a)
                a = a + 1