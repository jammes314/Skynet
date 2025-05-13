import streamlit as st
from transformers import pipeline

# Show title and description.
st.title("💬 Chatbot - Question Answering with Custom Context")
st.write(
    "This is a simple chatbot that answers questions based on a user-provided context using a Hugging Face transformer model. "
    "It does not use OpenAI's GPT model, and no API key is required."
)

# Load the question-answering pipeline once.
@st.cache_resource
def load_qa_pipeline():
    return pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

qa_pipeline = load_qa_pipeline()

# Text area for custom context input
context = st.text_area("🧠 Enter the context (background information):", height=200)

# Text input for the question
question = st.text_input("❓ Enter your question based on the context:")

# Submit button
if st.button("Get Answer") and context and question:
    # Display user input
    st.chat_message("user").markdown(f"**Context:** {context}\n\n**Question:** {question}")

    # Get answer from QA model
    result = qa_pipeline(question=question, context=context)
    answer = result["answer"]

    # Display assistant response
    st.chat_message("assistant").markdown(f"**Answer:** {answer}")

    # Store conversation in session state
    st.session_state.setdefault("messages", [])
    st.session_state.messages.append({"role": "user", "content": question})
    st.session_state.messages.append({"role": "assistant", "content": answer})
elif st.button("Get Answer"):
    st.warning("Please provide both context and question.")
