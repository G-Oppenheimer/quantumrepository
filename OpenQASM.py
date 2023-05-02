import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile, Aer, execute
from qiskit.visualization import plot_histogram, plot_bloch_multivector

#Circuits
qr = QuantumRegister(3, name="q")
cr = ClassicalRegister(3, name="c")

#INIT
circuit = QuantumCircuit(qr, cr)

# Superposition states
# Randomizes the state
theta = np.random.rand() * np.pi
phi = np.random.rand() * 2 * np.pi
circuit.u3(theta, phi, 0, qr[0])

# Entangled state (Bell Pair)
circuit.h(qr[1])
circuit.cx(qr[1], qr[2])

# Perform the teleportation 
circuit.cx(qr[0], qr[1])
circuit.h(qr[0])
circuit.barrier()
circuit.measure([qr[0], qr[1]], [cr[0], cr[1]])
circuit.barrier()
circuit.cx(qr[1], qr[2])
circuit.cz(qr[0], qr[2])

# Final state of teleported qubits to bits
circuit.measure(qr[2], cr[2])

# Simulate 
backend = Aer.get_backend('qasm_simulator')
job = execute(circuit, backend, shots=1024)
result = job.result()

# Visualization
counts = result.get_counts(circuit)
plot_histogram(counts)
