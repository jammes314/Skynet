import streamlit as st
import openai

# Set up the title and description
st.title("📘 Contextual Q&A Chatbot (OpenAI)")
st.write(
    "This chatbot uses OpenAI to answer **only** based on the provided context. "
    "Paste your OpenAI API key below to start."
)

# Input for OpenAI API key
api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")

if not api_key:
    st.warning("Please enter your OpenAI API key to continue.")
    st.stop()

# Set the API key for OpenAI
openai.api_key = api_key

# Input for context and question
context = st.text_area("🧠 Context", height=200, placeholder="Paste your context here...")
question = st.text_input("❓ Your question about the context")

# Button to get answer
if st.button("💬 Get Answer"):
    if not context or not question:
        st.error("Please provide both a context and a question.")
    else:
        with st.spinner("Thinking..."):
            try:
                # Call the OpenAI API with context + question
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Answer the user's question using only the provided context. If the context is insufficient, say you don't know."},
                        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
                    ],
                    temperature=0.2
                )
                answer = response["choices"][0]["message"]["content"]
                st.success("✅ Answer:")
                st.markdown(answer)
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
