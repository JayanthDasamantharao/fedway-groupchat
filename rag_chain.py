import os
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
# openai_api_key = st.secrets["OPENAI_API_KEY"]

# 1. Load vector store
embedding_model = OpenAIEmbeddings(openai_api_key=openai_api_key)
vectorstore = Chroma(persist_directory="chroma_db", embedding_function=embedding_model)
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 4})

# 2. Setup OpenAI LLM
llm = ChatOpenAI(model="gpt-4", temperature=0.15, openai_api_key=openai_api_key)

# 3. Custom prompt with smart escalation behavior
custom_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful assistant answering based only on the given POET system instructions.

If the user is asking to speak with a human representative without providing a question, clarify what they need help with first.
If the user query is incomplete, respond with "Could you please clarify your question so I can assist you better?"

Only if you cannot answer based on the context below, respond with:
"I'm not sure, let me connect you to a human representative."

Context:
{context}

Question:
{question}
"""
)

# 4. Create RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": custom_prompt},
    return_source_documents=True,
)

# 5. Function to query
def ask_question(query, suppress_escalation=False):
    result = qa_chain.invoke({"query": query})
    response = result["result"]

    # Define conditions that imply LLM doesn't know
    low_confidence = any(
        phrase in response.lower()
        for phrase in [
            "i'm not sure",
            "i do not know",
            "sorry",
            "as an ai language model",
            "cannot answer",
            "no information"
        ]
    )

    if low_confidence:
        if suppress_escalation:
            response = "🤖 Sorry, I couldn't find that in the docs."
        else:
            response = "I'm not sure, let me connect you to a human representative."

    return response

# 6. Compute similarity score for confidence check
def get_top_doc_score(query):
    results = vectorstore.similarity_search_with_score(query, k=2)
    if not results:
        print("[DEBUG] No results found.")
        return 1.0
    doc, score = results[0]
    # print(f"[DEBUG] Score: {score:.3f}")
    # print(f"[DEBUG] Top doc snippet: {doc.page_content[:200]}")
    return score

# Example test
if __name__ == "__main__":
    question = "What is the capital of USA?"
    print("Answer:", ask_question(question))
