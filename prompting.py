from dotenv import load_dotenv
load_dotenv()  # Loads variables from .env
import os
import tiktoken  # For token counting

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

# Retrieve the API key from the environment.
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("Please set your OPENAI_API_KEY in the .env file.")

# Initialize the embeddings model with the "all-MiniLM-L6-v2" model.
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Load the FAISS index with dangerous deserialization enabled.
vectorstore = FAISS.load_local("faiss_index", embedding_model, allow_dangerous_deserialization=True)

# Create the ChatOpenAI instance with your API key.
llm = ChatOpenAI(model_name="gpt-4", temperature=0.2, openai_api_key=openai_api_key)

# Build the RetrievalQA chain. Here we limit the number of retrieved documents (k=1)
# and use a map_reduce chain type to help reduce token usage.
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
    chain_type="refine",  # or "refine" based on your preference
    verbose=False
)

def count_tokens(text, model="gpt-4"):
    """
    Counts the number of tokens in the given text using tiktoken for the specified model.
    
    Args:
        text (str): Text whose tokens are to be counted.
        model (str): The name of the model, default is "gpt-4".
    
    Returns:
        int: The number of tokens in the text.
    """
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def ask_gpt(query):
    """
    Generates an answer for the query using the QA chain.
    Also prints token counts for the query and the answer.
    
    Args:
        query (str): The user's query.
        
    Returns:
        str: The generated answer.
    """
    # Count tokens in the query.
    query_token_count = count_tokens(query)
    print(f"Query token count: {query_token_count}")
    
    # Generate the answer from the QA chain.
    answer = qa_chain.run(query)
    
    # Count tokens in the answer.
    answer_token_count = count_tokens(answer)
    print(f"Answer token count: {answer_token_count}")
    
    return answer

if __name__ == "__main__":
    sample_query = "What companies are in the IPC"
    answer = ask_gpt(sample_query)
    print("Query:", sample_query)
    print("Answer:", answer)
