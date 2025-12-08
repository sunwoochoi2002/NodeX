import streamlit as st
import time
import random
from datetime import datetime

# ==========================================
# 1. CONFIGURATION & TRANSLATIONS
# ==========================================

# Color Palette
PRIMARY_COLOR = "#C40046"  # POSTECH Signature Red
SECONDARY_COLOR = "#333333"
ACCENT_COLOR = "#F0F2F6"

# Language Dictionary
TRANSLATIONS = {
    "en": {
        "nav_home": "Home",
        "nav_events": "Events",
        "nav_reviews": "Reviews",
        "nav_mypage": "My Page",
        "hero_title": "NodeX",
        "hero_subtitle": "Come meet, play, and connect with 100+ global students — Everything’s ready for you!",
        "hero_cta": "Join Now",
        "event_header": "Upcoming Events",
        "event_join": "Join",
        "event_joined": "Joined!",
        "review_header": "Student Reviews",
        "review_placeholder": "Write a review...",
        "review_submit": "Submit Review",
        "mypage_header": "My Profile",
        "mypage_welcome": "Welcome back, Student!",
        "lang_toggle": "🇰🇷 KR",
        "footer": "© 2024 NodeX - Connecting POSTECH & The World",
        "participants": "participants",
        "location": "Location",
        "date": "Date",
        "nav_register": "Register",
        "reg_title": "Join NodeX",
        "reg_desc": "Become a member to join events and write reviews.",
        "reg_name": "Full Name",
        "reg_id": "Student ID",
        "reg_email": "Email",
        "reg_submit": "Sign Up",
        "reg_success": "Registration Successful! Welcome, ",
        "stats_visitors": "Today's Visitors",
        "stats_users": "Total Members",
    },
    "kr": {
        "nav_home": "홈",
        "nav_events": "이벤트",
        "nav_reviews": "후기",
        "nav_mypage": "마이페이지",
        "hero_title": "NodeX",
        "hero_subtitle": "100명 이상의 글로벌 학생들과 만나고, 놀고, 연결되세요 — 모든 준비는 끝났습니다!",
        "hero_cta": "지금 참여하기",
        "event_header": "진행 중인 이벤트",
        "event_join": "참여하기",
        "event_joined": "참여 완료!",
        "review_header": "학생 후기",
        "review_placeholder": "후기를 작성해주세요...",
        "review_submit": "후기 등록",
        "mypage_header": "내 프로필",
        "mypage_welcome": "환영합니다, 학생님!",
        "lang_toggle": "🇺🇸 EN",
        "footer": "© 2024 NodeX - 포스텍과 세상을 잇다",
        "participants": "명 참여 중",
        "location": "장소",
        "date": "일시",
        "nav_register": "회원가입",
        "reg_title": "NodeX 가입하기",
        "reg_desc": "이벤트 참여와 후기 작성을 위해 멤버가 되어주세요.",
        "reg_name": "이름",
        "reg_id": "학번",
        "reg_email": "이메일",
        "reg_submit": "가입하기",
        "reg_success": "가입 완료! 환영합니다, ",
        "stats_visitors": "오늘 방문자 수",
        "stats_users": "총 가입 멤버",
    }
}

# ==========================================
# 2. FIREBASE DATABASE (Real Persistence)
# ==========================================
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import Increment

@st.cache_resource
def get_db():
    """Initializes Firebase and returns the Firestore client."""
    # Check if Firebase credentials are set in secrets
    if "firebase" not in st.secrets:
        return None

    # Check if app is already initialized
    if not firebase_admin._apps:
        cred = credentials.Certificate(dict(st.secrets["firebase"]))
        firebase_admin.initialize_app(cred)
    
    return firestore.client()

class RealFirestore:
    def __init__(self, db_client):
        self.db = db_client

    def collection(self, name):
        # Wrapper to allow stream() usage similar to previous code
        if self.db:
            return self.db.collection(name)
        return MockCollection([]) # Fallback if DB not connected

    def log_visit(self):
        if not self.db: return
        
        today = datetime.now().strftime("%Y-%m-%d")
        # Store daily visits in a 'stats' collection, document 'visitors'
        doc_ref = self.db.collection("stats").document("visitors")
        
        # Use set with merge=True to create if not exists, and atomic increment
        try:
            doc_ref.set({today: Increment(1)}, merge=True)
        except Exception as e:
            st.error(f"Error logging visit: {e}")

    def get_visitor_count(self):
        if not self.db: return 0
        
        today = datetime.now().strftime("%Y-%m-%d")
        doc = self.db.collection("stats").document("visitors").get()
        if doc.exists:
            return doc.to_dict().get(today, 0)
        return 0

    def register_user(self, user_data):
        if not self.db: return
        # Use student ID as the document ID to prevent duplicates
        self.db.collection("users").document(user_data["id"]).set(user_data)

    def get_user_count(self):
        if not self.db: return 0
        # Note: For large datasets, use aggregation queries. For now, this is fine.
        return len(list(self.db.collection("users").stream()))

# Fallback for when secrets are missing (to prevent crash)
class MockCollection:
    def __init__(self, data): self.data = data
    def stream(self): return self.data
    def add(self, item): pass

# ==========================================
# 3. SETUP & STYLING
# ==========================================

st.set_page_config(
    page_title="NodeX - Connect & Exchange",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Modern UI and POSTECH Colors
st.markdown(f"""
    <style>
    /* Global Font & Colors */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        color: {SECONDARY_COLOR};
    }}
    
    /* Primary Color Accents */
    .stButton > button {{
        background-color: {PRIMARY_COLOR};
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    .stButton > button:hover {{
        background-color: #A61955; /* Darker shade */
        box-shadow: 0 4px 12px rgba(196, 0, 70, 0.2);
    }}
    
    /* Navigation Bar Styling */
    .nav-container {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        border-bottom: 1px solid #eee;
        margin-bottom: 2rem;
    }}
    
    .nav-logo {{
        font-size: 1.5rem;
        font-weight: 800;
        color: {PRIMARY_COLOR};
        text-decoration: none;
    }}
    
    /* Cards */
    .event-card {{
        background-color: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: transform 0.2s;
        border: 1px solid {ACCENT_COLOR};
    }}
    .event-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
    }}
    
    /* Hero Section */
    .hero-box {{
        background: linear-gradient(135deg, {PRIMARY_COLOR} 0%, #8a0030 100%);
        color: white;
        padding: 4rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 3rem;
    }}
    
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'lang' not in st.session_state:
    st.session_state.lang = 'en'
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Initialize DB Connection
if 'db' not in st.session_state:
    db_client = get_db()
    st.session_state.db = RealFirestore(db_client)
    
    if db_client is None:
        st.warning("⚠️ **Firebase Credentials Not Found!** The app is running in read-only mode. Please configure `.streamlit/secrets.toml` to enable database features.")

# Helper to get text based on current language
def get_text(key):
    return TRANSLATIONS[st.session_state.lang].get(key, key)

def toggle_language():
    st.session_state.lang = 'kr' if st.session_state.lang == 'en' else 'en'

def navigate_to(page_name):
    st.session_state.page = page_name

# ==========================================
# 4. UI COMPONENTS
# ==========================================

def render_navbar():
    # Top Navigation Bar
    col1, col2, col3 = st.columns([2, 6, 1])
    
    with col1:
        st.markdown(f"<div class='nav-logo'>NodeX 🔗</div>", unsafe_allow_html=True)
        
    with col2:
        # Navigation Links as buttons
        c1, c2, c3, c4, c5 = st.columns(5)
        if c1.button(get_text("nav_home"), key="nav_home_btn"): navigate_to("home")
        if c2.button(get_text("nav_events"), key="nav_events_btn"): navigate_to("events")
        if c3.button(get_text("nav_reviews"), key="nav_reviews_btn"): navigate_to("reviews")
        if c4.button(get_text("nav_mypage"), key="nav_mypage_btn"): navigate_to("mypage")
        if c5.button(get_text("nav_register"), key="nav_register_btn"): navigate_to("register")
        
    with col3:
        # Language Toggle
        st.button(get_text("lang_toggle"), on_click=toggle_language, key="lang_btn")

def render_home():
    # Hero Section
    st.markdown(f"""
        <div class="hero-box">
            <h1 style="font-size: 3rem; margin-bottom: 1rem;">{get_text('hero_title')}</h1>
            <p style="font-size: 1.2rem; opacity: 0.9;">{get_text('hero_subtitle')}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Call to Action (Centered)
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        if st.button(get_text("hero_cta"), use_container_width=True):
            navigate_to("events")

    st.markdown("---")
    
    # Quick Preview (Optional)
    st.subheader(get_text("event_header"))
    render_events(limit=3)
    
    # Dashboard / Stats Section
    st.markdown("---")
    st.markdown(f"### 📊 NodeX Dashboard")
    s1, s2 = st.columns(2)
    with s1:
        st.metric(label=get_text("stats_visitors"), value=st.session_state.db.get_visitor_count(), delta="12")
    with s2:
        st.metric(label=get_text("stats_users"), value=st.session_state.db.get_user_count(), delta="New")

def render_events(limit=None):
    events = st.session_state.db.collection("events").stream()
    if limit:
        events = events[:limit]
        
    # Grid Layout for Events
    cols = st.columns(3)
    
    for idx, event in enumerate(events):
        with cols[idx % 3]:
            # Determine title based on language
            title = event['title_en'] if st.session_state.lang == 'en' else event['title_kr']
            
            # Card UI
            st.image(event['image'], use_container_width=True)
            st.markdown(f"### {title}")
            st.caption(f"📅 {event['date']} | 📍 {event['location']}")
            st.markdown(f"**{event['participants']}** {get_text('participants')}")
            
            if st.button(get_text("event_join"), key=f"join_{event['id']}"):
                st.success(get_text("event_joined"))
                # In a real app, update DB here
            
            st.markdown("---")

def render_reviews():
    st.header(get_text("review_header"))
    
    # Review Form
    with st.expander(get_text("review_placeholder")):
        with st.form("review_form"):
            st.text_area("Comment", placeholder=get_text("review_placeholder"))
            st.slider("Rating", 1, 5, 5)
            st.file_uploader("Photo")
            if st.form_submit_button(get_text("review_submit")):
                st.success("Review submitted successfully!")

    # Display Reviews
    reviews = st.session_state.db.collection("reviews").stream()
    
    # Masonry-like grid
    cols = st.columns(3)
    for idx, review in enumerate(reviews):
        with cols[idx % 3]:
            with st.container(border=True):
                st.image(review['image'], use_container_width=True)
                st.markdown(f"**{review['user']}**")
                st.markdown("⭐" * review['rating'])
                st.write(f"\"{review['comment']}\"")

def render_mypage():
    st.header(get_text("mypage_header"))
    
    st.info(get_text("mypage_welcome"))
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("https://api.dicebear.com/7.x/avataaars/svg?seed=Felix", width=150)
    with col2:
        st.subheader("Student Profile")
        st.write("**Name:** Choi Sunwoo")
        st.write("**University:** POSTECH")
        st.write("**Major:** Computer Science")
        st.write("**Interests:** Coding, Coffee, Travel")

def render_register():
    st.header(get_text("reg_title"))
    st.write(get_text("reg_desc"))
    
    with st.form("register_form"):
        name = st.text_input(get_text("reg_name"))
        student_id = st.text_input(get_text("reg_id"))
        email = st.text_input(get_text("reg_email"))
        
        submitted = st.form_submit_button(get_text("reg_submit"))
        if submitted:
            if name and student_id:
                new_user = {"name": name, "id": student_id, "email": email}
                st.session_state.db.register_user(new_user)
                st.success(f"{get_text('reg_success')} {name}!")
                time.sleep(1)
                navigate_to("home")
                st.rerun()
            else:
                st.error("Please fill in all required fields.")

# ==========================================
# 5. MAIN APP EXECUTION
# ==========================================

def main():
    # Visitor Tracking Logic
    if 'has_visited' not in st.session_state:
        st.session_state.db.log_visit()
        st.session_state.has_visited = True

    render_navbar()
    
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    
    if st.session_state.page == 'home':
        render_home()
    elif st.session_state.page == 'events':
        st.header(get_text("event_header"))
        render_events()
    elif st.session_state.page == 'reviews':
        render_reviews()
    elif st.session_state.page == 'mypage':
        render_mypage()
    elif st.session_state.page == 'register':
        render_register()
        
    # Footer
    st.markdown("---")
    st.markdown(f"<div style='text-align: center; color: #888;'>{get_text('footer')}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
