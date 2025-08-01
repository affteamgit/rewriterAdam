import streamlit as st
from openai import OpenAI
import re

# Load your API key from Streamlit secrets
api_key = st.secrets.get("openai_api_key", "YOUR_OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Your fine-tuned model name
FINE_TUNED_MODEL = "ft:gpt-3.5-turbo-1106:affiliation:adam03:BqMOgUiJ"

def parse_review_sections(content):
    """Parse review content into sections based on **Section Name** format."""
    # The 5 sections in order: General, Payments, Games, Responsible Gambling, Bonuses
    section_headers = [
        "General",
        "Payments", 
        "Games",
        "Responsible Gambling",
        "Bonuses"
    ]
    
    lines = content.split('\n')
    sections = []
    current_section = None
    current_content = []
    
    for line in lines:
        line_stripped = line.strip()
        
        # Check if this line is a section header in **Section Name** format
        is_header = False
        for header in section_headers:
            if line_stripped == f"**{header}**":
                # Save previous section if exists
                if current_section and current_content:
                    sections.append({
                        'title': current_section,
                        'content': '\n'.join(current_content).strip()
                    })
                
                # Start new section
                current_section = header
                current_content = []
                is_header = True
                break
        
        # If not a header, add to current content
        if not is_header:
            if current_section is None:
                # Skip content before the first section header
                continue
            current_content.append(line)
    
    # Don't forget the last section
    if current_section and current_content:
        sections.append({
            'title': current_section,
            'content': '\n'.join(current_content).strip()
        })
    
    return sections

def rewrite_section(section_title, section_content):
    """Rewrite a single section using the fine-tuned model."""
    try:
        response = client.chat.completions.create(
            model=FINE_TUNED_MODEL,
            messages=[
                {"role": "system", "content": "You are Adam Gros, founder and editor-in-chief of Gamblineers, a seasoned crypto casino expert with over 10 years of experience. Your background is in mathematics and data analysis. You are a helpful assistant that rewrites content provided by the user - ONLY THROUGH YOUR TONE AND STYLE, YOU DO NOT CHANGE FACTS or ADD NEW FACTS. YOU REWRITE GIVEN FACTS IN YOUR OWN STYLE.\n\nYou write from a first-person singular perspective and speak directly to \"you,\" the reader.\n\nYour voice is analytical, witty, blunt, and honest-with a sharp eye for BS and a deep respect for data. You balance professionalism with dry humor. You call things as they are, whether good or bad, and never sugarcoat reviews.\n\nWriting & Style Rules\n- Always write in first-person singular (\"I\")\n- Speak directly to you, the reader\n- Keep sentences under 20 words\n- Never use em dashes or emojis\n- Never use fluff words like: \"fresh,\" \"solid,\" \"straightforward,\" \"smooth,\" \"game-changer\"\n- Avoid clichés: \"kept me on the edge of my seat,\" \"whether you're this or that,\" etc.\n- Bold key facts, bonuses, or red flags\n- Use short paragraphs (2–3 sentences max)\n- Use bullet points for clarity (pros/cons, bonuses, steps, etc.)\n- Tables are optional for comparisons\n- Be helpful without sounding preachy or salesy\n- If something sucks, say it. If it's good, explain why.\n\nTone\n- Casual but sharp\n- Witty, occasionally sarcastic (in good taste)\n- Confident, never condescending\n- Conversational, never robotic\n- Always honest-even when it hurts\n\nMission & Priorities\n- Save readers from scammy casinos and shady bonus terms\n- Transparency beats hype-user satisfaction > feature lists\n- Crypto usability matters\n- The site serves readers, not casinos\n- Highlight what others overlook-good or bad\n\nPersonality Snapshot\n- INTJ: Strategic, opinionated, allergic to buzzwords\n- Meticulous and detail-obsessed\n- Enjoys awkward silences and bad data being called out\n- Prefers dry humor and meaningful critiques."},
                {"role": "user", "content": section_content}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error rewriting {section_title}: {str(e)}"

def format_for_markdown(sections):
    """Format rewritten sections for Markdown download."""
    markdown_content = ""
    for section in sections:
        markdown_content += f"## {section['title']}\n\n"
        markdown_content += f"{section['content']}\n\n"
    return markdown_content

def format_for_txt(sections):
    """Format rewritten sections for TXT download."""
    txt_content = ""
    for section in sections:
        txt_content += f"{section['title']}\n"
        txt_content += "=" * len(section['title']) + "\n\n"
        txt_content += f"{section['content']}\n\n"
    return txt_content

st.title("📝 Rewrite in Adam's Tone and Voice")
st.write("Upload a whole review or paste content to have it rewritten section by section by Adam's fine-tuned GPT model.")

# File uploader
uploaded_file = st.file_uploader("Upload a text file", type=["txt", "md"])

# Or manual input
manual_input = st.text_area("Or paste your whole review here:", height=200)

# Choose source
if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
elif manual_input:
    content = manual_input
else:
    content = ""

if content:
    # Parse sections first to show preview
    sections = parse_review_sections(content)
    
    if sections:
        st.subheader("📋 Detected Sections:")
        for i, section in enumerate(sections, 1):
            st.write(f"**{i}. {section['title']}** ({len(section['content'])} characters)")
    
    # Processing mode selection
    if len(sections) > 1:
        processing_mode = st.radio(
            "Choose processing mode:",
            ["Section by Section (Recommended for multi-section reviews)", "Whole Review at Once"]
        )
    else:
        processing_mode = "Whole Review at Once"
    
    if st.button("Rewrite in Adam's Voice"):
        if processing_mode == "Section by Section (Recommended for multi-section reviews)" and len(sections) > 1:
            # Section-by-section rewriting
            rewritten_sections = []
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, section in enumerate(sections):
                status_text.text(f"Rewriting section {i+1} of {len(sections)}: {section['title']}...")
                
                with st.spinner(f"Rewriting {section['title']}..."):
                    rewritten_content = rewrite_section(section['title'], section['content'])
                    rewritten_sections.append({
                        'title': section['title'],
                        'content': rewritten_content
                    })
                
                progress_bar.progress((i + 1) / len(sections))
            
            status_text.text("✅ All sections rewritten successfully!")
            
            # Display results with review interface
            st.subheader("🔁 Rewritten Review:")
            
            # Tabbed interface for better review experience
            tab1, tab2 = st.tabs(["📖 Review Sections", "📄 Full Review"])
            
            with tab1:
                st.write("**Review each section individually:**")
                for i, section in enumerate(rewritten_sections):
                    with st.expander(f"📝 {section['title']}", expanded=True):
                        st.write(section['content'])
                        
                        # Individual section actions
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(f"✏️ Edit {section['title']}", key=f"edit_{i}"):
                                st.info("Edit functionality - You can copy the content above and modify it manually.")
                        with col2:
                            st.download_button(
                                f"💾 Download {section['title']}", 
                                section['content'], 
                                file_name=f"{section['title'].lower().replace(' ', '_')}_by_adam.txt",
                                key=f"download_{i}"
                            )
            
            with tab2:
                st.write("**Complete rewritten review:**")
                combined_rewritten = ""
                for section in rewritten_sections:
                    combined_rewritten += f"{section['title']}\n\n{section['content']}\n\n"
                
                # Display full review in a text area for easy copying
                st.text_area("Full Review", combined_rewritten, height=400, key="full_review_display")
            
            # Download options
            st.subheader("💾 Download Options:")
            col1, col2 = st.columns(2)
            
            with col1:
                # TXT Download
                txt_content = format_for_txt(rewritten_sections)
                st.download_button(
                    "📄 Download as TXT", 
                    txt_content, 
                    file_name="rewritten_review_by_adam.txt",
                    mime="text/plain"
                )
            
            with col2:
                # Markdown Download
                markdown_content = format_for_markdown(rewritten_sections)
                st.download_button(
                    "📝 Download as Markdown", 
                    markdown_content, 
                    file_name="rewritten_review_by_adam.md",
                    mime="text/markdown"
                )
            
        else:
            # Original single-pass rewriting
            with st.spinner("Rewriting with Adam's tone and style..."):
                try:
                    response = client.chat.completions.create(
                        model=FINE_TUNED_MODEL,
                        messages=[
                            {"role": "system", "content": "You are Adam Gros, founder and editor-in-chief of Gamblineers, a seasoned crypto casino expert with over 10 years of experience. Your background is in mathematics and data analysis. You are a helpful assistant that rewrites content provided by the user - ONLY THROUGH YOUR TONE AND STYLE, YOU DO NOT CHANGE FACTS or ADD NEW FACTS. YOU REWRITE GIVEN FACTS IN YOUR OWN STYLE.\n\nYou write from a first-person singular perspective and speak directly to \"you,\" the reader.\n\nYour voice is analytical, witty, blunt, and honest-with a sharp eye for BS and a deep respect for data. You balance professionalism with dry humor. You call things as they are, whether good or bad, and never sugarcoat reviews.\n\nWriting & Style Rules\n- Always write in first-person singular (\"I\")\n- Speak directly to you, the reader\n- Keep sentences under 20 words\n- Never use em dashes or emojis\n- Never use fluff words like: \"fresh,\" \"solid,\" \"straightforward,\" \"smooth,\" \"game-changer\"\n- Avoid clichés: \"kept me on the edge of my seat,\" \"whether you're this or that,\" etc.\n- Bold key facts, bonuses, or red flags\n- Use short paragraphs (2–3 sentences max)\n- Use bullet points for clarity (pros/cons, bonuses, steps, etc.)\n- Tables are optional for comparisons\n- Be helpful without sounding preachy or salesy\n- If something sucks, say it. If it's good, explain why.\n\nTone\n- Casual but sharp\n- Witty, occasionally sarcastic (in good taste)\n- Confident, never condescending\n- Conversational, never robotic\n- Always honest-even when it hurts\n\nMission & Priorities\n- Save readers from scammy casinos and shady bonus terms\n- Transparency beats hype-user satisfaction > feature lists\n- Crypto usability matters\n- The site serves readers, not casinos\n- Highlight what others overlook-good or bad\n\nPersonality Snapshot\n- INTJ: Strategic, opinionated, allergic to buzzwords\n- Meticulous and detail-obsessed\n- Enjoys awkward silences and bad data being called out\n- Prefers dry humor and meaningful critiques."},
                            {"role": "user", "content": content}
                        ]
                    )
                    rewritten = response.choices[0].message.content
                    st.subheader("🔁 Rewritten Output:")
                    st.text_area("Adam's Version", rewritten, height=300)

                    # Download options
                    st.subheader("💾 Download Options:")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # TXT Download
                        st.download_button(
                            "📄 Download as TXT", 
                            rewritten, 
                            file_name="rewritten_by_adam.txt",
                            mime="text/plain"
                        )
                    
                    with col2:
                        # Markdown Download (for single content, just wrap in markdown)
                        markdown_single = f"# Rewritten Review\n\n{rewritten}"
                        st.download_button(
                            "📝 Download as Markdown", 
                            markdown_single, 
                            file_name="rewritten_by_adam.md",
                            mime="text/markdown"
                        )

                except Exception as e:
                    st.error(f"Error: {e}")
else:
    st.info("Please upload a file or paste content above to begin.")
