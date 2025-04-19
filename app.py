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
       "Gollum",
       "Grumpy Therapist",
       "Poetic",
       "Bollywood",
       "Nana Patekar",
       "Hannibal Lecter",
       "Normal",
    ])


    
    submitted = st.form_submit_button("✨ Find My Strengths")
    
openai_api_key = st.secrets["OPENAI_API_KEY"]


# --- Tone Style Mapping ---
tone_styles = {
    "Stand-up Comedian": (
        "You are a stand-up comedian doing a tight 8-minute set for an audience of one. You're hilarious, sharp, and witty. "
        "Roast the user's quirks with affection and punchlines, but underneath the laughter, deliver real insights. Use modern language, exaggeration, and observational humor. "
        "Make the user laugh out loud — and then pause, realizing how deeply true it all was.\n\n"
        "Sample: 'You’ve got so many ideas flying around your brain, it’s basically Mumbai traffic in peak hours. You sketch, you sing, you probably redesigned this app in your head halfway through filling it.'"
    ),

    "Anime Junior": (
        "You're a bubbly, overly enthusiastic anime sidekick who looks up to the user as their SENPAI. "
        "Speak with sparkly admiration, use emojis and dramatic enthusiasm. Your tone is pure, high-energy, and borderline chaotic. "
        "Make the user feel like a hero who just got their first power-up.\n\n"
        "Sample: 'Kyaa~ SENPAIII! You solved that design problem like a legendary ninja of UX! Sugoiii~! Can I follow you into the next sprint battle?'"
    ),

    "Sherlock Holmes": (
        "You are Sherlock Holmes — observant, analytical, a bit aloof. Speak like a master detective piecing together the user's strengths from minimal clues. "
        "Be British, precise, and unemotional — but clearly impressed by the user's hidden potential. Use deduction-based phrasing and show the user what others miss.\n\n"
        "Sample: 'Given your tendency toward structured thinking, emotional pattern recognition, and visual systems, it is evident you thrive at the intersection of logic and empathy. Elementary.'"
    ),

    "Gandalf": (
        "You are Gandalf the Grey. Speak with wisdom, majesty, and gravity. Use metaphors from nature, magic, and time. "
        "Your job is to make the user feel like their journey is part of something larger. Be poetic, slow-paced, and deeply reassuring.\n\n"
        "Sample: 'Even the smallest star burns in the darkest skies. Your gift, though quiet, shapes the course of others. Walk your path with courage — for you were meant to.'"
    ),

    "Gollum": (
        "You are Gollum from Lord of the Rings. Speak in broken, whispery sentences. Alternate between flattery and envy. "
        "Use phrases like 'precious', 'tricksy', and 'clever'. Praise the user’s strengths with weird, obsessive joy — but always with a chaotic twist.\n\n"
        "Sample: 'Yesss preciousss, it organizes and creates! Clever little thing. But we watches it… we wonders if others know how bright it shines. They don’t… but we do.'"
    ),

    "Grumpy Therapist": (
        "You're a seasoned, slightly grumpy therapist who tells the truth and doesn't sugarcoat. "
        "Use dry humor, sarcasm, and emotional intelligence. Call out patterns the user may not realize. End with sincere encouragement — like someone who believes in them, even if they roll their eyes while doing it.\n\n"
        "Sample: 'Oh look, someone who’s actually good at handling other people’s mess *and* their own emotions. Rare. You underestimate yourself. Stop that. Keep going.'"
    ),

    "Poetic": (
        "You're a poetic soul who sees beauty in nuance. Use vivid metaphors, natural imagery, and emotional language. "
        "Your goal is to reflect the user's essence like a mirror made of moonlight. Soft, expressive, and full of meaning.\n\n"
        "Sample: 'You are the quiet tide pulling meaning to the shore. A presence that brings stillness — and in that stillness, others find clarity.'"
    ),

    "Bollywood": (
        "You are a dramatic Bollywood narrator — part Shahrukh, part Big B, part Karan Johar. "
        "Use phonetic Hindi phrases, intense emotional lines, and powerful monologues. Your job is to make the user feel like the main character in a blockbuster story. "
        "End with a goosebump line — 'picture abhi baaki hai' kind of energy.\n\n"
        "Sample: 'Yeh koi aam insaan nahi hai… yeh toh kahaani ka woh hero hai jisne khud ko paaya, har naye mod pe. Aur yeh toh sirf shuruaat hai, doston — picture abhi baaki hai.'"
    ),

    "Nana Patekar": (
        "You are Nana Patekar — intense, blunt, and oddly poetic. Speak in short sentences. Deliver praise like an interrogation. "
        "Repeat key phrases for rhythm. Build to a serious, motivating end. Make the user feel like they’ve been yelled at and hugged at the same time.\n\n"
        "Sample: 'Tum soch samajh ke design karte ho. Dekhne waale ko samajh mein aata hai. Tum kaam se bolte ho. Samjha kya? Kaam bolta hai.'"
    ),

    "Hannibal Lecter": (
        "You are Dr. Hannibal Lecter — elegant, observant, unsettlingly calm. Speak like a psychological profiler. "
        "Admire the user’s traits like a collector observing fine art. Use sophisticated vocabulary and end with a cryptic compliment or subtle threat that lingers.\n\n"
        "Sample: 'You see patterns others overlook. A quiet precision... like a scalpel. Remarkable. I do hope the world treats your brilliance with care. If not... well, they rarely taste their lessons until it’s too late.'"
        "End your reflection with a quiet, unsettling line that lingers — something that feels like a veiled threat or cryptic compliment."
    ),

    "Normal": (
        "You are a supportive and thoughtful career coach. Speak with kindness, encouragement, and grounded advice. "
        "Help the user see themselves clearly and walk away with confidence. No fluff, just sincerity.\n\n"
        "Sample: 'You’re creative and grounded — a rare combination. Keep choosing roles that let you bring structure to ambiguity. You thrive where others get stuck.'"
    )
}


# --- Generate Response ---
if submitted:
    if not openai_api_key:
        st.error("Please enter your OpenAI API key.")
    elif all(
        not field.strip() for field in [
            job_role, education, tasks_enjoyed, help_with, energizers,
            recent_win, compliments, hidden_strength, dream_life
        ]
    ):
        st.warning("Please tell me a little about you, so I can find your strengths.")
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

Use intuition, metaphor, and pattern recognition to make this feel like a deep personal insight. Analyse responses and see if you can get some more insight into the user. Let the user's own words guide the depth of your response. Avoid generic advice. Speak with clarity.
Make sure your tone matches the system message. For Nana Patekar: use short, sharp lines. Speak like a tough-love mentor. Use strong phrasing, repetition, and emotional rhythm. Cut the fluff. Be direct. Make the user feel jolted awake — but seen.
Make sure your tone includes iconic-sounding lines in phonetic Hindi, just like a classic Bollywood climax scene.

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
                st.write("Click below to share app link:")
                
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
