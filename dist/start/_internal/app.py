# app.py — Stellar Dance (Streamlit UI)
import streamlit as st
import subprocess
import json
import os
import matplotlib.pyplot as plt
# =============================
# 🎓 EDUCATION MODE (with toggle)
# =============================
import streamlit as st
from typing import List, Dict

def _edu_faq() -> Dict[str, str]:
    return {
        "What is a binary star?":
            "A system of two stars bound by gravity that orbit their common center of mass (barycenter). "
            "Many binaries are discovered via radial-velocity shifts or eclipses (light dips).",
        "What is a triple star system?":
            "Three stars gravitationally bound. Often hierarchical: a close inner binary orbited by a third star farther out.",
        "What is the barycenter?":
            "The center of mass of a system. In binaries both stars orbit this point; it’s closer to the more massive star.",
        "What is the Roche lobe?":
            "The region around a star in a binary where material is gravitationally bound to that star. "
            "When a star fills its Roche lobe, gas can flow to its companion (mass transfer).",
        "Why do stars transfer mass?":
            "If one star expands (e.g., as a red giant) and overflows its Roche lobe, its outer layers can stream to the companion.",
        "Kepler’s laws (very short)":
            "1) Orbits are ellipses with the barycenter at a focus. "
            "2) Equal areas in equal times. "
            "3) Period relates to semimajor axis and total mass.",
        "How does mass affect orbits?":
            "Greater total mass → stronger gravity → for the same separation, higher orbital speeds and shorter periods.",
        "What determines star color?":
            "Surface temperature: hotter stars look blue/white; cooler stars look orange/red. Spectral types run O–B–A–F–G–K–M.",
        "How are exoplanet hosts relevant?":
            "Their mass/radius/temperature shape planetary environments and can be used as presets in your simulations.",
    }

def _edu_quiz() -> List[dict]:
    return [
        {"q": "In a binary system, where do the stars orbit?",
         "opts": ["Around the more massive star", "Around the center of mass", "In perfect circles around nothing"],
         "ans": 1,
         "why": "Both stars orbit their common center of mass (barycenter)."},
        {"q": "What happens when a star overfills its Roche lobe?",
         "opts": ["It spins faster", "It becomes cooler", "It transfers mass to its companion"],
         "ans": 2,
         "why": "Matter flows through the inner Lagrange point to the companion."},
        {"q": "Which spectral type is generally hottest?",
         "opts": ["K-type", "A-type", "O-type"],
         "ans": 2,
         "why": "O-type stars are the hottest and most massive; M-type are the coolest."},
        {"q": "Increasing total mass (keeping separation ~same) makes orbital periods…",
         "opts": ["Longer", "Shorter", "Unchanged"],
         "ans": 1,
         "why": "Stronger gravity → higher speeds → shorter orbital periods."},
        {"q": "A hierarchical triple most commonly means…",
         "opts": ["Three stars all equally spaced", "Two close stars plus a third farther out", "A star with two planets"],
         "ans": 1,
         "why": "An inner tight binary orbited by a distant third star is dynamically stable."},
    ]

def _edu_glossary() -> Dict[str, str]:
    return {
        "Barycenter": "The system’s center of mass about which bodies orbit.",
        "Periastron": "Point of closest approach in a stellar orbit.",
        "Apastron": "Point of farthest separation in a stellar orbit.",
        "Spectral Type": "Classification (O–M) tied to temperature and color.",
        "Mass Transfer": "Flow of material from one star to another, via Roche-lobe overflow.",
        "Eclipsing Binary": "Binary aligned so stars pass in front of each other, causing brightness dips.",
        "Radial Velocity": "Line-of-sight speed measured via Doppler shift; reveals orbits and companions.",
        "Light Curve": "Brightness vs. time; eclipses or transits create characteristic dips.",
    }

def _match_answer(query: str) -> str:
    if not query or not query.strip():
        return "Try asking: *What is a binary star?* or *What is the Roche lobe?*"

    q = query.lower()
    faqs = _edu_faq()
    mapping = {
        "binary": "What is a binary star?",
        "double": "What is a binary star?",
        "triple": "What is a triple star system?",
        "barycenter": "What is the barycenter?",
        "roche": "What is the Roche lobe?",
        "mass transfer": "Why do stars transfer mass?",
        "kepler": "Kepler’s laws (very short)",
        "color": "What determines star color?",
        "spectral": "What determines star color?",
        "exoplanet": "How are exoplanet hosts relevant?",
    }
    for kw, key in mapping.items():
        if kw in q:
            return f"**{key}**\n\n{faqs[key]}"
    for key in faqs:
        if any(w in q for w in key.lower().split()):
            return f"**{key}**\n\n{faqs[key]}"
    return "I couldn't find a match. Try keywords like *binary*, *triple*, *barycenter*, *Roche*, *Kepler*."

def education_mode():
    st.markdown("## 🎓 Education Mode")
    tabs = st.tabs(["FAQs", "Quiz", "Glossary", "Ask a Question"])

    # FAQs
    with tabs[0]:
        for title, text in _edu_faq().items():
            with st.expander(f"❓ {title}", expanded=False):
                st.write(text)

    # Quiz
    with tabs[1]:
        if "quiz_score" not in st.session_state:
            st.session_state.quiz_score = 0
        if "quiz_seen" not in st.session_state:
            st.session_state.quiz_seen = [False] * len(_edu_quiz())

        for i, item in enumerate(_edu_quiz()):
            st.markdown(f"**Q{i+1}. {item['q']}**")
            choice = st.radio(
                "Select one:",
                options=[f"A) {item['opts'][0]}", f"B) {item['opts'][1]}", f"C) {item['opts'][2]}"],
                key=f"quiz_{i}",
                index=None
            )
            if st.button(f"Check Q{i+1}", key=f"check_{i}"):
                if choice is None:
                    st.warning("Choose an option first.")
                else:
                    chosen_idx = ["A", "B", "C"].index(choice[0])
                    correct = chosen_idx == item["ans"]
                    if correct and not st.session_state.quiz_seen[i]:
                        st.session_state.quiz_score += 1
                        st.session_state.quiz_seen[i] = True
                    st.success("✅ Correct!" if correct else "❌ Not quite.")
                    st.info(item["why"])

        total = len(_edu_quiz())
        st.markdown(f"**Score:** {st.session_state.quiz_score} / {total}")
        if st.button("🔁 Reset Quiz"):
            st.session_state.quiz_score = 0
            st.session_state.quiz_seen = [False] * total
            st.rerun()

    # Glossary
    with tabs[2]:
        for term, definition in _edu_glossary().items():
            st.markdown(f"- **{term}** — {definition}")

    # Ask
    with tabs[3]:
        q = st.text_input("Ask something (e.g., 'Roche lobe', 'binary star')")
        if st.button("Answer"):
            st.write(_match_answer(q))

# 🎓 Toggle to show/hide Education Mode
try:
    show_edu = st.toggle("🎓 Enable Education Mode", value=True, key="edu_toggle")
except AttributeError:
    show_edu = st.checkbox("🎓 Enable Education Mode", value=True, key="edu_toggle")

if show_edu:
    education_mode()
# Databases
from astroquery.nasa_exoplanet_archive import NasaExoplanetArchive
from astroquery.simbad import Simbad

# Physics constants from your engine
from gravity import MS, RS

# -----------------------------
# Streamlit page config
# -----------------------------
st.set_page_config(page_title="🌌 Stellar Dance", page_icon="✨", layout="centered")
STAR_CSS = """
<style>
@keyframes driftStars {
  from { background-position: 0 0, 0 0, 0 0, 0 0, 0 0; }
  to   { background-position: 1000px 500px, -800px 400px, 600px -300px, -500px -250px, 300px 200px; }
}
.stApp {
  background-color: #000010 !important;
  background-image:
    radial-gradient(1px 1px at 20% 30%, rgba(255,255,255,0.55) 0, transparent 2px),
    radial-gradient(1.5px 1.5px at 80% 20%, rgba(255,255,255,0.45) 0, transparent 2px),
    radial-gradient(1.8px 1.8px at 60% 70%, rgba(255,255,255,0.55) 0, transparent 2px),
    radial-gradient(1px 1px at 30% 80%, rgba(255,255,255,0.35) 0, transparent 2px),
    radial-gradient(2px 2px at 70% 50%, rgba(255,255,255,0.55) 0, transparent 3px);
  background-size: 800px 600px;
  background-attachment: fixed;
  animation: driftStars 120s linear infinite;
}
[data-testid="stSidebar"] > div {
  background-color: rgba(0,0,0,0.6) !important;
  backdrop-filter: blur(2px);
}
h1, h2, h3, h4, h5, h6, p, label, span, div, code, .stMarkdown, .stCaption, .stTextInput label {
  color: #f0f0f0 !important;
}
.block-container { background: transparent !important; }
</style>
"""
st.markdown(STAR_CSS, unsafe_allow_html=True)

st.title("🌟 Stellar Dance — Binary & Triple Star Interaction Visualizer")
st.write("Simulate and visualize binary or triple star systems with real NASA/SIMBAD parameters.")

# -----------------------------
# System size (2 vs 3)
# -----------------------------
system_type = st.radio("Select system type:", ["Binary System (2 stars)", "Triple System (3 stars)"])
num_stars = 2 if "Binary" in system_type else 3

# -----------------------------
# Session state init/resize
# -----------------------------
if "stars" not in st.session_state:
    st.session_state["stars"] = [{"mass": float(MS), "radius": float(RS), "color": "#FFD700"} for _ in range(num_stars)]
elif len(st.session_state["stars"]) < num_stars:
    for _ in range(num_stars - len(st.session_state["stars"])):
        st.session_state["stars"].append({"mass": float(MS), "radius": float(RS), "color": "#FFD700"})
elif len(st.session_state["stars"]) > num_stars:
    st.session_state["stars"] = st.session_state["stars"][:num_stars]

# -----------------------------
# Quick presets
# -----------------------------
st.subheader("✨ Quick Add: Popular Stars (presets)")
preset_stars = {
    "Sun": {"mass": MS, "radius": RS, "color": "#FFD700"},
    "Sirius A": {"mass": 2.06 * MS, "radius": 1.71 * RS, "color": "#BFD9FF"},
    "Sirius B": {"mass": 1.02 * MS, "radius": 0.0084 * RS, "color": "#A4A9FF"},
    "Betelgeuse": {"mass": 20 * MS, "radius": 887 * RS, "color": "#FF4500"},
    "Proxima Centauri": {"mass": 0.122 * MS, "radius": 0.1542 * RS, "color": "#FF6F91"},
    "Rigel": {"mass": 21 * MS, "radius": 78.9 * RS, "color": "#87CEFA"},
}

col1, col2 = st.columns(2)
with col1:
    preset_choice = st.selectbox("Select a preset star:", list(preset_stars.keys()))
with col2:
    star_target = st.selectbox("Apply to which star?", [f"Star {i+1}" for i in range(num_stars)])

if st.button("Add preset star"):
    idx = int(star_target.split()[-1]) - 1
    selected_star = preset_stars[preset_choice]
    st.session_state["stars"][idx] = {
        "mass": float(selected_star["mass"]),
        "radius": float(selected_star["radius"]),
        "color": selected_star["color"],
    }
    st.success(f"✅ Applied parameters: {preset_choice} → {star_target}")
    st.rerun()  # instant refresh

# -----------------------------
# Databases: NASA & SIMBAD
# -----------------------------
st.subheader("🛰️ Databases")

tab_nasa, tab_simbad = st.tabs(["NASA Exoplanet Archive", "SIMBAD"])

def fetch_star_params_from_nasa(hostname: str):
    """
    Query Planetary Systems tables (PS/PSComppars) for host star mass/radius.
    Returns (mass_kg, radius_m, resolved_hostname). Raises ValueError if not found.
    """
    name = (hostname or "").strip()
    if not name:
        raise ValueError("Empty star name.")

    tables = ("pscomppars", "ps")
    select = "hostname,st_mass,st_rad"

    for table in tables:
        # exact
        res = NasaExoplanetArchive.query_criteria(
            table=table, select=select, where=f"upper(hostname)=upper('{name}')"
        )
        # prefix
        if len(res) == 0:
            res = NasaExoplanetArchive.query_criteria(
                table=table, select=select, where=f"upper(hostname) LIKE upper('{name}%')"
            )

        if len(res) > 0:
            df = res.to_pandas().dropna(subset=["st_mass", "st_rad"])
            if not df.empty:
                row = df.iloc[0]
                return float(row["st_mass"]) * MS, float(row["st_rad"]) * RS, str(row["hostname"])

    raise ValueError("No mass/radius found for this hostname in PS tables.")

with tab_nasa:
    c1, c2 = st.columns([2, 1])
    with c1:
        nasa_name = st.text_input("Host star name (e.g., Kepler-10, HD 209458, WASP-12)")
    with c2:
        nasa_apply_to = st.selectbox("Apply to:", [f"Star {i+1}" for i in range(num_stars)], key="nasa_apply")

    if st.button("🔍 Fetch from NASA"):
        try:
            m, r, resolved = fetch_star_params_from_nasa(nasa_name)
            idx = int(nasa_apply_to.split()[-1]) - 1
            st.session_state["stars"][idx]["mass"] = float(m)
            st.session_state["stars"][idx]["radius"] = float(r)
            st.session_state["stars"][idx]["color"] = "#FFD700"
            st.success(f"✅ NASA PS data loaded for {resolved} → Star {idx+1}")
            st.info(f"Mass: {m:.3e} kg   |   Radius: {r:.3e} m")
            st.rerun()  # instant refresh
        except Exception as e:
            st.error(f"⚠️ NASA query failed: {e}")
            st.caption("Tip: try the system name (hostname), e.g., 'Kepler-10' or 'HD 209458'.")

with tab_simbad:
    c1, c2 = st.columns([2, 1])
    with c1:
        simbad_name = st.text_input("Object name (e.g., Vega, Rigel, Betelgeuse)")
    with c2:
        simbad_apply_to = st.selectbox("Apply to:", [f"Star {i+1}" for i in range(num_stars)], key="simbad_apply")

    if st.button("🔭 Query SIMBAD"):
        try:
            s = Simbad()
            s.add_votable_fields("sptype", "flux(V)")
            result = s.query_object(simbad_name)

            if result is None or len(result) == 0:
                st.error("❌ Not found in SIMBAD.")
            else:
                sp = result["SP_TYPE"][0].decode() if "SP_TYPE" in result.colnames and result["SP_TYPE"][0] is not None else "Unknown"
                spectral_map = {
                    "O": (16*MS, 6.6*RS),
                    "B": (2.1*MS, 2.0*RS),
                    "A": (1.75*MS, 1.7*RS),
                    "F": (1.3*MS, 1.3*RS),
                    "G": (1.0*MS, 1.0*RS),
                    "K": (0.8*MS, 0.9*RS),
                    "M": (0.4*MS, 0.5*RS),
                }
                if sp and sp[0] in spectral_map:
                    mass, radius = spectral_map[sp[0]]
                else:
                    mass, radius = 1.0 * MS, 1.0 * RS

                idx = int(simbad_apply_to.split()[-1]) - 1
                st.session_state["stars"][idx]["mass"] = float(mass)
                st.session_state["stars"][idx]["radius"] = float(radius)
                st.session_state["stars"][idx]["color"] = "#FFD700"
                st.success(f"✅ SIMBAD: {simbad_name} (SpT {sp}) → Star {idx+1}")
                st.info(f"Estimated Mass: {mass:.3e} kg   |   Estimated Radius: {radius:.3e} m")
                st.rerun()  # instant refresh
        except Exception as e:
            st.error(f"⚠️ SIMBAD query failed: {type(e).__name__}: {e}")

# -----------------------------
# Custom manual inputs
# -----------------------------
st.subheader("🪐 Enter Custom Star Parameters")
for i in range(num_stars):
    st.markdown(f"### Star {i + 1}")
    st.session_state["stars"][i]["mass"] = st.number_input(
        f"Mass of Star {i + 1} (kg)",
        min_value=float(1e20),
        max_value=float(1e33),
        value=float(st.session_state["stars"][i]["mass"]),
        key=f"mass_{i}",
        step=1e28
    )
    st.session_state["stars"][i]["radius"] = st.number_input(
        f"Radius of Star {i + 1} (m)",
        min_value=float(1e3),
        max_value=float(1e12),
        value=float(st.session_state["stars"][i]["radius"]),
        key=f"radius_{i}",
        step=1e8
    )
    st.session_state["stars"][i]["color"] = st.color_picker(
        f"Color of Star {i + 1}",
        st.session_state["stars"][i]["color"],
        key=f"color_{i}"
    )

# =====================================================
# 📊 Current Star Parameters (Auto-updating)
# =====================================================
st.markdown("---")
st.subheader("📊 Current Star Parameters")

if "stars" in st.session_state and len(st.session_state["stars"]) > 0:
    for i, s in enumerate(st.session_state["stars"], start=1):
        try:
            m_sol = s["mass"] / MS
            r_sol = s["radius"] / RS
        except Exception:
            m_sol, r_sol = float("nan"), float("nan")

        st.markdown(
            f"**Star {i}**  \n"
            f"- Mass: {m_sol:.3g} M☉  \n"
            f"- Radius: {r_sol:.3g} R☉  \n"
            f"- Color: `{s.get('color', '#FFFFFF')}`"
        )
else:
    st.info("No star data yet. Load or apply parameters first.")

# -----------------------------
# Time speed (1000 — 70 000)
# -----------------------------
st.subheader("⏱️ Simulation Time Speed")
time_speed = st.slider(
    "Adjust simulation speed (higher = faster orbits)",
    min_value=1000,
    max_value=70000,
    value=5000,
    step=500
)

# -----------------------------
# Live preview (matplotlib)
# -----------------------------
st.subheader("🌌 System Preview")
fig, ax = plt.subplots(figsize=(5, 5))
ax.set_facecolor("white")

positions = [-1, 1, 0] if num_stars == 3 else [-0.6, 0.6]

max_radius = max(star["radius"] for star in st.session_state["stars"])
scale = 0.4 / (max_radius / RS) if max_radius > 0 else 0.2
scale = max(min(scale, 0.4), 0.05)

# orbit hints
for i in range(num_stars):
    orbit = plt.Circle((0, 0), abs(positions[i]), color="gray", linestyle="--", linewidth=0.6, fill=False)
    ax.add_patch(orbit)

# draw stars
for i in range(num_stars):
    star = st.session_state["stars"][i]
    radius_scaled = (star["radius"] / RS) * scale
    radius_scaled = min(radius_scaled, 0.5)
    circle = plt.Circle((positions[i], 0), radius_scaled, color=star["color"], ec="black", lw=0.5)
    ax.add_patch(circle)
    ax.text(
        positions[i], -0.25 - radius_scaled, f"Star {i+1}",
        color="black", ha="center", fontsize=10, weight="bold"
    )

ax.set_xlim(-2, 2)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect("equal", "box")
ax.axis("off")
st.pyplot(fig)

# -----------------------------
# Launch simulation (external window)
# -----------------------------
st.markdown("### 🌀 Simulation Control")
if st.button("Run Simulation"):
    st.info("Launching Pygame visualization...")

    config = {
        "stars": st.session_state["stars"],
        "time_speed": int(time_speed),
        "system_type": "binary" if num_stars == 2 else "triple"
    }

    with open("user_stars.json", "w", encoding="utf-8") as f:
        json.dump(config, f)

    # Launch gravity engine as a separate process (robust on Windows)
    subprocess.Popen(["python", "gravity.py", "user_stars.json"])
    st.success("Simulation running with your custom parameters! 🪐")

st.markdown("---")
st.caption("Created by Team Stellar Dance for NASA Space Apps Challenge 🌠")

