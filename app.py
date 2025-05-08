import streamlit as st

st.title("Personalized Recommendation System")
st.write("Enter your preferences (e.g., 'I like sci-fi movies with strong female leads')")
user_query = st.text_input("Your preferences:")
if st.button("Get Recommendations"):
    if user_query:
        st.write("### Recommendations")
        st.write(f"You entered: {user_query}")
    else:
        st.write("Please enter a query.")