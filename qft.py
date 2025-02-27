from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import numpy as np
import matplotlib.pyplot as plt
from qiskit.visualization import plot_bloch_multivector
from qiskit.quantum_info import Statevector
import matplotlib


# Initialize Qiskit Aer simulator (done globally on purpose)
simulator = AerSimulator()


def qft(circuit, n):  # Big-endian indexing
   """
   Applies the Quantum Fourier Transform on the first n qubits using big-endian convention.
   """
   for i in range(n-1, -1, -1):  # Reverse the qubit order
      circuit.h(i)
      for j in range(i-1, -1, -1):  # Reverse control-target order
         angle = np.pi / (2 ** (i - j))
         circuit.cp(angle, j, i)
   circuit.barrier()
   return circuit


def show_qft_qc():
   # Number of qubits
   num_qubits = 3
   qc = QuantumCircuit(num_qubits)
   qft(qc, num_qubits)
   qc.draw('mpl')
   plt.show()  # Show the QFT circuit


# If you remove this line on MacOS, the function after it will NOT work!!!
matplotlib.use("TkAgg")  # Ensures Matplotlib uses a GUI backend
def visualize_qft(n=3):
   num_qubits = n
   basis_states = range(2**num_qubits)
   
   for state in basis_states:
      qc = QuantumCircuit(num_qubits)
      bin_state = format(state, f'0{num_qubits}b')
      print(f"\nApplying QFT to |{bin_state}⟩:")
      
      # Prepare the input state
      for i, bit in enumerate(reversed(bin_state)):
         if bit == '1':
               qc.x(i)
      
      # Apply QFT
      qft(qc, num_qubits)
      
      # Get the statevector
      statevector = Statevector(qc)
      
      # Generate and show Bloch multivector
      fig = plot_bloch_multivector(statevector)
      fig.set_size_inches(10, 10)  # Increase figure size
      
      plt.suptitle(f"QFT Applied to |{bin_state}⟩", fontsize=16)
      plt.show()  # Ensure the figure renders properly


if __name__ == "__main__":
   show_qft_qc()
   visualize_qft()