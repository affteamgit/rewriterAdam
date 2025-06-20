import streamlit as st
from openai import OpenAI

# Load your API key from Streamlit secrets
api_key = st.secrets.get("openai_api_key", "YOUR_OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Your fine-tuned model name
FINE_TUNED_MODEL = "ft:gpt-4.1-2025-04-14:affiliation:adam02:BkGyzpHF"

st.title("📝 Rewrite in Adam's Tone and Voice")
st.write("Upload a file or paste content to have it rewritten by Adam's fine-tuned GPT model.")

# File uploader
uploaded_file = st.file_uploader("Upload a text file", type=["txt", "md"])

# Or manual input
manual_input = st.text_area("Or paste your content here:", height=200)

# Choose source
if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
elif manual_input:
    content = manual_input
else:
    content = ""

if content:
    if st.button("Rewrite in Adam's Voice"):
        with st.spinner("Rewriting with Adam's tone and style..."):
            try:
                response = client.chat.completions.create(
                    model=FINE_TUNED_MODEL,
                    messages=[
                        {"role": "system", "content": "You are Adam, a crypto casino reviewer with a sharp, conversational tone and honest takes."},
                        {"role": "user", "content": f"Rewrite this review in Adam's tone, style, and voice:\n\n{content}"}
                    ]
                )
                rewritten = response.choices[0].message.content
                st.subheader("🔁 Rewritten Output:")
                st.text_area("Adam's Version", rewritten, height=300)

                # Optionally download
                st.download_button("💾 Download Rewritten Review", rewritten, file_name="rewritten_by_adam.txt")

            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.info("Please upload a file or paste content above to begin.")
