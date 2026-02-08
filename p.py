import os
import random
import streamlit as st
from PIL import Image

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="💘 Valentine?",
    page_icon="💘",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Admin-only customization via secret URL param
# Use: https://yourapp.streamlit.app/?key=YOUR_SECRET
params = st.query_params
admin_key = params.get("key", "")
SECRET = "change_this_to_a_long_secret"  # <-- CHANGE THIS
show_custom = (admin_key == SECRET)

# Defaults (what everyone sees)
DEFAULT_YOUR_NAME = "Romil"
DEFAULT_HER_NAME = "Arshiya"
DEFAULT_DATE_IDEA = "Let’s book a hotel this weekend and have fun"
DEFAULT_SONG_LINK = ""  # e.g. https://open.spotify.com/track/...

# Sidebar only for you (admin link)
if show_custom:
    with st.sidebar:
        st.header("💌 Customize (Admin)")
        your_name = st.text_input("Your name", value=DEFAULT_YOUR_NAME)
        her_name = st.text_input("Her name", value=DEFAULT_HER_NAME)
        date_idea = st.text_input("Plan / date idea", value=DEFAULT_DATE_IDEA)
        song_link = st.text_input("Song link (optional)", value=DEFAULT_SONG_LINK)
else:
    your_name = DEFAULT_YOUR_NAME
    her_name = DEFAULT_HER_NAME
    date_idea = DEFAULT_DATE_IDEA
    song_link = DEFAULT_SONG_LINK

# =========================
# LUXE ROMANTIC THEME (CSS)
# =========================
st.markdown(
    """
<style>
  :root{
    --bg: #fbf7fb;
    --card: rgba(255,255,255,0.72);
    --stroke: rgba(30,30,40,0.10);
    --text: #1a1a22;
    --muted: rgba(26,26,34,0.62);
    --muted2: rgba(26,26,34,0.48);
    --accent: #ff3d6e;
    --accent2: #ff87b7;
    --gold: #f4d06f;
  }

  .stApp{
    background:
      radial-gradient(1200px 700px at 18% 12%, rgba(255,61,110,0.14), transparent 58%),
      radial-gradient(1200px 700px at 82% 18%, rgba(255,135,183,0.12), transparent 55%),
      radial-gradient(900px 600px at 50% 98%, rgba(244,208,111,0.10), transparent 58%),
      var(--bg);
  }

  .wrap { max-width: 760px; margin: 0 auto; padding: 18px 0 34px; }

  .hero {
    text-align:center;
    padding: 30px 24px 22px;
    border-radius: 28px;
    background: var(--card);
    border: 1px solid var(--stroke);
    box-shadow: 0 22px 70px rgba(0,0,0,0.10);
    backdrop-filter: blur(12px);
  }

  .badge {
    display:inline-flex;
    align-items:center;
    gap: 8px;
    padding: 7px 12px;
    border-radius: 999px;
    background: rgba(255,61,110,0.10);
    border: 1px solid rgba(255,61,110,0.16);
    color: rgba(26,26,34,0.70);
    font-size: 13px;
    margin-bottom: 12px;
  }

  .title {
    font-size: 46px;
    line-height: 1.06;
    font-weight: 850;
    color: var(--text);
    letter-spacing: -0.03em;
    margin: 0 0 10px 0;
  }

  .subtitle {
    margin: 0;
    color: var(--muted);
    font-size: 16px;
  }

  .divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,61,110,0.38), transparent);
    margin: 18px 0 14px;
  }

  .btnrow {
    display:flex;
    justify-content:center;
    align-items:center;
    gap: 18px;
    margin-top: 14px;
    margin-bottom: 6px;
  }

  .hint {
    margin-top: 12px;
    color: var(--muted2);
    font-size: 14px;
  }

  .soft {
    color: var(--muted);
    font-size: 15px;
    margin-top: 10px;
  }

  /* Make Streamlit buttons look luxe */
  .stButton > button {
    min-width: 240px;
    border-radius: 999px !important;
    padding: 0.72rem 1.25rem !important;
    font-weight: 700 !important;
    border: 1px solid rgba(30,30,40,0.12) !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.07) !important;
    transition: transform .15s ease, box-shadow .15s ease !important;
  }
  .stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 14px 38px rgba(0,0,0,0.10) !important;
  }
  button[kind="primary"]{
    background: linear-gradient(90deg, var(--accent), var(--accent2)) !important;
    border: none !important;
  }
  button[kind="secondary"]{
    background: rgba(255,255,255,0.70) !important;
  }

  /* Images: rounded, soft shadow */
  img {
    border-radius: 20px !important;
  }

  .reaction {
    margin-top: 14px;
    padding: 12px 14px;
    border-radius: 18px;
    background: rgba(255,61,110,0.06);
    border: 1px solid rgba(255,61,110,0.12);
    color: rgba(26,26,34,0.70);
    font-size: 15px;
  }

  .yescard {
    margin-top: 10px;
    padding: 18px 16px;
    border-radius: 22px;
    background: rgba(255,255,255,0.58);
    border: 1px solid rgba(30,30,40,0.08);
  }

  .yes-title {
    font-size: 34px;
    font-weight: 850;
    letter-spacing: -0.02em;
    margin: 0 0 8px 0;
    color: var(--text);
  }

  .plan {
    font-size: 18px;
    font-weight: 750;
    margin: 6px 0 0 0;
    color: var(--text);
  }

  .micro {
    margin-top: 10px;
    font-size: 14px;
    color: var(--muted2);
  }

  .songbtn a{
    display:inline-block;
    margin-top: 10px;
    padding: 10px 14px;
    border-radius: 999px;
    background: rgba(244,208,111,0.22);
    border: 1px solid rgba(244,208,111,0.30);
    color: rgba(26,26,34,0.82);
    text-decoration: none;
    font-weight: 700;
  }
  .songbtn a:hover{ opacity: 0.92; }

  .footer {
    text-align:center;
    margin-top: 18px;
    color: rgba(26,26,34,0.45);
    font-size: 13px;
  }
</style>
""",
    unsafe_allow_html=True,
)

# =========================
# STATE
# =========================
if "stage" not in st.session_state:
    st.session_state.stage = "ask"
if "no_clicks" not in st.session_state:
    st.session_state.no_clicks = 0
if "yes_size" not in st.session_state:
    st.session_state.yes_size = 1.0

# =========================
# IMAGES 01..05 (cloud-safe)
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(BASE_DIR, "Images")

CANDIDATES = [
    ("01", [".jpg", ".jpeg", ".png", ".webp"]),
    ("02", [".jpg", ".jpeg", ".png", ".webp"]),
    ("03", [".jpg", ".jpeg", ".png", ".webp"]),
    ("04", [".jpg", ".jpeg", ".png", ".webp"]),
    ("05", [".jpg", ".jpeg", ".png", ".webp"]),
]

images = []
for base, exts in CANDIDATES:
    found = None
    for ext in exts:
        p = os.path.join(IMAGE_FOLDER, f"{base}{ext}")
        if os.path.exists(p):
            found = p
            break
    if found:
        images.append(Image.open(found))

NO_RESPONSES = [
    "Are you sure Pa? 🥺",
    "Okay but… I am baby 😌",
    "Plot twist: you meant YES 🤍",
    "Ill feed you food 🍫",
    "One more chance, pretty Pa please? 💗",
    "I’m still your biggest fan 🥰",
]

CAPTIONS = [
    "Me, trying to act calm 🥺",
    "Still hopeful 😇",
    "I can wait… but I’ll pout 😌",
    "This could be us 👀",
    "Final boss: romance 💘",
]


def accept():
    st.session_state.stage = "accepted"


def nope():
    st.session_state.no_clicks += 1
    st.session_state.yes_size = min(2.4, st.session_state.yes_size + 0.18)


# =========================
# UI
# =========================
st.markdown('<div class="wrap"><div class="hero">', unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="badge">💌 A tiny question for <b>{her_name}</b></div>
    <h1 class="title">💘 {her_name}, will you be my<br/>Valentine?</h1>
    <p class="subtitle">From <b>{your_name}</b> — with all my heart.</p>
    <div class="divider"></div>
    """,
    unsafe_allow_html=True,
)

if st.session_state.stage == "ask":
    # Perfectly aligned buttons with flexbox.
    st.markdown(
        f"""
        <div class="btnrow">
            <div style="transform: scale({st.session_state.yes_size}); transform-origin: center;">
        """,
        unsafe_allow_html=True,
    )
    st.button("YES 💖", type="primary", key="yes_btn", on_click=accept)
    st.markdown("</div>", unsafe_allow_html=True)
    st.button("No 🙈", type="secondary", key="no_btn", on_click=nope)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="hint">Tip: choose <b>YES</b> for maximum happiness ✨</div>', unsafe_allow_html=True)

    # Reactions (no Streamlit info/success boxes — custom styling instead)
    if st.session_state.no_clicks > 0:
        msg = random.choice(NO_RESPONSES)
        st.markdown(
            f'<div class="reaction">{msg} <span style="opacity:.55;">(no clicks: {st.session_state.no_clicks})</span></div>',
            unsafe_allow_html=True,
        )

        if images:
            idx = (st.session_state.no_clicks - 1) % len(images)
            st.image(images[idx], caption=CAPTIONS[idx] if idx < len(CAPTIONS) else None, use_container_width=True)
        else:
            st.markdown(
                '<div class="reaction">I can’t find the images folder. Make sure it is named <b>images/</b> (lowercase) and contains 01..05.</div>',
                unsafe_allow_html=True,
            )

else:
    st.balloons()
    st.markdown(
        f"""
        <div class="yescard">
          <div class="yes-title">It’s a date, {her_name}! 🥰</div>
          <div class="soft">I’m so lucky. Here’s the plan:</div>
          <div class="plan">{date_idea}</div>
          <div class="micro">Screenshot this page and send it to me as proof 😉💌</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if song_link.strip():
        st.markdown(
            f"""
            <div class="songbtn">
              <a href="{song_link}" target="_blank">🎵 Play our song</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown('</div><div class="footer">Made with 💘 on Streamlit</div></div>', unsafe_allow_html=True)

# Optional: tiny admin hint only for you
if show_custom:
    st.caption("🔐 Admin mode enabled. Share the normal link without ?key=...")
