# ⚛️ Q-Sweep: Entangled Hazard

> **Track 1: Quantum Games & Interactive Puzzles**  
> **Qiskit Fall Fest 2026 — IIIT Kottayam**  
> **Team:** DOPA (Solo Developer: Kartik Jain)  
> **Tech Stack:** Python 3.10+, Qiskit 1.0+, Qiskit Aer (`AerSimulator`), Streamlit, Matplotlib

---

## 📌 Executive Summary

**Q-Sweep: Entangled Hazard** reinterprets the classic game of Minesweeper through fundamental quantum mechanics. 

In classical Minesweeper, hazards are pre-placed into static memory arrays before gameplay begins. In **Q-Sweep**, hazards do not physically exist until an observation occurs. Each unrevealed tile exists in a true quantum superposition $\vert{}\psi\rangle$ or an entangled Bell pair $\vert{}\Phi^+\rangle$. Clicking a tile compiles and executes an individual quantum circuit on Qiskit's `AerSimulator`, forcing wavefunction collapse in real time.

---

## 🔬 Core Quantum Mechanics Implemented

### 1. Parameterized Superposition ($R_y$ Rotation)
Standard grid coordinates exist in an unobserved superposition prepared via single-qubit rotation:
$$\vert{}\psi\rangle = R_y(\theta)\vert{}0\rangle = \cos\left(\frac{\theta}{2}\right)\vert{}0\rangle + \sin\left(\frac{\theta}{2}\right)\vert{}1\rangle$$
* State $\vert{}0\rangle \rightarrow$ **Safe**
* State $\vert{}1\rangle \rightarrow$ **Detonated Mine**
* Rotation parameter: $\theta = 2 \arcsin(\sqrt{P_{\text{mine}}})$ (configured at $P = 0.30$).
* Clicking the tile triggers a projective $Z$-basis measurement, collapsing the amplitude into a deterministic macroscopic outcome.

### 2. Non-Local Entanglement (Bell State $\vert{}\Phi^+\rangle$)
Tiles **(0, 1)** and **(4, 5)** are pairwise entangled:
$$\vert{}\Phi^+\rangle = \frac{1}{\sqrt{2}}(\vert{}00\rangle + \vert{}11\rangle)$$
* Generated via a Hadamard gate on qubit 0 followed by a CNOT gate across $(q_0, q_1)$.
* Measuring either tile instantaneously forces its partner to collapse into the exact identical state across the grid, demonstrating Einstein-Podolsky-Rosen (EPR) correlation.

### 3. Unitary Gate Interventions (Tactical Power-Ups)
Players can manipulate probability amplitudes prior to projective measurement:
* **Hadamard Shield ($H$-Gate):** Induces quantum interference across the basis states, drastically skewing probability amplitudes toward $\vert{}0\rangle$ (Safe), lowering mine probability from $30\%$ to $\sim 2.7\%$.
* **Pauli-X Inverter ($X$-Gate):** Bit-flip operation ($\vert{}0\rangle \leftrightarrow \vert{}1\rangle$), inverting outcome probabilities if a player suspects high hazard density.

---

## 🚀 Key Features & UI Architecture

* **Genuine Quantum Execution:** Zero pseudo-random generators (`random.randint` is strictly avoided). Every tile click synthesizes a `QuantumCircuit` executed on `AerSimulator(shots=1)`.
* **Live Circuit Telemetry:** Dynamically draws the generated Qiskit circuit diagram with Matplotlib, showing gate operations and measurement barriers in real time.
* **Circuit Export:** Judges and players can download single-shot PNG diagrams of synthesized circuits directly from the UI.
* **Responsive Dark Aurora Interface:** Built with Streamlit, custom CSS, 3D hover feedback, and real-time state telemetry.
* **Zero-Dependency Web Audio Synthesis:** Built-in audio cues using the browser Web Audio API for safe clears, entanglement sweeps, and detonation rumbles.

---

## 📁 Repository Structure

```text
Q-Sweep-Entangled-Hazard/
├── src/
│   ├── app.py                # Streamlit UI, Web Audio API, Telemetry dashboard
│   └── quantum_engine.py     # Qiskit circuit synthesis, AerSimulator execution
├── requirements.txt          # Python dependencies
├── q_sweep_presentation.html # Hackathon pitch deck (7-slide presentation)
├── README.md                 # Complete project documentation
└── LICENSE                   # MIT License