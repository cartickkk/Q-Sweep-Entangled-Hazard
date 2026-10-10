# Q-Sweep: Entangled Hazard

## Project Metadata
- **Track:** Track 1: Quantum Games & Interactive Puzzles
- **Team Name:** DOPA
- **Team Members:** Kartik Jain (kartik.jain.cs24@gmail.com)
- **Target Audience:** Students, quantum enthusiasts, and gamers exploring superposition and quantum entanglement fundamentals.

---

## 1. Project Overview & Motivation

- **Summary (3–4 sentences):**
  Q-Sweep: Entangled Hazard is an interactive quantum puzzle game that reinvents the classic minefield sweeper through genuine Qiskit circuit dynamics. Instead of relying on a static, pre-computed minefield, hazard states are indeterminate prior to observation and collapse in real time via quantum measurement. The game models non-local correlations using Bell states, causing entangled tile pairs across the grid to instantaneously collapse into identical states upon interaction.

- **Why this problem / game?**
  Classical puzzle games cannot intuitively represent wave function collapse or non-local correlations. Q-Sweep provides a hands-on, visually transparent playground where the act of measurement actively creates game outcomes. By displaying live quantum circuit execution telemetry alongside board updates, players build practical mental models of superposition ($R_y$) and Einstein-Podolsky-Rosen (EPR) pairs ($\vert{}\Phi^+\rangle$).

---

## 2. Quantum Architecture & Mechanics

- **Core Quantum Principles Used:**
  Parameterized Superposition ($R_y$ rotation gates), Bell-State Entanglement ($\vert{}\Phi^+\rangle$ via $H$ and $CX$ gates), and Wavefunction Measurement Collapse.

- **How the Quantum Circuit is Integrated:**
  Every player click triggers an event loop in `src/quantum_engine.py`. For unentangled tiles, a single-qubit parameterized rotation is applied and sampled via `AerSimulator` to determine whether the collapsed state is Safe ($\vert{}0\rangle$) or Mine ($\vert{}1\rangle$). When an entangled coordinate is chosen, a two-qubit Bell circuit is simulated with single-shot measurement; both paired grid coordinates update simultaneously based on the correlated bitstring outcome (`00` or `11`).

- **Circuit Details:**
  - **Number of Qubits:** 1 qubit for standard cells; 2 qubits for entangled pair cells.
  - **Key Gates Used:** $H$ (Hadamard), $CX$ (Controlled-NOT), $R_y(\theta)$ (Single-axis rotation), and Measurement operators.
  - **Primitives Used:** Qiskit Aer (`AerSimulator`).
  - **Other Technologies Used:** Streamlit (UI frontend), Matplotlib & Pylatexenc (circuit diagram visualization), NumPy (probabilistic parameter calculation).

```python
# Representative snippet of core Qiskit circuit execution
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def generate_bell_pair():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    sim = AerSimulator()
    result = sim.run(qc, shots=1).result().get_counts()
    bitstring = list(result.keys())[0]
    return int(bitstring[1]), int(bitstring[0]), qc