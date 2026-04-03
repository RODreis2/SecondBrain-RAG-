from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
import glob

file_path = glob.glob("./books/*.pdf")
all_docs = []

for file in file_path:
    loader = PyPDFLoader(file)
    docs = loader.load()

    for doc in docs:
        doc.metadata["source"] = file
        
    all_docs.extend(docs)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=80,
    separators=["\n\n", "\n", ".", " "])

chunks = text_splitter.split_documents(all_docs)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
vector_store = FAISS.from_documents(chunks, embeddings)

template = """
        Answer all the question below based on books and context: 
    
        Here is the conversation history: {context}
        
        Question: {question}
"""

model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model



def handle_conversation():
    context = ""
    print("Hello my name is ollama, i'm here to help you abbout computing, type 'exit' to quite")
    while True:
        query = input("You: ")
        if query.lower() == "exit":
            break
        results = vector_store.similarity_search(query, k=3)

        context += "\n".join((doc.page_content for doc in results))
        
        response = chain.invoke({
                "context": context,
                "question": query
                })

        print("Bot: ", response)
        context += f"\nUser: {query}\nAI: {response}"

if __name__ == "__main__":
    handle_conversation()
