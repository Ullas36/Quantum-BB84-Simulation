# 🔐 BB84 Quantum Key Distribution Simulator

This is a simulation of the BB84 quantum key distribution protocol using [Qiskit](https://qiskit.org/). It includes support for eavesdropping attacks (Eve) and error rate analysis to detect compromised quantum channels.

---

## 💡 What is BB84?

BB84 is a quantum cryptography protocol that allows two parties (Alice and Bob) to share a secret key using quantum bits. It leverages the principles of superposition and measurement collapse to ensure that any eavesdropping attempt introduces detectable errors.

---

## ⚙️ Features

- Random bit & basis generation (Alice)
- Qubit encoding using X/Z bases
- Eve intercept-resend simulation (random basis)
- Bob's measurement in random bases
- Sifting & key comparison
- Eavesdropper detection using sample error rate
- Final key extraction after verification

---

## 🧪 Sample Output

```bash
📦 BB84 Quantum Key Distribution Simulation

🔑 Sifted Key Length: 21

🔍 Eavesdropping Detection Sample:
  Alice: [0, 0, 0, 0, 1, 1, 0, 0, 1, 0]
  Bob  : [1, 0, 0, 0, 1, 1, 0, 1, 1, 0]
  Error rate: 20.00%

✅ Final Secret Key (Alice & Bob): [0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0]




How to Run
Install Python 3.10+

Install Qiskit & Aer:

pip install qiskit qiskit-aer
python simulation.py
```
