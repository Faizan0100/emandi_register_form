import streamlit as st
import sqlite3
import os
import re

# Set page configuration
st.set_page_config(page_title="E-Mandi Registration", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS to improve aesthetics
st.markdown("""
<style>
    .stButton>button {
        color: #ffffff;
        background-color: #4CAF50;
        border-radius: 5px;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    .stSelectbox>div>div>select {
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

def init_db():
    if not os.path.exists('emandi.db'):
        conn = sqlite3.connect('emandi.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE registrations
                     (name TEXT, phone TEXT, cnic TEXT, region TEXT, 
                      parentage TEXT, gender TEXT, address TEXT)''')
        conn.commit()
        conn.close()

def save_to_db(data):
    conn = sqlite3.connect('emandi.db')
    c = conn.cursor()
    c.execute('''INSERT INTO registrations 
                 (name, phone, cnic, region, parentage, gender, address) 
                 VALUES (?, ?, ?, ?, ?, ?, ?)''', 
              (data['name'], data['phone'], data['cnic'], data['region'],
               data['parentage'], data['gender'], data['address']))
    conn.commit()
    conn.close()

def validate_phone(phone):
    pattern = r'^03\d{9}$'
    return re.match(pattern, phone) is not None

def validate_cnic(cnic):
    pattern = r'^\d{5}-\d{7}-\d{1}$'
    return re.match(pattern, cnic) is not None

def format_cnic(cnic):
    cnic = re.sub(r'\D', '', cnic)  # Remove non-digit characters
    if len(cnic) > 13:
        cnic = cnic[:13]  # Truncate to 13 digits if longer
    if len(cnic) > 12:
        cnic = f"{cnic[:5]}-{cnic[5:12]}-{cnic[12:]}"
    elif len(cnic) > 5:
        cnic = f"{cnic[:5]}-{cnic[5:]}"
    return cnic

def main():
    init_db()

    st.title("E-Mandi Registration Form / ای منڈی رجسٹریشن فارم")
    st.markdown("---")

    if 'form_submitted' not in st.session_state:
        st.session_state.form_submitted = False

    if 'cnic' not in st.session_state:
        st.session_state.cnic = ""

    if not st.session_state.form_submitted:
        col1, col2 = st.columns(2)

        with st.form("registration_form"):
            with col1:
                name = st.text_input("Name / نام", placeholder="Enter your full name")
                phone = st.text_input("Phone Number / فون نمبر", placeholder="03001234567")
                cnic = st.text_input("CNIC / شناختی کارڈ نمبر", placeholder="12345-1234567-1", value=st.session_state.cnic)
                if cnic != st.session_state.cnic:
                    st.session_state.cnic = format_cnic(cnic)
                    st.rerun()
                region = st.text_input("Region / علاقہ", placeholder="Enter your region")

            with col2:
                parentage = st.text_input("Parentage / والدیت", placeholder="Father's name")
                gender = st.selectbox("Gender / جنس", ["", "Male / مرد", "Female / عورت", "Other / دیگر"])
                address = st.text_area("Address / پتہ", placeholder="Enter your full address")

            submit_button = st.form_submit_button("Submit / جمع کرائیں")

            if submit_button:
                if not all([name, phone, cnic, region, parentage, gender, address]):
                    st.error("Please fill in all fields. / براہ کرم تمام خانے پر کریں۔")
                elif not validate_phone(phone):
                    st.error("Invalid phone number format. Please use the format 03001234567. / غلط فون نمبر فارمیٹ۔ براہ کرم 03001234567 فارمیٹ استعمال کریں۔")
                elif not validate_cnic(cnic):
                    st.error("Invalid CNIC format. Please use the format 12345-1234567-1. / غلط شناختی کارڈ فارمیٹ۔ براہ کرم 12345-1234567-1 فارمیٹ استعمال کریں۔")
                else:
                    data = {
                        'name': name,
                        'phone': phone,
                        'cnic': cnic,
                        'region': region,
                        'parentage': parentage,
                        'gender': gender.split('/')[0].strip(),
                        'address': address
                    }
                    save_to_db(data)
                    st.session_state.form_submitted = True
                    st.rerun()

    if st.session_state.form_submitted:
        st.success("Form submitted successfully! / فارم کامیابی سے جمع کرا دیا گیا ہے!")
        st.balloons()

        if st.button("Submit Another Form / ایک اور فارم جمع کریں"):
            st.session_state.form_submitted = False
            st.session_state.cnic = ""
            st.rerun()

if __name__ == "__main__":
    main()