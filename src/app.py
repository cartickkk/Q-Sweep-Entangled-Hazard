"""
app.py - High-Impact Interactive Edition for Q-Sweep: Entangled Hazard
Track 1: Quantum Games & Interactive Puzzles | Team DOPA (Kartik Jain)
"""
import io
import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
from quantum_engine import QuantumSweeperEngine

st.set_page_config(
    page_title="Q-Sweep: Entangled Hazard",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Dynamic Quantum Aurora Theme & 3D Flip CSS
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Space+Grotesk:wght@500;700&family=JetBrains+Mono:wght@500;700&display=swap');

    /* Global Dark Mesh Gradient */
    .stApp {
        background: radial-gradient(at 0% 0%, #111827 0px, transparent 50%),
                    radial-gradient(at 100% 0%, #1e1b4b 0px, transparent 50%),
                    radial-gradient(at 50% 100%, #030712 0px, transparent 80%),
                    #090d16 !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #f1f5f9;
    }

    /* Headings */
    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }

    .badge-aer {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        background: rgba(56, 189, 248, 0.12);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.4);
        padding: 3px 10px;
        border-radius: 999px;
        font-weight: 700;
        vertical-align: middle;
        letter-spacing: 0.05em;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.25);
    }

    /* Top Stats Ribbon */
    div[data-testid="stMetric"] {
        background: rgba(17, 24, 39, 0.75) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        padding: 12px 18px !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4) !important;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        border-color: rgba(129, 140, 248, 0.4) !important;
        transform: translateY(-2px);
    }
    div[data-testid="stMetricLabel"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.72rem !important;
        color: #94a3b8 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
    }
    div[data-testid="stMetricValue"] {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #f8fafc !important;
    }

    /* Main Container Cards */
    .quantum-card {
        background: rgba(15, 23, 42, 0.65);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 12px 36px rgba(0, 0, 0, 0.45);
        margin-bottom: 20px;
    }

    .card-header-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        color: #e2e8f0;
    }

    .entangle-flag {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(217, 119, 6, 0.3) 100%);
        border: 1px solid #f59e0b;
        color: #fde68a;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 999px;
        box-shadow: 0 0 15px rgba(245, 158, 11, 0.25);
        animation: pulseAmber 2.5s infinite;
    }

    @keyframes pulseAmber {
        0%, 100% { box-shadow: 0 0 12px rgba(245, 158, 11, 0.25); }
        50% { box-shadow: 0 0 22px rgba(245, 158, 11, 0.55); }
    }

    /* 3D Animated Grid Buttons */
    div[data-testid="column"] button {
        height: 5.2rem !important;
        border-radius: 12px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.02em !important;
        transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%) !important;
        color: #f8fafc !important;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.35) !important;
    }

    div[data-testid="column"] button:hover:not(:disabled) {
        transform: translateY(-4px) scale(1.03) !important;
        border-color: #38bdf8 !important;
        background: linear-gradient(180deg, #1e3a5f 0%, #0f233f 100%) !important;
        color: #38bdf8 !important;
        box-shadow: 0 10px 25px rgba(56, 189, 248, 0.35) !important;
    }

    /* Sidebar Refinement */
    section[data-testid="stSidebar"] {
        background-color: #0b1120 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Dynamic Browser Audio Synthesizer (AudioContext FX)
# ---------------------------------------------------------
def play_sound_fx(fx: str):
    sounds = {
        "safe": """
            const ac = new (window.AudioContext || window.webkitAudioContext)();
            const o = ac.createOscillator();
            const g = ac.createGain();
            o.type = 'sine';
            o.frequency.setValueAtTime(523.25, ac.currentTime); // C5
            o.frequency.exponentialRampToValueAtTime(783.99, ac.currentTime + 0.15); // G5
            g.gain.setValueAtTime(0.15, ac.currentTime);
            g.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + 0.2);
            o.connect(g); g.connect(ac.destination);
            o.start(); o.stop(ac.currentTime + 0.2);
        """,
        "entangle": """
            const ac = new (window.AudioContext || window.webkitAudioContext)();
            const o1 = ac.createOscillator();
            const o2 = ac.createOscillator();
            const g = ac.createGain();
            o1.type = 'triangle'; o2.type = 'sine';
            o1.frequency.setValueAtTime(440, ac.currentTime);
            o1.frequency.exponentialRampToValueAtTime(880, ac.currentTime + 0.25);
            o2.frequency.setValueAtTime(554.37, ac.currentTime);
            o2.frequency.exponentialRampToValueAtTime(1108.73, ac.currentTime + 0.25);
            g.gain.setValueAtTime(0.12, ac.currentTime);
            g.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + 0.3);
            o1.connect(g); o2.connect(g); g.connect(ac.destination);
            o1.start(); o2.start(); o1.stop(ac.currentTime + 0.3); o2.stop(ac.currentTime + 0.3);
        """,
        "mine": """
            const ac = new (window.AudioContext || window.webkitAudioContext)();
            const o = ac.createOscillator();
            const g = ac.createGain();
            o.type = 'sawtooth';
            o.frequency.setValueAtTime(120, ac.currentTime);
            o.frequency.exponentialRampToValueAtTime(30, ac.currentTime + 0.4);
            g.gain.setValueAtTime(0.22, ac.currentTime);
            g.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + 0.4);
            o.connect(g); g.connect(ac.destination);
            o.start(); o.stop(ac.currentTime + 0.4);
        """
    }
    if fx in sounds:
        components.html(f"<script>{sounds[fx]}</script>", height=0, width=0)

# ---------------------------------------------------------
# Session Initialization
# ---------------------------------------------------------
if "engine" not in st.session_state:
    st.session_state.engine = QuantumSweeperEngine()

GRID_SIZE = 3
TOTAL_TILES = GRID_SIZE * GRID_SIZE
ENTANGLED_MAP = {0: 1, 1: 0, 4: 5, 5: 4}

def reset_game():
    st.session_state.revealed = [False] * TOTAL_TILES
    st.session_state.board_state = [None] * TOTAL_TILES
    st.session_state.game_over = False
    st.session_state.game_won = False
    st.session_state.score = 0
    st.session_state.last_circuit = None
    st.session_state.sound_to_play = None
    st.session_state.log = ["Register initialized in ground state |000000000⟩."]

if "revealed" not in st.session_state:
    reset_game()

if st.session_state.sound_to_play:
    play_sound_fx(st.session_state.sound_to_play)
    st.session_state.sound_to_play = None

# ---------------------------------------------------------
# Sidebar: Setup & Rules
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### 🎛 QUANTUM CONTROL")
    if st.button("↻ Restart Quantum Experiment", use_container_width=True):
        reset_game()
        st.rerun()

    st.markdown("---")
    st.markdown("### 🧬 PHYSICS FORMALISM")
    with st.expander("Superposition (|ψ⟩)", expanded=False):
        st.caption(
            "Individual tiles rotate through $R_y(\\theta)$ into $|\\psi\\rangle = \\cos(\\theta/2)|0\\rangle + \\sin(\\theta/2)|1\\rangle$. "
            "Measurement triggers instant state collapse upon user click."
        )

    with st.expander("Bell Entanglement (|Φ⁺⟩)", expanded=True):
        st.caption(
            "Paired tiles share Einstein-Podolsky-Rosen (EPR) correlation: "
            "$\\frac{1}{\\sqrt{2}}(|00\\rangle + |11\\rangle)$. Collapsing one instantaneously forces "
            "identical outcome on its twin."
        )

    st.markdown("---")
    st.caption("**Team DOPA** (Solo: Kartik Jain)  \nQiskit Fall Fest 2026 — IIIT Kottayam")

# ---------------------------------------------------------
# Header & Stats Ribbon
# ---------------------------------------------------------
st.markdown("""
<div class="hero-title">
    ⚛️ Q-SWEEP: ENTANGLED HAZARD
    <span class="badge-aer">QISKIT AER SIMULATOR</span>
</div>
""", unsafe_allow_html=True)
st.caption("A quantum minefield where hazards do not exist until forced into reality through quantum measurement.")

# Dynamic 3-Column Metrics Ribbon
m1, m2, m3 = st.columns(3)
with m1:
    st.metric(label="Player Score", value=st.session_state.score)
with m2:
    cleared_count = sum(st.session_state.revealed)
    st.metric(label="Tiles Observed", value=f"{cleared_count} / {TOTAL_TILES}")
with m3:
    status_text = "💥 DETONATED" if st.session_state.game_over else ("🏆 STABILIZED" if st.session_state.game_won else "✨ COHERENT")
    st.metric(label="System State", value=status_text)

st.write("")

# ---------------------------------------------------------
# Gameplay Engine Handler
# ---------------------------------------------------------
def handle_tile_action(idx: int):
    if st.session_state.revealed[idx] or st.session_state.game_over or st.session_state.game_won:
        return

    engine = st.session_state.engine

    if idx in ENTANGLED_MAP:
        twin = ENTANGLED_MAP[idx]
        ma, mb, qc = engine.generate_bell_pair()

        st.session_state.revealed[idx] = True
        st.session_state.revealed[twin] = True
        st.session_state.board_state[idx] = "💥 MINE" if ma == 1 else "🟢 SAFE"
        st.session_state.board_state[twin] = "💥 MINE" if mb == 1 else "🟢 SAFE"
        st.session_state.last_circuit = qc

        if ma == 1:
            st.session_state.game_over = True
            st.session_state.sound_to_play = "mine"
            st.session_state.log.append(f"Bell pair ({idx}, {twin}) collapsed -> |11⟩ (DETONATION)")
        else:
            st.session_state.score += 2
            st.session_state.sound_to_play = "entangle"
            st.session_state.log.append(f"Bell pair ({idx}, {twin}) collapsed -> |00⟩ (SAFE)")
    else:
        is_mine, qc = engine.probe_superposition_tile(mine_prob=0.30)
        st.session_state.revealed[idx] = True
        st.session_state.last_circuit = qc

        if is_mine == 1:
            st.session_state.board_state[idx] = "💥 MINE"
            st.session_state.game_over = True
            st.session_state.sound_to_play = "mine"
            st.session_state.log.append(f"Tile {idx} collapsed -> |1⟩ (DETONATION)")
        else:
            st.session_state.board_state[idx] = "🟢 SAFE"
            st.session_state.score += 1
            st.session_state.sound_to_play = "safe"
            st.session_state.log.append(f"Tile {idx} collapsed -> |0⟩ (SAFE)")

    if not st.session_state.game_over and all(st.session_state.revealed):
        st.session_state.game_won = True
        st.session_state.log.append("Wavefunction cleared across entire grid! Quantum Victory.")

# ---------------------------------------------------------
# Main Interactive Split (Grid on Left, Circuit on Right)
# ---------------------------------------------------------
col_grid, col_circuit = st.columns([1.1, 0.9])

with col_grid:
    st.markdown("""
    <div class="quantum-card">
        <div class="card-header-bar">
            <span>⚡ 3×3 QUANTUM HAZARD FIELD</span>
            <span class="entangle-flag">🔗 EPR PAIRS: (0,1) & (4,5)</span>
        </div>
    """, unsafe_allow_html=True)

    for row in range(GRID_SIZE):
        row_cols = st.columns(GRID_SIZE)
        for col in range(GRID_SIZE):
            idx = row * GRID_SIZE + col
            with row_cols[col]:
                if not st.session_state.revealed[idx]:
                    btn_label = f"|ψ{idx}⟩"
                    if idx in ENTANGLED_MAP:
                        btn_label += " 🔗"
                    if st.button(btn_label, key=f"t_{idx}", disabled=st.session_state.game_over or st.session_state.game_won):
                        handle_tile_action(idx)
                        st.rerun()
                else:
                    st.button(f"{st.session_state.board_state[idx]}", key=f"d_{idx}", disabled=True)

    if st.session_state.game_over:
        st.error(f"☠️ DETONATION COLLAPSE! Game Over. Final Score: {st.session_state.score}")
    elif st.session_state.game_won:
        st.success(f"🏆 COHERENT HARMONY! Grid Cleared. Final Score: {st.session_state.score}")
    st.markdown("</div>", unsafe_allow_html=True)

with col_circuit:
    st.markdown("""
    <div class="quantum-card">
        <div class="card-header-bar">
            <span>📡 CIRCUIT TELEMETRY</span>
            <span style="font-family:'JetBrains Mono',monospace; font-size:0.75rem; color:#64748b;">SHOTS: 1</span>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.last_circuit is not None:
        fig = st.session_state.last_circuit.draw(output="mpl")
        fig.patch.set_facecolor('#0f172a')
        for ax in fig.axes:
            ax.set_facecolor('#0f172a')
        st.pyplot(fig)

        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight", facecolor=fig.get_facecolor())
        st.download_button(
            label="📥 Download Circuit (.PNG)",
            data=buf.getvalue(),
            file_name="quantum_circuit.png",
            mime="image/png",
            use_container_width=True
        )
        plt.close(fig)
    else:
        st.info("Probe any qubit coordinate on the field to synthesize and measure its quantum circuit.")

    st.markdown("<br><strong style=\"font-family:'Space Grotesk',sans-serif; font-size:0.95rem; color:#cbd5e1;\">📜 Wavefunction Collapse History</strong>", unsafe_allow_html=True)
    for entry in reversed(st.session_state.log[-5:]):
        st.caption(f"<code>{entry}</code>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)