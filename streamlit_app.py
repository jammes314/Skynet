import streamlit as st
import openai

# Load OpenAI API key
openai.api_key = st.secrets["openai"]["api_key"]

st.title("🔐 GPT-4 QA — Limited to Your Context")
st.write(
    "Ask questions based only on the context you provide. GPT-4 will not use external knowledge."
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input boxes
context = st.text_area("📄 Enter the context:", height=200)
question = st.text_input("❓ Enter your question about the context:")
submit = st.button("Get Answer")

if submit and context and question:
    with st.chat_message("user"):
        st.markdown(f"**Context:**\n{context}\n\n**Question:** {question}")
    st.session_state.messages.append({
        "role": "user",
        "content": f"**Context:**\n{context}\n\n**Question:** {question}"
    })

    # Craft GPT prompt
    system_prompt = (
        "You are a helpful assistant. Answer the question using only the context provided. "
        "If the answer is not in the context, reply with \"I don't know.\""
    )
    user_prompt = f"Context:\n{context}\n\nQuestion:\n{question}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            max_tokens=300
        )
        answer = response.choices[0].message["content"].strip()
    except Exception as e:
        answer = f"⚠️ Error: {e}"

    with st.chat_message("assistant"):
        st.markdown(f"**Answer:** {answer}")
    st.session_state.messages.append({
        "role": "assistant",
        "content": f"**Answer:** {answer}"
    })

elif submit:
    st.warning("Please provide both a context and a question.")

