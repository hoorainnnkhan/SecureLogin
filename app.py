
import streamlit as st
import secrets
import time

from database import create_table, register_user, get_user, check_password
from email_service import send_otp_email


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="SecureLogin | 2-Step Authentication",
    page_icon="🔐",
    layout="centered"
)

create_table()


# ---------------- CUSTOM DESIGN ----------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #080d20, #111b3b, #17113b);
    color: #f5f7ff;
}

.block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3, p, label {
    color: #f5f7ff !important;
}

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    background: linear-gradient(90deg, #45d6ff, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    color: #aebbd9 !important;
    font-size: 16px;
    margin-bottom: 30px;
}

.info-card {
    background: linear-gradient(135deg, #18264b, #252052);
    border: 1px solid #394b82;
    border-radius: 18px;
    padding: 25px;
    margin: 15px 0;
    text-align: center;
}

.info-card h2 {
    color: #55d9ff !important;
}

.info-card p {
    color: #d5dcf5 !important;
}

.stButton > button,
.stFormSubmitButton > button {
    background: linear-gradient(90deg, #087cf5, #7955ed);
    color: white !important;
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: bold;
    width: 100%;
    transition: 0.3s;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: linear-gradient(90deg, #7955ed, #08bde9);
    border: none;
    transform: scale(1.02);
}

.stTextInput input {
    background-color: #172342 !important;
    color: white !important;
    border: 1px solid #52658f !important;
    border-radius: 9px !important;
}

div[data-baseweb="radio"] label {
    color: white !important;
}

hr {
    border-color: #394b70;
}

.footer {
    text-align: center;
    color: #8998bd;
    font-size: 13px;
    margin-top: 35px;
}

.roll-box {
    background: #202c50;
    border: 1px solid #536aab;
    border-radius: 12px;
    padding: 18px 5px;
    text-align: center;
    color: #58d9ff;
    font-size: 25px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE ----------------

defaults = {
    "pending_email": None,
    "otp": None,
    "otp_expiry": None,
    "otp_attempts": 0,
    "authenticated": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ---------------- HELPER ----------------

def clear_otp():
    st.session_state.pending_email = None
    st.session_state.otp = None
    st.session_state.otp_expiry = None
    st.session_state.otp_attempts = 0


def generate_otp():
    return str(secrets.randbelow(900000) + 100000)


# ---------------- HEADER ----------------

st.markdown(
    '<div class="main-title">🔐 SecureLogin</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Advanced Security • Smart Authentication • Account Protection</div>',
    unsafe_allow_html=True
)


# ==================================================
#                    DASHBOARD
# ==================================================

if st.session_state.authenticated:

    st.markdown("""
    <div class="info-card">
        <h2>🎉 Welcome to SecureLogin!</h2>
        <h3>Two-Step Authentication System</h3>
        <p>
        Your account has been successfully verified through
        our two-step authentication process.
        </p>
        <p>
        Security is not just a feature, it's a necessity.
        SecureLogin adds an extra layer of protection to
        help keep user accounts safe.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🛡️ Project Overview")

    st.write(
        "This project demonstrates secure user authentication "
        "using password verification and Email OTP verification."
    )

    st.success("Authentication Status: Fully Verified")

    st.divider()

    st.subheader("👨‍💻 Project Team")

    cols = st.columns(4)

    roll_numbers = ["104", "109", "121", "136"]

    for col, roll in zip(cols, roll_numbers):
        with col:
            st.markdown(
                f'<div class="roll-box">{roll}</div>',
                unsafe_allow_html=True
            )

    st.markdown(
        '<div class="footer">SecureLogin | Two-Step Authentication Project</div>',
        unsafe_allow_html=True
    )

    st.divider()

    if st.button("🚪 Logout"):
        st.session_state.authenticated = False
        clear_otp()
        st.rerun()


# ==================================================
#                 OTP VERIFICATION SCREEN
# ==================================================

elif st.session_state.pending_email:

    st.markdown("""
    <div class="info-card">
        <h2>📧 Email Verification</h2>
        <p>Your account is almost secure!</p>
        <p>Enter the six-digit OTP sent to your registered email.</p>
    </div>
    """, unsafe_allow_html=True)

    st.info(f"Verification email: {st.session_state.pending_email}")

    remaining_time = max(
        0,
        int(st.session_state.otp_expiry - time.time())
    )

    if remaining_time == 0:
        st.error("Your OTP has expired. Please login again.")
        clear_otp()

        if st.button("Back to Login"):
            st.rerun()

    elif st.session_state.otp_attempts >= 5:
        st.error("Maximum verification attempts reached.")
        clear_otp()

        if st.button("Back to Login"):
            st.rerun()

    else:

        st.caption(
            f"OTP expires in {remaining_time // 60} min "
            f"{remaining_time % 60} sec"
        )

        with st.form("otp_form"):

            entered_otp = st.text_input(
                "Enter 6-Digit OTP",
                max_chars=6
            )

            verify = st.form_submit_button("🔓 Verify OTP")

            if verify:

                if not entered_otp.isdigit() or len(entered_otp) != 6:
                    st.error("Please enter a valid 6-digit OTP.")

                elif entered_otp == st.session_state.otp:

                    st.session_state.authenticated = True
                    clear_otp()
                    st.rerun()

                else:

                    st.session_state.otp_attempts += 1
                    remaining = 5 - st.session_state.otp_attempts

                    if remaining > 0:
                        st.error(
                            f"Incorrect OTP! {remaining} attempts remaining."
                        )
                    else:
                        st.error("Maximum attempts reached. Login again.")
                        clear_otp()
                        st.rerun()

        # RESEND OTP

        st.divider()
        st.write("Didn't receive the verification code?")

        if st.button("🔄 Resend OTP"):

            new_otp = generate_otp()

            result = send_otp_email(
                st.session_state.pending_email,
                new_otp
            )

            if result:
                st.session_state.otp = new_otp
                st.session_state.otp_expiry = time.time() + 300
                st.session_state.otp_attempts = 0

                st.success("A new OTP has been sent to your email!")
                st.rerun()

            else:
                st.error("Unable to resend OTP. Please try again.")

        if st.button("← Back to Login"):
            clear_otp()
            st.rerun()


# ==================================================
#                REGISTER / LOGIN
# ==================================================

else:

    choice = st.radio(
        "Choose an option",
        ["Login", "Register"],
        horizontal=True
    )

    # ---------------- REGISTER ----------------

    if choice == "Register":

        st.markdown("""
        <div class="info-card">
            <h2>✨ Create Your Account</h2>
            <p>Join SecureLogin and protect your account.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("registration_form"):

            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
            phone = st.text_input("Phone Number (+92...)")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input(
                "Confirm Password",
                type="password"
            )

            submit = st.form_submit_button("Create Account")

            if submit:

                if not all([name, email, phone, password, confirm_password]):
                    st.error("Please fill all fields.")

                elif password != confirm_password:
                    st.error("Passwords do not match.")

                elif len(password) < 8:
                    st.error("Password must be at least 8 characters.")

                else:
                    result = register_user(
                        name, email, phone, password
                    )

                    if result:
                        st.success("Account created successfully!")
                    else:
                        st.error("This email is already registered.")

    # ---------------- LOGIN ----------------

    elif choice == "Login":

        st.markdown("""
        <div class="info-card">
            <h2>👋 Welcome Back!</h2>
            <p>Login securely to access your account.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):

            email = st.text_input("Email Address")
            password = st.text_input(
                "Password",
                type="password"
            )

            login = st.form_submit_button("🔐 Login Securely")

            if login:

                user = get_user(email)

                if user and check_password(password, user[4]):

                    otp = generate_otp()

                    result = send_otp_email(email, otp)

                    if result:
                        st.session_state.pending_email = email
                        st.session_state.otp = otp
                        st.session_state.otp_expiry = time.time() + 300
                        st.session_state.otp_attempts = 0

                        st.rerun()

                    else:
                        st.error("Unable to send OTP. Please try again.")

                else:
                    st.error("Invalid email or password.")


st.markdown(
    '<div class="footer">© SecureLogin | Your Security Matters 🔐</div>',
    unsafe_allow_html=True
)

