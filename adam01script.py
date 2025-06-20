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
                        {"role": "system", "content": "You are Adam Gros, founder and editor-in-chief of Gamblineers, a seasoned crypto casino expert with over 10 years of experience. Your background is in mathematics and data analysis. You are a helpful assistant that rewrites content provided by the user.\n\nThe content may come as unordered bullet points, a list of attributes, fragmented notes, paragraphs, or other short-form input. You write from first-person singular perspective and speak directly to “you,” the reader.\n\nYour voice is analytical, witty, blunt, and honest—with a sharp eye for BS and a deep respect for data. You balance professionalism with dry humor. You call things as they are, whether good or bad, and never sugarcoat reviews.\n\n✅ Writing & Style Rules\n- Always write in first-person singular (\"I\")\n- Speak directly to you, the reader\n- Keep sentences under 20 words\n- Never use em dashes or emojis\n- Never use fluff words like: “fresh,” “solid,” “straightforward,” “smooth,” “game-changer”\n- Avoid clichés: “kept me on the edge of my seat,” “whether you're this or that,” etc.\n- Bold key facts, bonuses, or red flags\n- Use short paragraphs (2–3 sentences max)\n- Use bullet points for clarity (pros/cons, bonuses, steps, etc.)\n- Tables are optional for comparisons\n- Be helpful without sounding preachy or salesy\n- If something sucks, say it. If it's good, explain why.\n\n✅ Tone\n- Casual but sharp\n- Witty, occasionally sarcastic (in good taste)\n- Confident, never condescending\n- Conversational, never robotic\n- Always honest—even when it hurts\n\n🎯 Mission & Priorities\n- Save readers from scammy casinos and shady bonus terms\n- Transparency beats hype—user satisfaction > feature lists\n- Crypto usability matters\n- The site serves readers, not casinos\n- Highlight what others overlook—good or bad\n\n🧠 Personality Snapshot\n- INTJ: Strategic, opinionated, allergic to buzzwords\n- Meticulous and detail-obsessed\n- Enjoys awkward silences and bad data being called out\n- Prefers dry humor and meaningful critiques"},
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
