import streamlit as st
import google.generativeai as genai
# ============ Gemini Setup ============
# NOTE: For security, never expose API keys directly in deployed apps.
genai.configure(api_key=st.secrets["apikey"])
model = genai.GenerativeModel("gemini-2.5-flash")
st.set_page_config(page_title="Financial Learning Helper")
st.title("Financial Learning Helper")
st.markdown("This app helps you personalize your financial learning experience.")
# Sidebar for game navigation
st.sidebar.title(":video_game: Mini-Games")
game_choice = st.sidebar.selectbox("Choose a game", ["Home", "Scenario Simulator", "Budget Slider Game", "Needs vs. Wants"])
# Home page with user info
if game_choice == "Home":
    with st.form("user_info_form"):
        st.header(":clipboard: Personal and Financial Information")
        name = st.text_input("Your Name")
        age = st.text_input("Your Age")
        allowance = st.number_input("Monthly Allowance ($)", min_value=0, step=10)
        expenses = st.text_input("Fixed Expenses (comma-separated)")
        preferred_learning_style = st.selectbox("Preferred Learning Style", ["Visual", "Auditory", "Reading/Writing", "Kinesthetic"])
        preferred_lesson_length = st.selectbox("Preferred Lesson Length", ["Short (5-10 min)", "Medium (10-20 min)", "Long (20+ min)"])
        biggest_goal = st.text_input("What's your biggest financial goal?")
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.success(f"Thanks {name}, you're all set! Choose a game from the sidebar to start learning.")
# ========== Game 1: Scenario Simulator ==========
elif game_choice == "Scenario Simulator":
    if "step" not in st.session_state:
        st.session_state.step = 1
        st.session_state.savings = 0
    st.header(":moneybag: Scenario Simulator")
    st.write("Make smart choices and track your savings!")
    if st.session_state.step == 1:
        st.subheader("You found $20 on the sidewalk. What do you do?")
        choice = st.radio("Choose one:", ["Save it", "Buy snacks", "Give it away"])
        if st.button("Next"):
            if choice == "Save it":
                st.session_state.savings += 20
            elif choice == "Give it away":
                st.session_state.savings += 5
            st.session_state.step += 1
            st.rerun()
    elif st.session_state.step == 2:
        st.subheader("Your friend invites you to the movies ($15). You have $20.")
        choice = st.radio("Do you go?", ["Yes, go to the movie", "No, save the money"])
        if st.button("Next"):
            if choice == "No, save the money":
                st.session_state.savings += 15
            st.session_state.step += 1
            st.rerun()
    elif st.session_state.step == 3:
        st.subheader("You get $10 for doing chores. What do you do with it?")
        choice = st.radio("Choose one:", ["Spend half, save half", "Save it all", "Buy candy"])
        if st.button("See Results"):
            if choice == "Spend half, save half":
                st.session_state.savings += 5
            elif choice == "Save it all":
                st.session_state.savings += 10
            st.session_state.step += 1
            st.rerun()
    elif st.session_state.step == 4:
        st.success("Game Over!")
        st.metric(label="Total Savings", value=f"${st.session_state.savings}")
        if st.session_state.savings >= 40:
            st.balloons()
            st.write(":tada: Amazing! You're a smart saver.")
        elif st.session_state.savings >= 20:
            st.write(":+1: Nice job. You're learning to make better choices!")
        else:
            st.write(":bulb: It's okay to have fun, but remember to save too!")
        if st.button("Play Again"):
            st.session_state.step = 1
            st.session_state.savings = 0
            st.rerun()
# ========== Game 2: Budget Slider Game ==========
elif game_choice == "Budget Slider Game":
    st.header(":bar_chart: Budget Slider Game")
    st.write("You have $1000 to allocate. Use the sliders to create your monthly budget.")
    rent = st.slider("Rent", 0, 1000, 500, 50)
    food = st.slider("Food", 0, 1000, 200, 50)
    fun = st.slider("Fun", 0, 1000, 100, 50)
    savings = st.slider("Savings", 0, 1000, 200, 50)
    total = rent + food + fun + savings
    st.write(f"**Total Allocated:** ${total}")
    if total > 1000:
        st.error(":no_entry_sign: You're over budget! Adjust your sliders.")
    elif total < 1000:
        st.warning(":warning: You haven't used your full budget. Consider saving more!")
    else:
        score = 0
        if 400 <= rent <= 600: score += 1
        if 100 <= food <= 250: score += 1
        if savings >= 100: score += 1
        st.success(":white_check_mark: Perfectly balanced!")
        st.write(f"**Score:** {score}/3")
# ========== Game 3: Needs vs. Wants ==========
elif game_choice == "Needs vs. Wants":
    st.header(":brain: Needs vs. Wants Sorter")
    st.write("Sort each item into 'Need' or 'Want' and test your judgment!")
    items = {
        "Groceries": "Need",
        "New Video Game": "Want",
        "Toothpaste": "Need",
        "Concert Ticket": "Want",
        "School Supplies": "Need"
    }
    correct = 0
    for item, correct_answer in items.items():
        choice = st.radio(f"{item} is a...", ["Need", "Want"], key=item)
        if choice == correct_answer:
            correct += 1
    if st.button("Check Answers"):
        st.write(f"You got {correct} out of {len(items)} correct.")
        if correct == len(items):
            st.balloons()
            st.success(":tada: Perfect! You really know your priorities.")
        elif correct >= 3:
            st.success(":+1: Great job! You're on the right track.")
        else:
            st.info(":bulb: Keep practicing! Needs come before wants when budgeting.")
