"""
app.py - Production-Ready Streamlit Interface for Q-Sweep: Entangled Hazard
Track 1: Quantum Games & Interactive Puzzles | Team DOPA (Kartik Jain)
"""
import io
import streamlit as st
import matplotlib.pyplot as plt
from quantum_engine import QuantumSweeperEngine

st.set_page_config(
    page_title="Q-Sweep: Entangled Hazard",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom responsive CSS injection
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        height: 4rem;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.2s ease-in-out;
    }
    .metric-card {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        margin-bottom: 12px;
    }
    .status-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Session initialization
if "engine" not in st.session_state:
    st.session_state.engine = QuantumSweeperEngine()

GRID_SIZE = 3
TOTAL_TILES = GRID_SIZE * GRID_SIZE
ENTANGLED_PAIRS = {0: 1, 1: 0, 4: 5, 5: 4}

def init_game():
    st.session_state.revealed = [False] * TOTAL_TILES
    st.session_state.board_state = [None] * TOTAL_TILES
    st.session_state.game_over = False
    st.session_state.game_won = False
    st.session_state.score = 0
    st.session_state.last_circuit = None
    st.session_state.log = ["Initialized grid in quantum state |ψ⟩."]

if "revealed" not in st.session_state:
    init_game()

# Sidebar: Controls & Rules
with st.sidebar:
    st.header("⚙️ Game Controls")
    if st.button("🔄 Reset / New Game", key="btn_reset"):
        init_game()
        st.rerun()

    st.markdown("---")
    st.subheader("📖 Quantum Game Rules")
    with st.expander("How does Superposition work?", expanded=False):
        st.write(
            "Individual tiles are unobserved prior to your click. An $R_y(\\theta)$ gate "
            "places the tile into superposition. When probed, measurement collapses the wavefunction "
            "into Safe (|0⟩) or Mine (|1⟩) in real time."
        )

    with st.expander("How does Entanglement work?", expanded=True):
        st.write(
            "Tiles **(0, 1)** and **(4, 5)** share a Bell State $|\\Phi^+\\rangle = \\frac{|00\\rangle + |11\\rangle}{\\sqrt{2}}$. "
            "Probing either tile collapses **both** tiles simultaneously into identical states."
        )

    st.markdown("---")
    st.caption("**Team DOPA** | Qiskit Fall Fest 2026")

# Header Section
st.title("⚛️ Q-Sweep: Entangled Hazard")
st.markdown(
    "A quantum hazard puzzle powered by **Qiskit AerSimulator**. "
    "Mines are not pre-calculated—they are brought into reality through quantum measurement collapse."
)

# Top Metrics Row
m_col1, m_col2, m_col3 = st.columns(3)
with m_col1:
    st.metric("Player Score", st.session_state.score)
with m_col2:
    revealed_count = sum(st.session_state.revealed)
    st.metric("Tiles Cleared", f"{revealed_count} / {TOTAL_TILES}")
with m_col3:
    status_label = "💥 Detonated" if st.session_state.game_over else ("🏆 Cleared" if st.session_state.game_won else "🟢 In Superposition")
    st.metric("System State", status_label)

st.markdown("---")

def handle_click(idx: int):
    if st.session_state.revealed[idx] or st.session_state.game_over or st.session_state.game_won:
        return

    engine = st.session_state.engine

    if idx in ENTANGLED_PAIRS:
        partner = ENTANGLED_PAIRS[idx]
        ma, mb, qc = engine.generate_bell_pair()

        st.session_state.revealed[idx] = True
        st.session_state.revealed[partner] = True
        st.session_state.board_state[idx] = "💥 Mine" if ma == 1 else "🟢 Safe"
        st.session_state.board_state[partner] = "💥 Mine" if mb == 1 else "🟢 Safe"
        st.session_state.last_circuit = qc

        if ma == 1:
            st.session_state.game_over = True
            st.session_state.log.append(f"💥 Bell pair ({idx}, {partner}) collapsed into MINES!")
        else:
            st.session_state.score += 2
            st.session_state.log.append(f"⚡ Bell pair ({idx}, {partner}) collapsed into SAFE states.")
    else:
        is_mine, qc = engine.probe_superposition_tile(mine_prob=0.30)
        st.session_state.revealed[idx] = True
        st.session_state.last_circuit = qc

        if is_mine == 1:
            st.session_state.board_state[idx] = "💥 Mine"
            st.session_state.game_over = True
            st.session_state.log.append(f"💥 Tile {idx} collapsed into a MINE!")
        else:
            st.session_state.board_state[idx] = "🟢 Safe"
            st.session_state.score += 1
            st.session_state.log.append(f"🟢 Tile {idx} measured SAFE.")

    if not st.session_state.game_over and all(st.session_state.revealed):
        st.session_state.game_won = True
        st.session_state.log.append("🏆 All tiles collapsed without detonating a lethal mine!")

# Main Grid & Telemetry
col_grid, col_circuit = st.columns([1.1, 0.9])

with col_grid:
    st.subheader("Quantum Hazard Grid")
    st.info("🔗 **Tile pairs (0, 1) and (4, 5) share Bell Entanglement.** Measuring one collapses both.")

    for row in range(GRID_SIZE):
        row_cols = st.columns(GRID_SIZE)
        for col in range(GRID_SIZE):
            idx = row * GRID_SIZE + col
            with row_cols[col]:
                if not st.session_state.revealed[idx]:
                    entangled_tag = " [E]" if idx in ENTANGLED_PAIRS else ""
                    if st.button(f"❓ Tile {idx}{entangled_tag}", key=f"t_{idx}", disabled=st.session_state.game_over or st.session_state.game_won):
                        handle_click(idx)
                        st.rerun()
                else:
                    st.button(f"{st.session_state.board_state[idx]}", key=f"d_{idx}", disabled=True)

    if st.session_state.game_over:
        st.error(f"☠️ Detonation! Game Over. Final Score: {st.session_state.score}")
    elif st.session_state.game_won:
        st.success(f"🏆 Victory! You cleared the quantum minefield. Final Score: {st.session_state.score}")

with col_circuit:
    st.subheader("Circuit Telemetry & Teleportation")
    if st.session_state.last_circuit is not None:
        fig = st.session_state.last_circuit.draw(output="mpl")
        st.pyplot(fig)

        # In-memory circuit diagram download
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        st.download_button(
            label="📥 Download Circuit Diagram",
            data=buf.getvalue(),
            file_name="quantum_circuit.png",
            mime="image/png"
        )
        plt.close(fig)
    else:
        st.info("Click any grid tile to execute its underlying Qiskit circuit.")

    st.subheader("Measurement History")
    for item in reversed(st.session_state.log[-5:]):
        st.caption(f"• {item}")