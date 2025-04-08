import streamlit as st
import os
from groq import Client
from dotenv import load_dotenv


#Load api key
load_dotenv()
groq_api_key=os.getenv("GROQ_API_KEY")

#Connect to groq ai
client=Client(api_key=groq_api_key)

## main logic
def explain_concept(concept, level="elementary"):
    # what the ai will do
    prompt = f"""
    Explain '{concept}' to a {level} school student.

    Please:
    1. Use simple words
    2. Include a real-world example
    3. Use an analogy (comparing it to something familiar)
    4. Add a fun fact if possible
    5. Keep it under 200 words
    """
    # Ask groq ai for an explanation
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a friendly teacher who explains concepts in simple, fun ways."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    # get answer
    return completion.choices[0].message.content

#create a webapage using streamlit
st.title('Explains Intuitively')
st.write('Hi i can explain anything to you in a simple and most intuitive way')
##input box for the user
concept=st.text_input("What concept would you like me to explain")
level=st.selectbox("What level would you like it",["Basic","Middle","High"])

# a button to get explanations
if st.button("Explain this"):
    if concept:
        st.spinner("Thinking...")
        explanation = explain_concept(concept, level)
        st.write("### Here's your explanation:")
        st.write(explanation)
    else:
        st.error("Please enter a concept!!!") # Changed print to st.error for better UI feedback


# save past explanations
if 'history' not in st.session_state:
    st.session_state.history = []

# show prev explanations
if st.session_state.history:
    st.write("### Previous explanations:")
    for item in st.session_state.history:
        st.write(f"**{item['concept']}**")
        st.write(item['explanation'])
        st.write("---")

# Save current explanation to history
if st.button("Save this explanation"):
    if 'explanation' in locals() and explanation: # Check if explanation exists and is not empty
        st.session_state.history.append({
            "concept": concept,
            "explanation": explanation
        })
        st.success("Saved!")
