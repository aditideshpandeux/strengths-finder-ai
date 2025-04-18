import streamlit as st
import openai

# --- Page Setup ---
st.set_page_config(page_title="Strengths Finder AI", page_icon="🌟")
st.title("🌟 Strengths Finder AI")
st.markdown("Answer the questions using keywords or short phrases. Choose your favorite tone, then click the button to discover your strengths! 💪")

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
        "Friendly", "Poetic", "Humorous", "Deep Insightful",
        "Bugs Bunny", "Victorian British", "Filmy"
    ])

    
    submitted = st.form_submit_button("✨ Find My Strengths")
    
openai_api_key = st.secrets["OPENAI_API_KEY"]


# --- Tone Style Mapping ---
tone_styles = {
    "Friendly": "a friendly and supportive career coach",
    "Poetic": "a poetic soul who sees beauty in human potential",
    "Humorous": "a witty coach who uses humor to uplift",
    "Deep Insightful": "a philosophical guide with reflective insights",
    "Bugs Bunny": "Bugs Bunny with wisecracks and street smarts",
    "Victorian British": "a proper Victorian-era British life coach",
    "Filmy": "a dramatic Bollywood-style motivator with flair"
}

# --- Generate Response ---
if submitted:
    if not openai_api_key:
        st.error("Please enter your OpenAI API key.")
    else:
        with st.spinner("Analyzing your hidden brilliance... 🧠✨"):
            openai.api_key = openai_api_key

            system_tone = tone_styles.get(tone, "a friendly coach")

            prompt = f"""
You are {system_tone}. Based on the user's short keyword-style answers, identify their top 3 strengths with short explanations, suggest 2-3 career or personal growth paths where these strengths would shine, and offer a motivational reflection in the selected tone.

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
                        {"role": "system", "content": f"You are {system_tone}."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.9
                )

                output = response['choices'][0]['message']['content']
                st.markdown("---")
                st.subheader("🔍 Here's what I see in you:")
                st.write(output)

            except Exception as e:
                st.error(f"Something went wrong: {e}")
