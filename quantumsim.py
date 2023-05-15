import tkinter as tk
from tkinter import ttk
from qiskit import QuantumCircuit, transpile, assemble
from qiskit.visualization import circuit_drawer
from qiskit.providers.aer import AerSimulator

# Create the simulator
simulator = AerSimulator()

def simulate_quantum_transfer(qubit_count):
    # Create the quantum circuit
    qc = QuantumCircuit(qubit_count, qubit_count)
    qc.h(0)
    for i in range(qubit_count - 1):
        qc.cx(i, i + 1)
    qc.measure(range(qubit_count), range(qubit_count))

    # Simulate the circuit
    qc = transpile(qc, basis_gates=['u1', 'u2', 'u3', 'cx'])
    qobj = assemble(qc)
    counts = simulator.run(qobj).result().get_counts()

    return counts

def start_simulation():
    qubit_count = int(qubit_entry.get())
    counts = simulate_quantum_transfer(qubit_count)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, str(counts))

    # Generate and display the circuit diagram
    qc = QuantumCircuit(qubit_count, qubit_count)
    qc.h(0)
    for i in range(qubit_count - 1):
        qc.cx(i, i + 1)
    qc.measure(range(qubit_count), range(qubit_count))

    circuit_text = circuit_drawer(qc, output='text')
    circuit_output.delete("1.0", tk.END)
    circuit_output.insert(tk.END, circuit_text)

# Create the main window
window = tk.Tk()
window.title("Quantum Data Transfer Simulation")
window.geometry("400x300")

# Set the background color
background_color = "#F0F0F0"
window.configure(bg=background_color)

# Create the input widgets
qubit_label = ttk.Label(window, text="Number of Qubits:")
qubit_label.pack(pady=10)

qubit_entry = ttk.Entry(window)
qubit_entry.pack(pady=5)

start_button = ttk.Button(window, text="Start Simulation", command=start_simulation)
start_button.pack(pady=10)

# Create the output widgets
output_label = ttk.Label(window, text="Output:")
output_label.pack()

output_text = tk.Text(window, height=5, width=30)
output_text.pack(pady=5)

circuit_label = ttk.Label(window, text="Circuit Diagram:")
circuit_label.pack()

circuit_output = tk.Text(window, height=10, width=50)
circuit_output.pack(pady=5)

# Run the GUI main loop
window.mainloop()
