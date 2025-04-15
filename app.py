
import streamlit as st
import random
import time

st.set_page_config(page_title="Reactie Spelmenu", layout="centered")

st.title("🎮 Reactietrainer Spelmenu 🎮")

keuze = st.selectbox("Kies een spel", ["-- Selecteer --", "Klassieke Reactietest", "Dynamische Positie Test", "9-Vak Lampjesspel"])

# Score opslag
if "scores" not in st.session_state:
    st.session_state.scores = {
        "Klassieke Reactietest": [],
        "Dynamische Positie Test": [],
        "9-Vak Lampjesspel": []
    }

# Klassieke Reactietest
if keuze == "Klassieke Reactietest":
    st.subheader("⚡ Klassieke Reactietest")
    if "starttijd" not in st.session_state:
        st.session_state.starttijd = None

    if st.button("Start test"):
        wachttijd = random.uniform(2, 5)
        st.session_state.starttijd = time.time() + wachttijd
        st.experimental_rerun()

    if st.session_state.starttijd:
        if time.time() >= st.session_state.starttijd:
            if st.button("Klik nu!"):
                tijd = int((time.time() - st.session_state.starttijd) * 1000)
                st.success(f"Reactietijd: {tijd} ms")
                st.session_state.scores[keuze].append(tijd)
                st.session_state.starttijd = None
        else:
            st.info("Wachten...")

# Dynamische Positie Test
elif keuze == "Dynamische Positie Test":
    st.subheader("📍 Dynamische Positie Test")
    if "dp_start" not in st.session_state:
        st.session_state.dp_start = None
        st.session_state.dp_positie = "center"

    if st.button("Start ronde"):
        wachttijd = random.uniform(2, 5)
        st.session_state.dp_start = time.time() + wachttijd
        st.session_state.dp_positie = random.choice(["left", "center", "right"])
        st.experimental_rerun()

    if st.session_state.dp_start:
        if time.time() >= st.session_state.dp_start:
            col1, col2, col3 = st.columns(3)
            target_col = col1 if st.session_state.dp_positie == "left" else col2 if st.session_state.dp_positie == "center" else col3
            with target_col:
                if st.button("KLIK!"):
                    tijd = int((time.time() - st.session_state.dp_start) * 1000)
                    st.success(f"Reactietijd: {tijd} ms")
                    st.session_state.scores[keuze].append(tijd)
                    st.session_state.dp_start = None

# 9-Vak Lampjesspel
elif keuze == "9-Vak Lampjesspel":
    st.subheader("🔲 9-Vak Lampjesspel")
    if "lampje_index" not in st.session_state:
        st.session_state.lampje_index = None
        st.session_state.lampje_start = None

    if st.button("Start ronde"):
        st.session_state.lampje_index = random.randint(0, 8)
        st.session_state.lampje_start = time.time()
        st.experimental_rerun()

    cols = st.columns(3)
    for i in range(9):
        kleur = "#ddd"
        if i == st.session_state.lampje_index:
            kleur = "lime"
        with cols[i % 3]:
            knop = st.button(" ", key=f"lampje_{i}", use_container_width=True)
            if knop:
                if i == st.session_state.lampje_index:
                    tijd = int((time.time() - st.session_state.lampje_start) * 1000)
                    st.success(f"Reactietijd: {tijd} ms")
                    st.session_state.scores[keuze].append(tijd)
                    st.session_state.lampje_index = None
            st.markdown(f"""
            <div style='height: 60px; background-color: {kleur}; border-radius: 8px;'></div>
            """, unsafe_allow_html=True)

# Scoreoverzicht
if keuze != "-- Selecteer --" and st.session_state.scores[keuze]:
    st.markdown("### Jouw scores:")
    st.write(f"Laatste: {st.session_state.scores[keuze][-1]} ms")
    st.write(f"Gemiddelde: {sum(st.session_state.scores[keuze]) // len(st.session_state.scores[keuze])} ms")
    st.line_chart(st.session_state.scores[keuze][-10:])
