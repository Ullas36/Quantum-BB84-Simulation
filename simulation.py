import random
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit import transpile

# Step 1: Alice generates random bits and bases
def generate_bits_and_bases(n):
    bits = [random.randint(0, 1) for _ in range(n)]
    bases = [random.choice(['X', 'Z']) for _ in range(n)]
    return bits, bases

# Step 2: Alice prepares qubits based on bits and bases
def create_qubit_circuits(bits, bases):
    circuits = []
    for bit, base in zip(bits, bases):
        qc = QuantumCircuit(1, 1)
        if bit == 1:
            qc.x(0)  # Flip to |1⟡
        if base == 'X':
            qc.h(0)  # Prepare in X basis
        circuits.append(qc)
    return circuits

# Eve intercepts and resends qubits
def intercept_qubits(circuits):
    intercepted_circuits = []
    simulator = AerSimulator()
    for qc in circuits:
        eve_base = random.choice(['X', 'Z'])
        intercepted_qc = qc.copy()
        if eve_base == 'X':
            intercepted_qc.h(0)
        intercepted_qc.measure(0, 0)

        compiled = transpile(intercepted_qc, simulator)
        result = simulator.run(compiled, shots=1).result()
        counts = result.get_counts(intercepted_qc)
        measured_bit = int(list(counts.keys())[0])

        # Eve prepares a new qubit based on her measurement
        new_qc = QuantumCircuit(1, 1)
        if measured_bit == 1:
            new_qc.x(0)
        if eve_base == 'X':
            new_qc.h(0)
        intercepted_circuits.append(new_qc)
    return intercepted_circuits

# Step 3: Bob measures with his own random bases
def measure_qubits(circuits, bob_bases):
    measured_bits = []
    simulator = AerSimulator()
    for qc, base in zip(circuits, bob_bases):
        if base == 'X':
            qc.h(0)  # Measure in X basis
        qc.measure(0, 0)
        compiled_circuit = transpile(qc, simulator)
        result = simulator.run(compiled_circuit, shots=1).result()
        counts = result.get_counts(qc)
        bit = int(list(counts.keys())[0])
        measured_bits.append(bit)
    return measured_bits

# Step 4: Sifting 
def sift_keys(alice_bits, alice_bases, bob_bits, bob_bases):
    sifted_alice = []
    sifted_bob = []
    for a_bit, a_base, b_bit, b_base in zip(alice_bits, alice_bases, bob_bits, bob_bases):
        if a_base == b_base:
            sifted_alice.append(a_bit)
            sifted_bob.append(b_bit)
    return sifted_alice, sifted_bob

# Step 5: Eavesdropping Detection
def detect_eavesdropping(sifted_alice, sifted_bob, sample_size=10):
    sample_size = min(sample_size, len(sifted_alice))
    indices = random.sample(range(len(sifted_alice)), sample_size)
    alice_sample = [sifted_alice[i] for i in indices]
    bob_sample = [sifted_bob[i] for i in indices]
    mismatches = sum(1 for a, b in zip(alice_sample, bob_sample) if a != b)
    error_rate = mismatches / sample_size
    print(f"\n🔍 Eavesdropping Detection Sample:")
    print("  Alice:", alice_sample)
    print("  Bob  :", bob_sample)
    print(f"  Error rate: {error_rate * 100:.2f}%")
    return error_rate, indices

# Step 6: Final key extraction
def extract_final_key(key, indices_to_remove):
    return [bit for i, bit in enumerate(key) if i not in indices_to_remove]

# BB84 full protocol with Eve
def bb84_protocol(n=50, sample_size=10):
    print("📦 BB84 Quantum Key Distribution Simulation")

    # Step 1: Generate Alice's bits and bases
    alice_bits, alice_bases = generate_bits_and_bases(n)

    # Step 2: Encode qubits
    circuits = create_qubit_circuits(alice_bits, alice_bases)

    # Eve intercepts the qubits
    intercepted_circuits = intercept_qubits(circuits)

    # Step 3: Bob chooses random bases and measures
    bob_bases = [random.choice(['X', 'Z']) for _ in range(n)]
    bob_bits = measure_qubits(intercepted_circuits, bob_bases)

    # Step 4: Sifting
    sifted_alice, sifted_bob = sift_keys(alice_bits, alice_bases, bob_bits, bob_bases)
    print(f"\n🔑 Sifted Key Length: {len(sifted_alice)}")

    # Step 5: Eavesdropping Detection
    error_rate, test_indices = detect_eavesdropping(sifted_alice, sifted_bob, sample_size)
    if error_rate > 0.2:
        print("❌ Eavesdropping detected! Discarding key.")
        return []

    # Step 6: Final Key Extraction
    final_key = extract_final_key(sifted_alice, test_indices)
    print(f"\n✅ Final Secret Key (Alice & Bob): {final_key}")
    return final_key

# Run the simulation
final_key = bb84_protocol(n=50, sample_size=10)
