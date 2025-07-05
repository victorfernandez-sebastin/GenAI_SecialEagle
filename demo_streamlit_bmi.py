import streamlit as st

# Web page title
st.title("💪 BMI Calculator App")

# Input fields
name = st.text_input("Enter your name")
height = st.number_input("Enter your height (in meters)", format="%.2f")
weight = st.number_input("Enter your weight (in kilograms)", format="%.1f")

# Calculate BMI
if st.button("Calculate BMI"):
    if height > 0 and weight > 0:
        bmi = weight / (height ** 2)
        st.success(f"{name}, your BMI is: {bmi:.2f}")

        # Category message
        if bmi < 18.5:
            st.warning("You are underweight.")
        elif 18.5 <= bmi < 24.9:
            st.info("You have a normal weight.")
        elif 25 <= bmi < 29.9:
            st.warning("You are overweight.")
        else:
            st.error("You are obese.")
    else:
        st.error("Please enter valid height and weight.")
