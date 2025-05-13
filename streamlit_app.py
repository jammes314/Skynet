import streamlit as st
from transformers import pipeline

# Show title and description
st.title("💬 Chatbot - Question Answering with Custom Context")
st.write(
    "This chatbot answers questions based on a user-provided context using a Hugging Face transformer model. "
    "It does not use OpenAI's GPT models, and no API key is required."
)

# Load the QA pipeline only once
@st.cache_resource
def load_qa_pipeline():
    return pipeline("question-answering")

qa_pipeline = load_qa_pipeline()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User inputs for context and question
context = st.text_area("📄 Enter the context:", height=200)
question = st.text_input("❓ Enter your question about the context:")

# Button to get the answer
submit = st.button("Get Answer")

if submit and context and question:
    # Display user input
    st.chat_message("user").markdown(f"**Context:**\n{context}\n\n**Question:** {question}")

    # Get answer using the QA model
    result = qa_pipeline(question=question, context=context)
    answer = result["answer"]

    # Display answer
    st.chat_message("assistant").markdown(f"**Answer:** {answer}")

    # Update chat history
    st.session_state.messages.append({"role": "user", "content": f"**Context:**\n{context}\n\n**Question:** {question}"})
    st.session_state.messages.append({"role": "assistant", "content": f"**Answer:** {answer}"})

elif submit:
    st.warning("Please provide both a context and a question.")
