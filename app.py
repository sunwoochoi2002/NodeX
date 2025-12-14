import streamlit as st
import time
import random
import json
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
        "nav_events": "All Events",
        "nav_reviews": "Reviews",
        "nav_mypage": "My Page",
        "hero_title": "NodeX",
        "hero_subtitle": "Come meet, play, and connect with 100+ global students — Everything’s ready for you!",
        "hero_cta": "Register Now",
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
        "event_details": "View Details",
        "event_schedule": "Schedule",
        "event_cost": "Participation Fee",
        "event_duration": "Duration",
        "event_hours": "hours",
        "event_enter_name": "Enter your registered name",
        "event_not_registered": "You are not registered. Please register first!",
        "event_already_joined": "You have already joined this event!",
        "event_join_success": "Successfully joined the event!",
        "mypage_joined_events": "My Joined Events",
        "mypage_no_events": "You haven't joined any events yet.",
        "mypage_login_prompt": "Enter your name to view your profile",
        "mypage_view": "View Profile",
    },
    "kr": {
        "nav_home": "홈",
        "nav_events": "전체 이벤트",
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
        "event_details": "상세 보기",
        "event_schedule": "일정",
        "event_cost": "참가비",
        "event_duration": "소요 시간",
        "event_hours": "시간",
        "event_enter_name": "등록된 이름을 입력하세요",
        "event_not_registered": "등록되지 않은 사용자입니다. 먼저 회원가입을 해주세요!",
        "event_already_joined": "이미 참여한 이벤트입니다!",
        "event_join_success": "이벤트 참여가 완료되었습니다!",
        "mypage_joined_events": "참여한 이벤트",
        "mypage_no_events": "아직 참여한 이벤트가 없습니다.",
        "mypage_login_prompt": "프로필을 보려면 이름을 입력하세요",
        "mypage_view": "프로필 보기",
    }
}

# ==========================================
# 1.1 INITIAL DATA (For Seeding)
# ==========================================
INITIAL_EVENTS = [
    {
        "title_en": "Board Game Cafe Night",
        "title_kr": "보드게임 카페 모임",
        "date": "2026-01-15 19:00",
        "location": "Whale Cafe, Hyoja",
        "image": "https://images.unsplash.com/photo-1632501641765-e568d9088bed?auto=format&fit=crop&q=80&w=800",
        "current_participants": 3,
        "max_participants": 12,
        "participant_names": [],
        "duration_hours": 4,
        "is_upcoming": True,
        "schedule": [
            {"time": "19:00", "activity_en": "Meetup & Introduction", "activity_kr": "만남 및 소개"},
            {"time": "19:30", "activity_en": "Light snacks & drinks", "activity_kr": "간식 및 음료"},
            {"time": "20:00", "activity_en": "Board game session 1", "activity_kr": "보드게임 세션 1"},
            {"time": "21:00", "activity_en": "Break & Photo time", "activity_kr": "휴식 및 사진 시간"},
            {"time": "21:30", "activity_en": "Board game session 2", "activity_kr": "보드게임 세션 2"},
            {"time": "22:30", "activity_en": "Wrap-up & Farewell", "activity_kr": "마무리 및 작별"}
        ]
    },
    {
        "title_en": "Pohang Hyoja Market Tour",
        "title_kr": "포항 효자 시장 투어",
        "date": "2026-01-22 11:00",
        "location": "Hyoja Market Entrance",
        "image": "https://images.unsplash.com/photo-1533900298318-6b8da08a523e?auto=format&fit=crop&q=80&w=800",
        "current_participants": 2,
        "max_participants": 8,
        "participant_names": [],
        "duration_hours": 3,
        "is_upcoming": True,
        "schedule": [
            {"time": "11:00", "activity_en": "Meet at market entrance", "activity_kr": "시장 입구 집합"},
            {"time": "11:15", "activity_en": "Traditional market exploration", "activity_kr": "전통시장 탐방"},
            {"time": "12:00", "activity_en": "Local street food tasting", "activity_kr": "현지 길거리 음식 맛보기"},
            {"time": "13:00", "activity_en": "Free shopping time", "activity_kr": "자유 쇼핑 시간"},
            {"time": "13:45", "activity_en": "Group photo & Wrap-up", "activity_kr": "단체 사진 및 마무리"}
        ]
    },
    {
        "title_en": "Local Foodie Tour",
        "title_kr": "맛집 투어",
        "date": "2026-01-10 18:00",
        "location": "Yeongildae Beach",
        "image": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&q=80&w=800",
        "current_participants": 5,
        "max_participants": 20,
        "participant_names": [],
        "duration_hours": 5,
        "is_upcoming": True,
        "schedule": [
            {"time": "18:00", "activity_en": "Gather at meeting point", "activity_kr": "집합 장소 모임"},
            {"time": "18:30", "activity_en": "Restaurant 1: Fresh seafood", "activity_kr": "맛집 1: 신선한 해산물"},
            {"time": "19:30", "activity_en": "Walk along the beach", "activity_kr": "해변 산책"},
            {"time": "20:00", "activity_en": "Restaurant 2: Korean BBQ", "activity_kr": "맛집 2: 한국식 바베큐"},
            {"time": "21:30", "activity_en": "Dessert cafe visit", "activity_kr": "디저트 카페 방문"},
            {"time": "22:30", "activity_en": "Night view & Farewell", "activity_kr": "야경 감상 및 작별"}
        ]
    },
    {
        "title_en": "Yeongildae Beach Tour",
        "title_kr": "영일대 해변 투어",
        "date": "2026-01-18 14:00",
        "location": "Space Walk",
        "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&q=80&w=800",
        "current_participants": 8,
        "max_participants": 25,
        "participant_names": [],
        "duration_hours": 6,
        "is_upcoming": True,
        "schedule": [
            {"time": "14:00", "activity_en": "Meet at Space Walk", "activity_kr": "스페이스워크 집합"},
            {"time": "14:30", "activity_en": "Space Walk photo time", "activity_kr": "스페이스워크 사진 시간"},
            {"time": "15:30", "activity_en": "Beach activities & games", "activity_kr": "해변 활동 및 게임"},
            {"time": "17:00", "activity_en": "Free time & swimming", "activity_kr": "자유시간 및 수영"},
            {"time": "18:30", "activity_en": "Sunset watching", "activity_kr": "일몰 감상"},
            {"time": "19:30", "activity_en": "Beach BBQ dinner", "activity_kr": "해변 바베큐 저녁"},
            {"time": "20:30", "activity_en": "Wrap-up & Farewell", "activity_kr": "마무리 및 작별"}
        ]
    },
    {
        "title_en": "Movie Night",
        "title_kr": "영화 나들이",
        "date": "2026-01-25 20:00",
        "location": "CGV Pohang",
        "image": "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&q=80&w=800",
        "current_participants": 4,
        "max_participants": 15,
        "participant_names": [],
        "duration_hours": 4,
        "is_upcoming": True,
        "schedule": [
            {"time": "20:00", "activity_en": "Meet at CGV lobby", "activity_kr": "CGV 로비 집합"},
            {"time": "20:15", "activity_en": "Get popcorn & snacks", "activity_kr": "팝콘 및 간식 구매"},
            {"time": "20:30", "activity_en": "Movie screening", "activity_kr": "영화 상영"},
            {"time": "22:30", "activity_en": "Movie discussion at cafe", "activity_kr": "카페에서 영화 토론"},
            {"time": "23:30", "activity_en": "Farewell", "activity_kr": "작별"}
        ]
    }
]

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

    def _to_dict(self, doc):
        """Helper to convert Firestore DocumentSnapshot to dict safely."""
        if hasattr(doc, 'to_dict'):
            data = doc.to_dict()
            data['id'] = doc.id  # Include the document ID
            return data
        return doc # Already a dict (Mock case)

    def get_events(self, limit=None):
        """Fetches events as a list of dictionaries."""
        if not self.db: return []
        
        # Fetch stream
        docs = self.db.collection("events").stream()
        
        # Convert to list of dicts
        events = [self._to_dict(doc) for doc in docs]
        
        # Apply limit if requested
        if limit:
            return events[:limit]
        return events

    def get_reviews(self):
        """Fetches reviews as a list of dictionaries."""
        if not self.db: return []
        docs = self.db.collection("reviews").stream()
        return [self._to_dict(doc) for doc in docs]

    def add_review(self, review_data):
        """Add a new review to the database."""
        if not self.db: return None
        review_data['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M")
        doc_ref = self.db.collection("reviews").add(review_data)
        return doc_ref

    def get_past_events(self):
        """Fetches past events (is_upcoming=False) as a list of dictionaries."""
        if not self.db: return []
        all_events = self.db.collection("events").stream()
        events = [self._to_dict(doc) for doc in all_events]
        # Filter for past events only
        return [e for e in events if e.get('is_upcoming', True) == False]

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
        """Registers a user and stamps the registration date for daily stats."""
        if not self.db: return
        
        # Ensure we don't mutate the original input
        user_record = dict(user_data)
        user_record.setdefault("created_at", datetime.now().strftime("%Y-%m-%d"))
        
        # Use student ID as the document ID to prevent duplicates
        self.db.collection("users").document(user_record["id"]).set(user_record)

    def get_user_count(self):
        if not self.db: return 0
        # Note: For large datasets, use aggregation queries. For now, this is fine.
        return len(list(self.db.collection("users").stream()))

    def get_today_user_registrations(self):
        """Counts how many users registered today."""
        if not self.db: return 0
        
        today = datetime.now().strftime("%Y-%m-%d")
        users = self.db.collection("users").stream()
        return sum(1 for user in users if self._to_dict(user).get("created_at") == today)

    def add_event(self, event_data):
        if not self.db: return
        self.db.collection("events").add(event_data)

    def delete_event(self, event_id):
        if not self.db: return
        self.db.collection("events").document(event_id).delete()

    def update_event(self, event_id, updates):
        """Update specific fields of an event."""
        if not self.db: return
        self.db.collection("events").document(event_id).update(updates)

    def seed_events(self):
        if not self.db: return
        
        # First, delete ALL existing events to prevent duplicates
        existing_events = self.db.collection("events").stream()
        for doc in existing_events:
            doc.reference.delete()
        
        # Then add fresh events
        batch = self.db.batch()
        for event in INITIAL_EVENTS:
            doc_ref = self.db.collection("events").document()
            batch.set(doc_ref, event)
        batch.commit()

    def get_user_by_name(self, name):
        """Find a user by their name. Returns user dict or None."""
        if not self.db: return None
        users = self.db.collection("users").where("name", "==", name).stream()
        for user in users:
            return self._to_dict(user)
        return None

    def get_user_by_id(self, user_id):
        """Find a user by their ID. Returns user dict or None."""
        if not self.db: return None
        doc = self.db.collection("users").document(user_id).get()
        if doc.exists:
            return self._to_dict(doc)
        return None

    def join_event(self, user_id, event_id, event_title, user_name):
        """Add an event to a user's joined_events list and update event participants."""
        if not self.db: return False
        
        # Get user document
        user_ref = self.db.collection("users").document(user_id)
        user_doc = user_ref.get()
        
        if not user_doc.exists:
            return False
        
        user_data = user_doc.to_dict()
        joined_events = user_data.get("joined_events", [])
        
        # Check if already joined
        if any(e.get("event_id") == event_id for e in joined_events):
            return "already_joined"
        
        # Get event document to check capacity
        event_ref = self.db.collection("events").document(event_id)
        event_doc = event_ref.get()
        
        if not event_doc.exists:
            return False
        
        event_data = event_doc.to_dict()
        current = event_data.get("current_participants", event_data.get("participants", 0))
        max_p = event_data.get("max_participants", 20)
        
        # Check if event is full
        if current >= max_p:
            return "event_full"
        
        # Add event to user's joined_events
        joined_events.append({
            "event_id": event_id,
            "event_title": event_title,
            "joined_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        user_ref.update({"joined_events": joined_events})
        
        # Update event: increment current_participants and add user name to participant_names
        participant_names = event_data.get("participant_names", [])
        participant_names.append(user_name)
        
        event_ref.update({
            "current_participants": Increment(1),
            "participant_names": participant_names
        })
        
        return True

    def get_user_events(self, user_id):
        """Get list of events a user has joined."""
        if not self.db: return []
        
        user_doc = self.db.collection("users").document(user_id).get()
        if user_doc.exists:
            return user_doc.to_dict().get("joined_events", [])
        return []

    def get_event_by_id(self, event_id):
        """Get a single event by its ID."""
        if not self.db: return None
        
        doc = self.db.collection("events").document(event_id).get()
        if doc.exists:
            return self._to_dict(doc)
        return None

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
        cols = st.columns(6) if st.session_state.get('is_admin', False) else st.columns(5)
        
        if cols[0].button(get_text("nav_home"), key="nav_home_btn"): navigate_to("home")
        if cols[1].button(get_text("nav_events"), key="nav_events_btn"): navigate_to("events")
        if cols[2].button(get_text("nav_reviews"), key="nav_reviews_btn"): navigate_to("reviews")
        if cols[3].button(get_text("nav_mypage"), key="nav_mypage_btn"): navigate_to("mypage")
        if cols[4].button(get_text("nav_register"), key="nav_register_btn"): navigate_to("register")
        
        if st.session_state.get('is_admin', False):
            if cols[5].button("⚙️ Admin", key="nav_admin_btn"): navigate_to("admin")
        
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
            navigate_to("register")

    st.markdown("---")
    
    # Quick Preview (Optional)
    st.subheader(get_text("event_header"))
    render_events(limit=3)
    
    # Dashboard / Stats Section
    st.markdown("---")
    st.markdown(f"### 📊 NodeX Dashboard")
    s1, s2 = st.columns(2)

    visitor_count = st.session_state.db.get_visitor_count()
    total_users = st.session_state.db.get_user_count()
    today_new_users = st.session_state.db.get_today_user_registrations()

    with s1:
        st.metric(label=get_text("stats_visitors"), value=visitor_count)
    with s2:
        st.metric(
            label=get_text("stats_users"),
            value=total_users,
            delta=f"+{today_new_users}" if today_new_users else "0"
        )

def render_events(limit=None):
    # Use the robust data access method
    all_events = st.session_state.db.get_events(limit=None)
    
    # Filter events: only show events where is_upcoming is True
    events = [event for event in all_events if event.get('is_upcoming', False) == True]
    
    # Sort events by date (closest first)
    def parse_date(event):
        try:
            return datetime.strptime(event.get('date', '2099-12-31 23:59'), "%Y-%m-%d %H:%M")
        except (ValueError, TypeError):
            return datetime.max
    
    events = sorted(events, key=parse_date)
    
    # Apply limit after filtering and sorting
    if limit:
        events = events[:limit]
    
    if not events:
        st.info("No upcoming events at the moment. Check back later!")
        return
        
    # Grid Layout for Events
    cols = st.columns(3)
    
    for idx, event in enumerate(events):
        with cols[idx % 3]:
            # Determine title based on language
            title = event.get('title_en', 'Untitled') if st.session_state.lang == 'en' else event.get('title_kr', '제목 없음')
            event_id = event.get('id', str(idx))
            
            # Card UI
            image_url = event.get('image') or 'https://via.placeholder.com/300x200?text=No+Image'
            try:
                st.image(image_url, use_container_width=True)
            except Exception:
                st.image('https://via.placeholder.com/300x200?text=No+Image', use_container_width=True)
            st.markdown(f"### {title}")
            st.caption(f"📅 {event.get('date', 'TBD')} | 📍 {event.get('location', 'TBD')}")
            
            # Participants count: current/max format
            current = event.get('current_participants', event.get('participants', 0))
            max_p = event.get('max_participants', 20)
            st.markdown(f"👥 **{current}/{max_p}** {get_text('participants')}")
            
            # Duration and Cost
            duration = event.get('duration_hours', 3)
            cost = duration * 1.5
            st.markdown(f"⏱️ **{get_text('event_duration')}:** {duration} {get_text('event_hours')} | 💵 **{get_text('event_cost')}:** ${cost:.1f}")
            
            # Event Details Toggle (Schedule)
            schedule = event.get('schedule', [])
            if schedule:
                with st.expander(f"📋 {get_text('event_details')}"):
                    st.markdown(f"**{get_text('event_schedule')}**")
                    for item in schedule:
                        activity = item.get('activity_en', '') if st.session_state.lang == 'en' else item.get('activity_kr', '')
                        st.markdown(f"- **{item.get('time', '')}** - {activity}")
            
            # Join Button with Name Verification
            with st.expander(f"🎫 {get_text('event_join')}"):
                # Check if event is full
                if current >= max_p:
                    st.warning("🚫 This event is full!")
                else:
                    join_name = st.text_input(
                        get_text("event_enter_name"), 
                        key=f"join_name_{event_id}"
                    )
                    
                    # Initialize session state for showing register button
                    show_register_key = f"show_register_{event_id}"
                    if show_register_key not in st.session_state:
                        st.session_state[show_register_key] = False
                    
                    # Join button
                    if st.button(get_text("event_join"), key=f"join_btn_{event_id}", use_container_width=True):
                        if join_name:
                            # Check if user is registered
                            user = st.session_state.db.get_user_by_name(join_name)
                            if user:
                                # Try to join the event
                                result = st.session_state.db.join_event(user['id'], event_id, title, join_name)
                                if result == "already_joined":
                                    st.warning(get_text("event_already_joined"))
                                elif result == "event_full":
                                    st.error("This event is full!")
                                elif result:
                                    st.success(get_text("event_join_success"))
                                    st.session_state[show_register_key] = False
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.error("Failed to join event.")
                            else:
                                # User not registered - show register button
                                st.error(get_text("event_not_registered"))
                                st.session_state[show_register_key] = True
                        else:
                            st.warning(get_text("event_enter_name"))
                    
                    # Show Register button only if user is not registered
                    if st.session_state[show_register_key]:
                        if st.button("🔐 Register First", key=f"go_register_{event_id}", use_container_width=True):
                            navigate_to("register")
                            st.rerun()
            
            st.markdown("---")

def render_reviews():
    st.header(get_text("review_header"))
    
    # Get past events for selection
    past_events = st.session_state.db.get_past_events()
    
    # Review Form
    with st.expander(f"✍️ {get_text('review_placeholder')}", expanded=False):
        if not past_events:
            st.info("No past events available for review yet. Reviews can only be written for completed events.")
        else:
            with st.form("review_form"):
                # Event selection
                event_options = {
                    e.get('id'): f"{e.get('title_en', 'Untitled')} ({e.get('date', 'N/A')})" 
                    if st.session_state.lang == 'en' 
                    else f"{e.get('title_kr', '제목 없음')} ({e.get('date', 'N/A')})"
                    for e in past_events
                }
                
                selected_event_id = st.selectbox(
                    "Select Event" if st.session_state.lang == 'en' else "이벤트 선택",
                    options=list(event_options.keys()),
                    format_func=lambda x: event_options.get(x, "Unknown")
                )
                
                # Author name
                author_name = st.text_input(
                    "Your Name" if st.session_state.lang == 'en' else "작성자 이름"
                )
                
                # Rating
                rating = st.slider(
                    "Rating" if st.session_state.lang == 'en' else "별점", 
                    1, 5, 5
                )
                
                # Comment
                comment = st.text_area(
                    "Your Review" if st.session_state.lang == 'en' else "리뷰 내용",
                    placeholder=get_text("review_placeholder")
                )
                
                if st.form_submit_button(get_text("review_submit")):
                    if author_name and comment:
                        # Get event title for display
                        event_title = event_options.get(selected_event_id, "Unknown Event")
                        
                        review_data = {
                            "event_id": selected_event_id,
                            "event_title": event_title,
                            "user": author_name,
                            "rating": rating,
                            "comment": comment
                        }
                        st.session_state.db.add_review(review_data)
                        st.success("Review submitted successfully!" if st.session_state.lang == 'en' else "리뷰가 등록되었습니다!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.warning("Please fill in your name and review." if st.session_state.lang == 'en' else "이름과 리뷰 내용을 입력해주세요.")

    # Display Reviews
    st.markdown("---")
    reviews = st.session_state.db.get_reviews()
    
    if not reviews:
        st.info("No reviews yet. Be the first to write one!" if st.session_state.lang == 'en' else "아직 리뷰가 없습니다. 첫 리뷰를 작성해보세요!")
        return
    
    # Grid layout for reviews
    cols = st.columns(3)
    for idx, review in enumerate(reviews):
        with cols[idx % 3]:
            with st.container(border=True):
                # Event title
                st.caption(f"📅 {review.get('event_title', 'Unknown Event')}")
                # Author
                st.markdown(f"**{review.get('user', 'Anonymous')}**")
                # Rating
                st.markdown("⭐" * review.get('rating', 5))
                # Comment
                st.write(f"\"{review.get('comment', '')}\"")
                # Date
                st.caption(f"🕐 {review.get('created_at', 'N/A')}")

def render_mypage():
    st.header(get_text("mypage_header"))
    
    # User lookup by name - store only the user_id, not the full data
    if 'mypage_user_id' not in st.session_state:
        st.session_state.mypage_user_id = None
    
    # Login form to find user
    with st.container(border=True):
        st.markdown(f"**{get_text('mypage_login_prompt')}**")
        lookup_name = st.text_input("Name", key="mypage_lookup_name", label_visibility="collapsed")
        if st.button(get_text("mypage_view"), key="mypage_lookup_btn"):
            if lookup_name:
                user = st.session_state.db.get_user_by_name(lookup_name)
                if user:
                    st.session_state.mypage_user_id = user.get('id')
                    st.rerun()
                else:
                    st.error(get_text("event_not_registered"))
    
    # Display user profile if logged in - ALWAYS fetch fresh data from DB
    if st.session_state.mypage_user_id:
        # Fetch fresh user data every time
        user = st.session_state.db.get_user_by_id(st.session_state.mypage_user_id)
        
        if not user:
            st.error("User not found. Please login again.")
            st.session_state.mypage_user_id = None
            return
        
        st.info(get_text("mypage_welcome"))
        
        col1, col2 = st.columns([1, 3])
        with col1:
            # Generate avatar based on user name
            avatar_seed = user.get('name', 'User').replace(' ', '')
            st.image(f"https://api.dicebear.com/7.x/avataaars/svg?seed={avatar_seed}", width=150)
        with col2:
            st.subheader(user.get('name', 'Unknown'))
            st.write(f"**Student ID:** {user.get('id', 'N/A')}")
            st.write(f"**Email:** {user.get('email', 'N/A')}")
            st.write(f"**Registered:** {user.get('created_at', 'N/A')}")
        
        st.markdown("---")
        
        # Display joined events - this now shows fresh data
        st.subheader(f"🎫 {get_text('mypage_joined_events')}")
        
        joined_events = user.get('joined_events', [])
        if joined_events:
            for event_info in joined_events:
                with st.container(border=True):
                    col_a, col_b = st.columns([3, 1])
                    with col_a:
                        st.markdown(f"**{event_info.get('event_title', 'Unknown Event')}**")
                        st.caption(f"📅 Joined: {event_info.get('joined_at', 'N/A')}")
                    with col_b:
                        # Fetch event details if needed
                        event_id = event_info.get('event_id')
                        if event_id:
                            event_data = st.session_state.db.get_event_by_id(event_id)
                            if event_data:
                                duration = event_data.get('duration_hours', 3)
                                cost = duration * 1.5
                                st.markdown(f"💵 ${cost:.1f}")
        else:
            st.info(get_text("mypage_no_events"))
        
        # Logout button
        if st.button("🚪 Logout", key="mypage_logout"):
            st.session_state.mypage_user_id = None
            st.rerun()

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



def render_admin():
    st.header("⚙️ Admin Dashboard")
    
    st.subheader("1. Database Management")
    if st.button("Initialize/Seed Event Data"):
        st.session_state.db.seed_events()
        st.success("Database seeded with initial events!")
        time.sleep(1)
        st.rerun()

    st.divider()
    
    st.subheader("2. Add New Event")
    with st.form("add_event_form"):
        c1, c2 = st.columns(2)
        title_en = c1.text_input("Title (English)")
        title_kr = c2.text_input("Title (Korean)")
        date = c1.text_input("Date (e.g., 2024-05-20 19:00)")
        location = c2.text_input("Location")
        image = st.text_input("Image URL (Unsplash etc.)")
        
        c3, c4 = st.columns(2)
        current_participants = c3.number_input("Current Participants", value=0)
        max_participants = c4.number_input("Max Participants", min_value=1, value=20)
        
        c5, c6 = st.columns(2)
        duration_hours = c5.number_input("Duration (hours)", min_value=1, max_value=12, value=4)
        is_upcoming = c6.checkbox("Is Upcoming (visible to users)", value=True)
        
        st.markdown("**Schedule (JSON format)**")
        st.caption('Example: [{"time": "19:00", "activity_en": "Meetup", "activity_kr": "만남"}]')
        schedule_json = st.text_area("Schedule", value="[]", height=100)
        
        if st.form_submit_button("Add Event"):
            try:
                schedule = json.loads(schedule_json)
            except json.JSONDecodeError:
                schedule = []
                st.warning("Invalid JSON format for schedule. Using empty schedule.")
            
            new_event = {
                "title_en": title_en, "title_kr": title_kr,
                "date": date, "location": location,
                "image": image, 
                "current_participants": current_participants,
                "max_participants": max_participants,
                "participant_names": [],
                "duration_hours": duration_hours,
                "is_upcoming": is_upcoming,
                "schedule": schedule
            }
            st.session_state.db.add_event(new_event)
            st.success("Event added!")
            time.sleep(1)
            st.rerun()
            
    st.divider()
    
    st.subheader("3. Manage Events")
    events = st.session_state.db.get_events()
    for e_data in events:
        is_upcoming = e_data.get('is_upcoming', False)
        status_icon = "✅" if is_upcoming else "❌"
        with st.expander(f"{status_icon} {e_data.get('title_en', 'Untitled')} ({e_data.get('date', 'No Date')})"):
            st.write(e_data)
            
            col_a, col_b = st.columns(2)
            with col_a:
                # Toggle is_upcoming status
                if is_upcoming:
                    if st.button("🚫 Mark as Past", key=f"hide_{e_data.get('id')}"):
                        st.session_state.db.update_event(e_data.get('id'), {"is_upcoming": False})
                        st.warning("Event marked as past (hidden from users).")
                        time.sleep(1)
                        st.rerun()
                else:
                    if st.button("✅ Mark as Upcoming", key=f"show_{e_data.get('id')}"):
                        st.session_state.db.update_event(e_data.get('id'), {"is_upcoming": True})
                        st.success("Event marked as upcoming (visible to users).")
                        time.sleep(1)
                        st.rerun()
            
            with col_b:
                if st.button("🗑️ Delete Event", key=f"del_{e_data.get('id')}"):
                    st.session_state.db.delete_event(e_data.get('id'))
                    st.error("Event deleted.")
                    time.sleep(1)
                    st.rerun()

# ==========================================
# 5. MAIN APP EXECUTION
# ==========================================

def main():
    # Admin Login Sidebar
    with st.sidebar:
        st.header("Admin Access")
        if not st.session_state.get('is_admin', False):
            pwd = st.text_input("Password", type="password")
            # Simple password check (In production, use st.secrets['admin_password'])
            if pwd == "1234": 
                st.session_state.is_admin = True
                st.success("Logged in!")
                st.rerun()
        else:
            st.success("Admin Mode Active")
            if st.button("Logout"):
                st.session_state.is_admin = False
                navigate_to("home")
                st.rerun()

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
    elif st.session_state.page == 'admin':
        if st.session_state.get('is_admin', False):
            render_admin()
        else:
            st.error("Access Denied")
            navigate_to("home")
        
    # Footer
    st.markdown("---")
    st.markdown(f"<div style='text-align: center; color: #888;'>{get_text('footer')}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
