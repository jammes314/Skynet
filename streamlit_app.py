import streamlit as st
from transformers import pipeline

# Show title and description.
st.title("💬 Chatbot - Question Answering with Fixed Context")
st.write(
    "This is a simple chatbot that answers questions based on a fixed context using a Hugging Face transformer model. "
    "It does not use OpenAI's GPT model, and no API key is required."
)

# Load the question-answering pipeline once.
@st.cache_resource
def load_qa_pipeline():
    return pipeline("question-answering")

qa_pipeline = load_qa_pipeline()

# Define the fixed context.
context = (
    "Artificial intelligence (AI) is a branch of computer science that aims to create machines that can perform tasks that would normally require human intelligence. "
    "Machine learning (ML) is a subset of AI that involves the use of algorithms and statistical models to enable computers to improve their performance on a task through experience. "
    "One common application of ML is in the field of natural language processing (NLP), where algorithms are used to understand and generate human language. "
    "For example, GPT-3 is a state-of-the-art language model developed by OpenAI that can generate human-like text based on a given prompt."
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user input
if question := st.chat_input("Ask a question based on the context above:"):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Generate answer using the QA pipeline
    result = qa_pipeline(question=question, context=context)
    answer = result["answer"]

    # Append assistant message
    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})

