
import streamlit as st
import random
import time

st.set_page_config(page_title="Reactie Spelmenu", layout="centered")
st.title("🎮 Reactietrainer Spelmenu 🎮")

keuze = st.selectbox("Kies een spel", ["-- Selecteer --", "Klassieke Reactietest", "Dynamische Positie Test", "9-Vak Lampjesspel"])

if "scores" not in st.session_state:
    st.session_state.scores = {
        "Klassieke Reactietest": [],
        "Dynamische Positie Test": [],
        "9-Vak Lampjesspel": []
    }

# --- Klassieke Reactietest ---
if keuze == "Klassieke Reactietest":
    st.subheader("⚡ Klassieke Reactietest")
    if "klassiek_gewacht" not in st.session_state:
        st.session_state.klassiek_gewacht = False
        st.session_state.klassiek_starttijd = 0

    if not st.session_state.klassiek_gewacht:
        if st.button("Start test"):
            wachttijd = random.uniform(2, 5)
            st.session_state.klassiek_starttijd = time.time() + wachttijd
            st.session_state.klassiek_gewacht = True
            st.session_state.klassiek_reactie = None

    if st.session_state.klassiek_gewacht:
        if time.time() >= st.session_state.klassiek_starttijd:
            if st.button("Klik nu!"):
                reactietijd = int((time.time() - st.session_state.klassiek_starttijd) * 1000)
                st.success(f"Reactietijd: {reactietijd} ms")
                st.session_state.scores[keuze].append(reactietijd)
                st.session_state.klassiek_gewacht = False
        else:
            st.info("Wachten...")

# --- Dynamische Positie Test ---
elif keuze == "Dynamische Positie Test":
    st.subheader("📍 Dynamische Positie Test")
    if "dyn_starttijd" not in st.session_state:
        st.session_state.dyn_starttijd = 0
        st.session_state.dyn_pos = None
        st.session_state.dyn_active = False

    if not st.session_state.dyn_active:
        if st.button("Start ronde"):
            wachttijd = random.uniform(2, 5)
            st.session_state.dyn_starttijd = time.time() + wachttijd
            st.session_state.dyn_pos = random.choice(["left", "center", "right"])
            st.session_state.dyn_active = True

    if st.session_state.dyn_active and time.time() >= st.session_state.dyn_starttijd:
        col1, col2, col3 = st.columns(3)
        cols = {"left": col1, "center": col2, "right": col3}
        with cols[st.session_state.dyn_pos]:
            if st.button("KLIK!"):
                tijd = int((time.time() - st.session_state.dyn_starttijd) * 1000)
                st.success(f"Reactietijd: {tijd} ms")
                st.session_state.scores[keuze].append(tijd)
                st.session_state.dyn_active = False

# --- 9-Vak Lampjesspel ---
elif keuze == "9-Vak Lampjesspel":
    st.subheader("🔲 9-Vak Lampjesspel")
    if "lamp_positie" not in st.session_state:
        st.session_state.lamp_positie = None
        st.session_state.lamp_starttijd = None

    if st.button("Start ronde"):
        st.session_state.lamp_positie = random.randint(0, 8)
        st.session_state.lamp_starttijd = time.time()

    cols = st.columns(3)
    for i in range(9):
        kleur = "#ddd"
        if st.session_state.lamp_positie == i:
            kleur = "lime"
        with cols[i % 3]:
            if st.button(" ", key=f"lampje_{i}", use_container_width=True):
                if st.session_state.lamp_positie == i:
                    tijd = int((time.time() - st.session_state.lamp_starttijd) * 1000)
                    st.success(f"Reactietijd: {tijd} ms")
                    st.session_state.scores[keuze].append(tijd)
                    st.session_state.lamp_positie = None
            st.markdown(f"""<div style='height: 60px; background-color: {kleur}; border-radius: 8px;'></div>""", unsafe_allow_html=True)

# --- Scoreoverzicht ---
if keuze != "-- Selecteer --" and st.session_state.scores[keuze]:
    st.markdown("### Jouw scores:")
    st.write(f"Laatste: {st.session_state.scores[keuze][-1]} ms")
    st.write(f"Gemiddelde: {sum(st.session_state.scores[keuze]) // len(st.session_state.scores[keuze])} ms")
    st.line_chart(st.session_state.scores[keuze][-10:])
