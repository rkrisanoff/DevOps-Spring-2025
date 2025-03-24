import streamlit as st

# Initialize session state to store our "database"
if "database" not in st.session_state:
    st.session_state.database = {}


def simulate_get_api():
    """Simulate GET request by returning data from session state"""
    return st.session_state.database


def simulate_post_api(name: str, phone: str):
    """Simulate POST request by storing data in session state"""
    st.session_state.database[name] = phone
    return {"status": "success", "message": f"Added {name} with phone {phone}"}


# App title
st.title("Contact Management App")

# Input section
st.header("Add New Contact")
with st.form(key="contact_form", clear_on_submit=True):
    name_input = st.text_input("Name", key="name")
    phone_input = st.text_input("Phone Number", key="phone")

    # Form submission buttons
    submit_button = st.form_submit_button("Add Contact")

    if submit_button:
        if name_input and phone_input:
            result = simulate_post_api(name_input, phone_input)
            st.success(result["message"])
        else:
            st.error("Please fill in both name and phone number")

# GET section
st.header("View All Contacts")
if st.button("Refresh Contacts"):
    contacts = simulate_get_api()
    if contacts:
        # Convert the contacts dictionary to a list of dictionaries for the dataframe
        contact_list = [{"Name": name, "Phone": phone} for name, phone in contacts.items()]
        st.table(contact_list)
    else:
        st.info("No contacts found")
