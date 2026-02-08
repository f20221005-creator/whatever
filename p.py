import os
import random
import streamlit as st
from PIL import Image

# ---------- Page config ----------
st.set_page_config(
    page_title="💘 Valentine?",
    page_icon="💘",
    layout="centered",
    initial_sidebar_state="collapsed",  # hide sidebar by default for everyone
)

# ---------- Admin-only customization via secret URL param ----------
# Use: https://yourapp.streamlit.app/?key=YOUR_SECRET
params = st.query_params
admin_key = params.get("key", "")

SECRET = "change_this_to_a_long_secret"  # <-- CHANGE THIS
show_custom = (admin_key == SECRET)

# ---------- Default values (what everyone sees) ----------
DEFAULT_YOUR_NAME = "Romil"
DEFAULT_HER_NAME = "Arshiya"
DEFAULT_DATE_IDEA = "Lets book a hotel this weekend and have fun"
DEFAULT_SONG_LINK = ""  # e.g. https://open.spotify.com/track/...

# ---------- Sidebar personalization (ONLY for you with the secret key) ----------
if show_custom:
    with st.sidebar:
        st.header("💌 Customize (Admin)")
        your_name = st.text_input("Your name", value=DEFAULT_YOUR_NAME)
        her_name = st.text_input("Her name", value=DEFAULT_HER_NAME)
        date_idea = st.text_input("Date idea", value=DEFAULT_DATE_IDEA)
        song_link = st.text_input("Song link (optional)", value=DEFAULT_SONG_LINK)
else:
    your_name = DEFAULT_YOUR_NAME
    her_name = DEFAULT_HER_NAME
    date_idea = DEFAULT_DATE_IDEA
    song_link = DEFAULT_SONG_LINK

# ---------- CSS (cute + clean) ----------
st.markdown(
    """
    <style>
      .big-title { font-size: 44px; font-weight: 800; text-align: center; margin-top: 6px; }
      .sub { font-size: 18px; text-align: center; opacity: 0.9; margin-bottom: 16px; }
      .card {
        background: rgba(255, 192, 203, 0.18);
        border: 1px solid rgba(255, 105, 180, 0.25);
        padding: 18px 18px 14px 18px;
        border-radius: 18px;
        box-shadow: 0 10px 30px rgba(255, 105, 180, 0.08);
      }
      .footer { text-align:center; opacity:0.75; margin-top: 22px; font-size: 14px; }
      button[kind="primary"] { border-radius: 999px !important; }
      button[kind="secondary"] { border-radius: 999px !important; }
      button { transition: transform 0.2s ease; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Session state ----------
if "stage" not in st.session_state:
    st.session_state.stage = "ask"  # ask -> accepted
if "no_clicks" not in st.session_state:
    st.session_state.no_clicks = 0
if "yes_size" not in st.session_state:
    st.session_state.yes_size = 1.0

# ---------- Load images 01..05 from ./images (cloud-safe absolute path) ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(BASE_DIR, "images")

CANDIDATES = [
    ("01", [".jpg", ".jpeg", ".png", ".webp"]),
    ("02", [".jpg", ".jpeg", ".png", ".webp"]),
    ("03", [".jpg", ".jpeg", ".png", ".webp"]),
    ("04", [".jpg", ".jpeg", ".png", ".webp"]),
    ("05", [".jpg", ".jpeg", ".png", ".webp"]),
]

images = []
image_labels = []

for base, exts in CANDIDATES:
    found_path = None
    for ext in exts:
        p = os.path.join(IMAGE_FOLDER, f"{base}{ext}")
        if os.path.exists(p):
            found_path = p
            break
    if found_path:
        images.append(Image.open(found_path))
        image_labels.append(base)

NO_RESPONSES = [
    "Are you suuure? 🥺",
    "Try again… for me? 💗",
    "That button seems broken 😤",
    "Okay but… what if I ask nicely? 😊",
    "I brought snacks though 🍫",
    "I’ll be extra cute today 😌",
    "Plot twist: you meant YES 😇",
    "I’m not giving up 😤💘",
]

CAPTIONS = [
    "Me when you say no 🥺",
    "Still hopeful 😇",
    "One more chance? 💗",
    "Okay but look at THIS face 😌",
    "Final boss: cuteness overload 💘",
]


def render_hearts(n=22):
    hearts = ["💗", "💖", "💘", "💕", "💞", "❤️"]
    st.write(" ".join(random.choice(hearts) for _ in range(n)))


def accept():
    st.session_state.stage = "accepted"


def nope():
    st.session_state.no_clicks += 1
    st.session_state.yes_size = min(2.4, st.session_state.yes_size + 0.18)


# ---------- UI ----------
st.markdown(
    f'<div class="big-title">💘 {her_name}, will you be my Valentine?</div>',
    unsafe_allow_html=True,
)
st.markdown(
    f'<div class="sub">From <b>{your_name}</b> — with love, bribes, and zero shame.</div>',
    unsafe_allow_html=True,
)

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    if st.session_state.stage == "ask":
        render_hearts()

        # ---------- PERFECTLY ALIGNED BUTTON ROW (flexbox) ----------
        st.markdown(
            f"""
            <div style="
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 40px;
                margin-top: 12px;
                margin-bottom: 12px;
            ">
                <div style="transform: scale({st.session_state.yes_size}); transform-origin: center;">
            """,
            unsafe_allow_html=True,
        )

        # YES button (inside the scaled wrapper)
        st.button("YES 💖", type="primary", key="yes_btn", on_click=accept)

        # Close YES wrapper, render NO button, close flex container
        st.markdown("</div>", unsafe_allow_html=True)
        st.button("No 🙈", type="secondary", key="no_btn", on_click=nope)
        st.markdown("</div>", unsafe_allow_html=True)

        # Reaction message + image after at least one "No"
        if st.session_state.no_clicks > 0:
            st.info(f"{random.choice(NO_RESPONSES)} (No clicks: {st.session_state.no_clicks})")
            st.write("😈 The YES button is getting stronger...")

            if images:
                idx = (st.session_state.no_clicks - 1) % len(images)  # 0..4 looping
                caption = CAPTIONS[idx] if idx < len(CAPTIONS) else f"Reaction {image_labels[idx]}"
                st.image(images[idx], caption=caption, use_container_width=True)
            else:
                st.warning(
                    "I couldn't find your images. Make sure your repo has a folder named `images/` "
                    "in the root and files named `01.jpg`..`05.jpg` (or .jpeg/.png/.webp). "
                    "Linux is case-sensitive: `images` ≠ `Images`."
                )

        st.divider()
        st.write("✨ Hint: Choose **YES** for maximum happiness.")

    else:
        st.balloons()
        st.success("YAYYYYY!!! 💞💞💞")
        st.markdown(
            f"""
            <h2 style="text-align:center; margin-top: 6px;">It’s a date, {her_name}! 🥰</h2>
            <p style="text-align:center; font-size: 18px;">
              I’m so lucky. Here’s the plan: <b>{date_idea}</b>
            </p>
            """,
            unsafe_allow_html=True,
        )

        if song_link.strip():
            st.markdown(
                f'<p style="text-align:center;">🎵 Our vibe song: <a href="{song_link}" target="_blank">click here</a></p>',
                unsafe_allow_html=True,
            )

        render_hearts(30)
        st.markdown(
            """
            <p style="text-align:center; font-size: 16px; opacity: 0.9;">
              Screenshot this page and send it to me as proof 😌💌
            </p>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="footer">Made with 💘 on Streamlit</div>', unsafe_allow_html=True)

# Optional: show a tiny admin hint only to you
if show_custom:
    st.caption("🔐 Admin mode enabled (sidebar unlocked). Share the normal link without ?key=...")
