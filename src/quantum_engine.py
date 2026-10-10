"""
quantum_engine.py
Core quantum backend for Q-Sweep: Entangled Hazard using Qiskit AerSimulator.
Handles Bell-state generation, superposition, and gate interventions (H, X).
"""
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

class QuantumSweeperEngine:
    def __init__(self):
        self.simulator = AerSimulator()

    def generate_bell_pair(self) -> tuple[int, int, QuantumCircuit]:
        """
        Creates a maximally entangled Bell state:
        |Phi+> = (|00> + |11>) / sqrt(2)
        Measuring qubit 0 instantly correlates with qubit 1.
        Outcome '1' represents a Mine, '0' represents Safe.
        """
        qc = QuantumCircuit(2, 2)
        qc.h(0)          # Apply Hadamard to put qubit 0 into superposition
        qc.cx(0, 1)      # Entangle qubit 0 and qubit 1
        qc.measure([0, 1], [0, 1])

        job = self.simulator.run(qc, shots=1)
        counts = job.result().get_counts()
        bitstring = list(counts.keys())[0]  # Deterministically '00' or '11'

        mine_a = int(bitstring[1])
        mine_b = int(bitstring[0])
        return mine_a, mine_b, qc

    def probe_superposition_tile(self, mine_prob: float = 0.30, intervention_gate: str | None = None) -> tuple[int, QuantumCircuit]:
        """
        Puts an unentangled tile into superposition via Ry rotation.
        Optionally applies an intervention gate (H or X) before measurement.
        Measurement collapses the tile into Safe (0) or Mine (1).
        """
        qc = QuantumCircuit(1, 1)
        theta = 2 * np.arcsin(np.sqrt(mine_prob))
        qc.ry(theta, 0)

        # Apply player intervention gate if selected
        if intervention_gate == "H":
            qc.h(0)
        elif intervention_gate == "X":
            qc.x(0)

        qc.measure(0, 0)

        job = self.simulator.run(qc, shots=1)
        counts = job.result().get_counts()
        bitstring = list(counts.keys())[0]

        is_mine = int(bitstring[0])
        return is_mine, qc