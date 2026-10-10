"""
app.py
Interactive Streamlit UI for Q-Sweep: Entangled Hazard.
Run via: streamlit run src/app.py
"""
import streamlit as st
import matplotlib.pyplot as plt
from quantum_engine import QuantumSweeperEngine

st.set_page_config(page_title="Q-Sweep: Entangled Hazard", page_icon="⚛️", layout="wide")

st.title("⚛️ Q-Sweep: Entangled Hazard")
st.caption("Track 1: Quantum Games & Interactive Puzzles | Team DOPA")

# Initialize Engine
if "engine" not in st.session_state:
    st.session_state.engine = QuantumSweeperEngine()

GRID_SIZE = 3
TOTAL_TILES = GRID_SIZE * GRID_SIZE

# Entangled pairs across the grid: (0, 1) and (4, 5)
ENTANGLED_MAP = {0: 1, 1: 0, 4: 5, 5: 4}

if "revealed" not in st.session_state or st.sidebar.button("🔄 Reset / New Game"):
    st.session_state.revealed = [False] * TOTAL_TILES
    st.session_state.board_state = [None] * TOTAL_TILES
    st.session_state.game_over = False
    st.session_state.score = 0
    st.session_state.last_circuit = None
    st.session_state.log = ["Board initialized with superposed and entangled qubits."]

def handle_cell_click(idx: int):
    if st.session_state.revealed[idx] or st.session_state.game_over:
        return

    engine = st.session_state.engine

    if idx in ENTANGLED_MAP:
        partner_idx = ENTANGLED_MAP[idx]
        mine_curr, mine_partner, qc = engine.generate_bell_pair()

        st.session_state.revealed[idx] = True
        st.session_state.revealed[partner_idx] = True
        st.session_state.board_state[idx] = "💥 Mine" if mine_curr == 1 else "🟢 Safe"
        st.session_state.board_state[partner_idx] = "💥 Mine" if mine_partner == 1 else "🟢 Safe"
        st.session_state.last_circuit = qc

        if mine_curr == 1:
            st.session_state.game_over = True
            st.session_state.log.append(f"💥 Wavefunction collapsed: Entangled pair ({idx}, {partner_idx}) detonated!")
        else:
            st.session_state.score += 2
            st.session_state.log.append(f"⚡ Bell State collapse: Tiles ({idx}, {partner_idx}) safely resolved!")
    else:
        is_mine, qc = engine.probe_superposition_tile(mine_prob=0.30)
        st.session_state.revealed[idx] = True
        st.session_state.last_circuit = qc

        if is_mine == 1:
            st.session_state.board_state[idx] = "💥 Mine"
            st.session_state.game_over = True
            st.session_state.log.append(f"💥 Tile {idx} collapsed into a Mine! Game over.")
        else:
            st.session_state.board_state[idx] = "🟢 Safe"
            st.session_state.score += 1
            st.session_state.log.append(f"🟢 Tile {idx} measured: Safe.")

col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("3x3 Hazard Grid")
    st.info("🔗 **Pairs (0, 1) and (4, 5) share Bell Entanglement.** Observing one collapses both instantaneously.")

    for row in range(GRID_SIZE):
        cols = st.columns(GRID_SIZE)
        for col in range(GRID_SIZE):
            idx = row * GRID_SIZE + col
            with cols[col]:
                if not st.session_state.revealed[idx]:
                    if st.button(f"❓ Tile {idx}", key=f"btn_{idx}", use_container_width=True):
                        handle_cell_click(idx)
                        st.rerun()
                else:
                    st.button(f"{st.session_state.board_state[idx]}", key=f"lbl_{idx}", disabled=True, use_container_width=True)

    if st.session_state.game_over:
        st.error(f"☠️ Detonation! Game Over. Final Score: {st.session_state.score}")
    elif all(st.session_state.revealed):
        st.success(f"🏆 Grid Cleared! Surviving Score: {st.session_state.score}")

with col2:
    st.subheader("Quantum Circuit Telemetry")
    if st.session_state.last_circuit is not None:
        fig = st.session_state.last_circuit.draw(output="mpl")
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("Select any tile to execute a quantum circuit and inspect state collapse telemetry.")

    st.subheader("Measurement History")
    for event in reversed(st.session_state.log[-5:]):
        st.caption(event)