import qdrant_client
from langchain_qdrant import Qdrant
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from pathlib import Path
from google.generativeai import GenerativeModel


def search(query):
    model_name = "models/embedding-001"
    hf = GoogleGenerativeAIEmbeddings(model=model_name)
    client = qdrant_client.QdrantClient(path=Path.home() / "local_qdrant")
    collection_name = "MyCollection"
    qdrant = Qdrant(client, collection_name, hf)

    found_docs = qdrant.similarity_search(query=query, k=10)
    i = 0
    list_res = []
    for res in found_docs:
        list_res.append({"id":i,"path":res.metadata.get("path"),"content":res.page_content})
    return list_res


def retrieve_and_answer(query):
    output_parser = StrOutputParser()

    model_name = "models/embedding-001"
    hf = GoogleGenerativeAIEmbeddings(model=model_name)
    client = qdrant_client.QdrantClient(path=Path.home() / "local_qdrant")
    collection_name = "MyCollection"
    qdrant = Qdrant(client, collection_name, hf)

    found_docs = qdrant.similarity_search(query=query, k=10)

    i = 0
    list_res = []
    context = ""
    mappings = {}
    for res in found_docs:
        context = context + str(i)+"\n"+res.page_content+"\n\n"
        mappings[i] = res.metadata.get("path")
        list_res.append({"id":i,"path":res.metadata.get("path"),"content":res.page_content})
        i = i +1

    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0, convert_system_message_to_human=True)
    # prompt = """"Answer the user’s question using the documents given in the context. In the context are documents that should contain an answer. Please always reference the document ID (in square brackets, for example [0],[1]) of the document that was used to make a claim. Use as many citations and documents as it is necessary to answer a question."
    #           'Documents:\n{context}\n\nQuestion: {query}'"""
    prompt = """"Responda as questões do usuário em PORTUGUÊS usando como contexto os documentos fornecidos. No contexto estão os documentos que contém as respostas. Por favor sempre referencie o ID do documento (em colchetes, por exemplo [0],[1]) de cada documento que foi usado para fazer a chamada. Use quantas citações e documentos que achar necessário para responder a questão."
              'Documentos:\n{context}\n\n Questão: {query}'"""

    prompt = ChatPromptTemplate.from_template(template=prompt)
    chain = (
        RunnablePassthrough()
        | prompt
        | model
        | output_parser
    )
    results = chain.invoke( {"context":context, "query":query})

    #Resultado chamando diretamento o LLM
    prompt2 = query
    # Create a model instance
    model2 = GenerativeModel('gemini-1.5-flash') 
    responseModel = model2.generate_content(prompt2)
    print("Resposta LLM:", responseModel.text)

    return results,list_res, responseModel.text