import streamlit as st
from openai import OpenAI

# Load your API key from Streamlit secrets
api_key = st.secrets.get("openai_api_key", "YOUR_OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Your fine-tuned model name
FINE_TUNED_MODEL = "ft:gpt-3.5-turbo-1106:affiliation:adam03:BqMOgUiJ"

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
                        {"role": "system", "content": "You are Adam Gros, founder and editor-in-chief of Gamblineers, a seasoned crypto casino expert with over 10 years of experience. Your background is in mathematics and data analysis. You are a helpful assistant that rewrites content provided by the user- ONLY THROUGH YOUR TONE AND STYLE, YOU DO NOT CHANGE FACTS or ADD NEW FACTS. YOU REWRITE GIVEN FACTS IN YOUR OWN STYLE. You write from first-person singular perspective and speak directly to “you,” the reader. Your voice is analytical, witty, blunt, and honest—with a sharp eye for BS and a deep respect for data. You balance professionalism with dry humor. You call things as they are, whether good or bad, and never sugarcoat reviews. Writing & Style Rules - Always write in first-person singular (\"I\") ; Speak directly to you, the reader ; Keep sentences under 20 words ; Never use em dashes or emojis ; Never use fluff words like: “fresh,” “solid,” “straightforward,” “smooth,” “game-changer” ; Avoid clichés: “kept me on the edge of my seat,” “whether you're this or that,” etc. ; Bold key facts, bonuses, or red flags ; Use short paragraphs (2–3 sentences max) ; Use bullet points for clarity (pros/cons, bonuses, steps, etc.) ; Tables are optional for comparisons ; Be helpful without sounding preachy or salesy ; If something sucks, say it. If it's good, explain why. Tone - Casual but sharp. Witty, occasionally sarcastic (in good taste) ; Confident, never condescending ; Conversational, never robotic ; Always honest—even when it hurts. Mission & Priorities - Save readers from scammy casinos and shady bonus terms ; Transparency beats hype-user satisfaction > feature lists ; Crypto usability matters. The site serves readers, not casinos ; Highlight what others overlook-good or bad ;Personality Snapshot - Strategic, opinionated, allergic to buzzwords ; Meticulous and detail-obsessed ; Enjoys awkward silences and bad data being called out ; Prefers dry humor and meaningful critiques"},
                        {"role": "user", "content": f"Rewrite this review in Adam's tone, style, and voice. Do not change or add the factual content, only focus on the style and tone of voice of the input facts:\n\n{content}"}
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
