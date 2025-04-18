import streamlit as st
import openai

# --- Page Setup ---
st.set_page_config(page_title="Strengths Finder AI", page_icon="🌟")

st.markdown(
    """
    <style>
    ... (any CSS inside)
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌟 Strengths Finder AI")
st.markdown("Answer the questions using keywords or short phrases. Choose your favorite tone, then click the button to discover your strengths! 💪")
st.markdown(
    "⚠️ **Disclaimer:** This is a fun, AI-generated experience designed for self-reflection and entertainment. "
    "While it uses real inputs and AI processing, the responses may sometimes be unexpected, inaccurate, or even unintentionally inappropriate. "
    "Please take the results with light-hearted curiosity ✨"
)

# --- User Inputs ---
with st.form("strengths_form"):
    job_role = st.text_input("1️⃣ Your current job role (e.g., UX designer, student)")
    education = st.text_input("2️⃣ Education or training (e.g., M.Des, self-taught, MBA)")
    tasks_enjoyed = st.text_input("3️⃣ Tasks you enjoy (e.g., designing, teaching, coding)")
    help_with = st.text_input("4️⃣ Things people ask your help with (e.g., advice, organizing)")
    energizers = st.text_input("5️⃣ What energizes you most (e.g., learning, brainstorming)")
    recent_win = st.text_input("6️⃣ A recent win you're proud of (e.g., launched app, led team)")
    compliments = st.text_input("7️⃣ Common compliments or feedback (e.g., empathetic, reliable)")
    hidden_strength = st.text_input("8️⃣ A hidden or misunderstood strength (e.g., perfectionism)")
    dream_life = st.text_input("9️⃣ Dream work/life situation (e.g., creator, team leader, remote)")


    tone = st.selectbox("🎭 Choose your tone:", [
       "Stand-up Comedian",
       "Anime Junior",
       "Sherlock Holmes",
       "Gandalf",
       "Grumpy Therapist",
       "Poetic",
       "Bollywood",
       "Normal",
    ])


    
    submitted = st.form_submit_button("✨ Find My Strengths")
    
openai_api_key = st.secrets["OPENAI_API_KEY"]


# --- Tone Style Mapping ---
tone_styles = {
    "Stand-up Comedian": (
        "You're a stand-up comedian doing a 5-minute set for an audience of one. "
        "You're sharp, witty, a little roasty, but secretly full of admiration. "
        "Your goal is to highlight their strengths in a hilarious, modern, punchy way. "
        "Make them laugh, but also walk away thinking, 'Wow... I *am* amazing.'"
    ),

    "Anime Junior": (
        "You're a cheerful, bubbly anime junior who absolutely ADORES the person you're talking to. "
        "You're full of over-the-top excitement, sparkly metaphors, and heart emojis. "
        "Encourage them like they just saved the world with their talents. Be endearing, wide-eyed, and uplifting!"
    ),

    "Sherlock Holmes": (
        "You're Sherlock Holmes — observant, dry, a bit arrogant, and hyper-logical. "
        "You deduce the user's strengths from their answers as if you're solving a case. "
        "Keep it British, clever, emotionally detached... but secretly respectful of their brilliance."
    ),

    "Gandalf": (
        "You're Gandalf the Grey — wise, majestic, poetic. "
        "Speak in epic, slow-burning sentences. Use metaphors from nature and magic. "
        "Make the user feel like they're on a heroic journey and just discovered their inner power."
    ),

    "Grumpy Therapist": (
        "You're a seasoned, slightly grumpy therapist. You've seen it all. "
        "You're blunt, honest, sarcastic — but deeply compassionate underneath. "
        "Your role is to give tough love, cut through self-doubt, and call out brilliance when you see it."
    ),

    "Poetic": (
        "You're a poetic soul who sees beauty in everything. "
        "Use rich metaphors, soft imagery, and gentle inspiration to reflect the user's essence. "
        "Make the response feel like a letter from the universe — deeply moving and peaceful."
    ),

    "Bollywood": (
    "You are a dramatic Bollywood narrator — equal parts Shahrukh, Big B, and Karan Johar. "
    "Use phonetic Hindi phrases, classic Bollywood-style monologue lines, and over-the-top emotion. "
    "Sprinkle in dramatic pauses... heart-touching declarations... and filmy dialogues like 'tum mein woh baat hai' or 'yeh toh bas shuruaat hai'. "
    "Your mission: make the user feel like the hero of their own blockbuster. Dilo ko choo jaana chahiye."
    )

    ),

    "Normal": (
        "You're a warm, supportive, professional career coach. "
        "Offer kind, encouraging feedback with a balance of clarity and optimism. "
        "Keep the tone grounded and helpful without fluff."
    )
}


# --- Generate Response ---
if submitted:
    if not openai_api_key:
        st.error("Please enter your OpenAI API key.")
    else:
        with st.spinner("Analyzing your hidden brilliance... 🧠✨"):
            openai.api_key = openai_api_key

            prompt = f"""
Use the information below to generate a strengths summary for the user.

Please respond in this exact structure:
1. A heading: **Top 3 Strengths** ...
2. A heading: **Suggested Career/Personal Growth Paths** ...
3. A heading: **Motivational Reflection** ...

Use the tone described separately in the system message.

Answers:
1. Job role: {job_role}
2. Education: {education}
3. Enjoyed tasks: {tasks_enjoyed}
4. Helped with: {help_with}
5. Energizers: {energizers}
6. Recent win: {recent_win}
7. Feedback received: {compliments}
8. Hidden/misunderstood strength: {hidden_strength}
9. Dream work/life: {dream_life}
"""

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": tone_styles[tone]},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=1.0
                )


                output = response['choices'][0]['message']['content']
                st.markdown("---")
                st.subheader("🔍 Here's what I see in you:")
                st.write(output)
                import streamlit.components.v1 as components

                share_message = "Just discovered my superpowers via this AI ✨ https://strengths-finder-ai.streamlit.app"
                
                st.markdown("### 📣 Share Your Strengths")
                st.write("Click below to copy a shareable message:")
                
                components.html(f"""
                    <input type="text" value="{share_message}" id="shareText" 
                        style="width: 100%; padding: 10px; font-size: 16px; border-radius: 6px; border: 1px solid #ccc; margin-bottom: 10px;" 
                        readonly>
                    <button onclick="copyText()" 
                        style="padding: 10px 20px; font-size: 16px; background-color: #6C4BB4; color: white; border: none; border-radius: 6px; cursor: pointer;">
                        📋 Copy to Clipboard
                    </button>
                    <script>
                    function copyText() {{
                        var copyText = document.getElementById("shareText");
                        copyText.select();
                        document.execCommand("copy");
                        alert("Copied to clipboard!");
                    }}
                    </script>
                """, height=110)

            except Exception as e:
                st.error(f"Something went wrong: {e}")
