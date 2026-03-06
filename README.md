# Quantum Cryptography Key Exchange Analysis

## Overview

This project provides a comprehensive study and simulation of **quantum cryptography key exchange mechanisms**, with a primary focus on the **BB84 Quantum Key Distribution (QKD) protocol**. It compares quantum approaches with classical key exchange techniques such as **Diffie-Hellman (DH)** and **RSA**, evaluating their security guarantees in both current and post-quantum computing landscapes.

The project includes a full Python simulation with **six separate matplotlib visualizations** covering protocol behavior, eavesdropper detection, channel noise effects, key rate limitations, and the comparative vulnerability of classical cryptographic systems to quantum attacks.

---

## Table of Contents

- [Overview](#overview)
- [Background](#background)
  - [Classical Key Exchange](#classical-key-exchange)
  - [Quantum Key Distribution](#quantum-key-distribution)
  - [BB84 Protocol](#bb84-protocol)
- [Quantum Properties Enabling Secure Communication](#quantum-properties-enabling-secure-communication)
- [Project Structure](#project-structure)
- [Simulation Details](#simulation-details)
  - [Core Function: simulate_bb84()](#core-function-simulate_bb84)
  - [Simulation Scenarios](#simulation-scenarios)
  - [Theoretical Models](#theoretical-models)
- [Visualizations](#visualizations)
- [Console Output](#console-output)
- [How to Run](#how-to-run)
- [Results and Findings](#results-and-findings)
- [Limitations and Future Work](#limitations-and-future-work)
- [References](#references)

---

## Background

### Classical Key Exchange

Classical key exchange protocols allow two parties to establish a shared secret over a public channel. The two dominant approaches are:

#### Diffie-Hellman (DH) Key Exchange
- Introduced in 1976 by Whitfield Diffie and Martin Hellman.
- Based on the computational difficulty of the **discrete logarithm problem** (DLP).
- Two parties (Alice and Bob) publicly agree on a large prime $p$ and a generator $g$.
- Each party generates a private key ($a$, $b$), computes a public value ($g^a \mod p$, $g^b \mod p$), and exchanges them.
- Both can independently compute the shared secret: $K = g^{ab} \mod p$.
- Security relies on the assumption that given $g^a \mod p$, recovering $a$ is computationally infeasible.
- **Variants:** Elliptic Curve Diffie-Hellman (ECDH) provides equivalent security with shorter keys.

#### RSA Key Exchange
- Introduced in 1977 by Rivest, Shamir, and Adleman.
- Relies on the difficulty of **integer factorization**.
- One party generates a key pair: public key $(n, e)$ and private key $d$, where $n = p \cdot q$ (product of two large primes).
- A session key is encrypted with the recipient's public key; only the corresponding private key can decrypt it.
- Security depends on the infeasibility of factoring $n$ back into $p$ and $q$.

#### Vulnerabilities of Classical Approaches

| Vulnerability | Details |
|---------------|---------|
| **Shor's Algorithm** | Solves integer factorization and discrete logarithm in polynomial time $O(n^3)$ on a quantum computer, breaking both RSA and DH. |
| **No Eavesdrop Detection** | A passive adversary can record all ciphertext without either party ever knowing. |
| **Computational Security Only** | Security is based on assumed computational hardness, not proven impossibility. Given enough computational power (or algorithmic breakthroughs), keys can be recovered. |
| **Harvest Now, Decrypt Later** | Encrypted traffic recorded today can be stored and decrypted once quantum computers become available. |

### Quantum Key Distribution

Quantum Key Distribution (QKD) leverages the fundamental principles of quantum mechanics to enable two parties to produce a shared random secret key known only to them. Unlike classical methods, QKD provides:

| Property | Description |
|----------|-------------|
| **Information-Theoretic Security** | Security is guaranteed by the laws of physics, not by computational hardness assumptions. No amount of computational power can break the protocol. |
| **Eavesdropper Detection** | Any attempt by a third party (Eve) to intercept the quantum channel introduces measurable disturbances, quantified as the Quantum Bit Error Rate (QBER). |
| **Forward Secrecy** | Each key exchange session generates a completely fresh, independent key. Compromising one session reveals nothing about past or future sessions. |
| **Future-Proof Security** | Unlike classical protocols, QKD is inherently resistant to quantum computing attacks. |

### BB84 Protocol

The **BB84 protocol**, proposed by Charles Bennett and Gilles Brassard in 1984, was the first quantum cryptographic protocol and remains the most widely studied and implemented QKD scheme.

#### Protocol Steps in Detail

**Step 1 — Qubit Preparation (Alice):**
- Alice generates a random sequence of classical bits (0s and 1s).
- For each bit, she randomly selects one of two **encoding bases**:
  - **Rectilinear basis (+):** encodes 0 as |0⟩ (horizontal polarization) and 1 as |1⟩ (vertical polarization)
  - **Diagonal basis (×):** encodes 0 as |+⟩ (45° polarization) and 1 as |−⟩ (135° polarization)
- She sends the encoded qubits to Bob through a **quantum channel** (e.g., optical fiber or free-space link).

**Step 2 — Qubit Measurement (Bob):**
- Bob independently and randomly chooses a measurement basis (+ or ×) for each received qubit.
- If Bob's chosen basis matches Alice's encoding basis → he obtains the **correct** bit value with certainty.
- If the bases differ → the measurement result is **completely random** (50/50 chance of 0 or 1), and the original state is destroyed.

**Step 3 — Basis Reconciliation (Sifting):**
- Over an authenticated **classical channel** (e.g., internet), Alice and Bob publicly compare their basis choices for each qubit (but **never** the bit values).
- They discard all bits where their bases did not match.
- The remaining bits form the **sifted key**, which is approximately **50% of the originally transmitted qubits**.

**Step 4 — Error Estimation & Eavesdrop Detection:**
- Alice and Bob publicly sacrifice a random subset of the sifted key to estimate the **Quantum Bit Error Rate (QBER)**.
- If QBER < **11%** (theoretical security threshold for BB84) → the channel is considered secure; they proceed.
- If QBER ≥ **11%** → potential eavesdropping is detected; the entire key is discarded and the process restarts.
- A full intercept-resend attack by Eve introduces a QBER of approximately **25%**, making it easily detectable.

**Step 5 — Error Correction:**
- Standard classical error correction protocols (e.g., Cascade, LDPC codes) fix the remaining bit errors in the sifted key.
- Some key bits are consumed during this process.

**Step 6 — Privacy Amplification:**
- Universal hashing functions compress the corrected key to a shorter final key.
- This eliminates any partial information an eavesdropper might have gained.
- The resulting key is **provably secure** for use in one-time pad encryption or other symmetric ciphers.

#### BB84 Encoding Table

| Alice's Bit | Basis | Quantum State | Polarization |
|:-----------:|:-----:|:-------------:|:------------:|
| 0 | Rectilinear (+) | \|0⟩ | Horizontal (0°) |
| 1 | Rectilinear (+) | \|1⟩ | Vertical (90°) |
| 0 | Diagonal (×) | \|+⟩ | Diagonal (45°) |
| 1 | Diagonal (×) | \|−⟩ | Anti-diagonal (135°) |

---

## Quantum Properties Enabling Secure Communication

The security of quantum cryptography rests on three fundamental quantum mechanical principles:

### 1. Superposition

A qubit can exist in a **superposition** of states — simultaneously in both |0⟩ and |1⟩ until measured. In BB84, this allows encoding information in different, incompatible bases. A qubit prepared in the diagonal basis is a superposition of the rectilinear basis states:

$$|+\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle), \quad |-\rangle = \frac{1}{\sqrt{2}}(|0\rangle - |1\rangle)$$

**Why this matters for security:** Measuring a diagonal-basis qubit in the rectilinear basis yields a completely random result (probability 1/2 for each outcome). Eve cannot determine which basis Alice used without disturbing the qubit. This incompatibility between bases is the core mechanism enabling eavesdropper detection.

### 2. Measurement Disturbance (Heisenberg Uncertainty Principle)

Quantum measurement **irreversibly disturbs** the state of a qubit when the measurement basis is incompatible with the preparation basis:

> Measuring a quantum system in a basis incompatible with its preparation basis irreversibly collapses the state, introducing errors that cannot be hidden.

**Impact on BB84:**
- Eve must guess Alice's encoding basis for each qubit.
- She guesses correctly only **50%** of the time.
- When she guesses wrong, she measures in the wrong basis, collapsing the qubit to a random state.
- She then resends the collapsed qubit to Bob.
- When Bob measures these disturbed qubits (even in the correct basis), he gets the wrong answer **50%** of the time.
- Net effect: Eve introduces errors on **25%** of the sifted key bits ($0.5 \times 0.5 = 0.25$).

### 3. No-Cloning Theorem

The **no-cloning theorem** (Wootters & Zurek, 1982) proves that it is physically impossible to create an identical copy of an arbitrary unknown quantum state:

$$\nexists \text{ unitary } U \text{ such that } U|\psi\rangle|0\rangle = |\psi\rangle|\psi\rangle \text{ for all } |\psi\rangle$$

**Why this matters:** This theorem prevents Eve from employing a "copy and forward" strategy. She cannot:
1. Intercept Alice's qubit
2. Make a perfect copy
3. Forward the original to Bob (undisturbed)
4. Measure her copy at leisure

Any interaction with the qubit necessarily disturbs its state, making eavesdropping fundamentally detectable.

### Combined Security Guarantee

Together, these three principles ensure that:
- Eve **cannot copy** qubits (no-cloning)
- Eve **cannot measure** without disturbing (measurement disturbance)
- Eve **cannot determine** the encoding basis without measuring (superposition/incompatible bases)
- Any eavesdropping attempt **inevitably introduces errors** that Alice and Bob can detect via QBER

This provides **unconditional security** — security that holds regardless of Eve's computational power or technological capabilities.

---

## Project Structure

```
Quantum Cryptography Key Exchange Analysis/
│
├── quantum_key_exchange_analysis.py    # Main simulation and visualization script
│
├── plot1_bb84_sifted_key.png           # Plot 1: BB84 sifted key bit comparison
├── plot2_qber_vs_interception.png      # Plot 2: QBER vs eavesdropper interception
├── plot3_qber_vs_noise.png             # Plot 3: QBER vs channel noise
├── plot4_key_rate_vs_distance.png      # Plot 4: Key rate vs distance
├── plot5_symmetric_key_attack.png      # Plot 5: Classical vs quantum symmetric attacks
├── plot6_rsa_vulnerability.png         # Plot 6: RSA classical vs quantum factoring
│
└── README.md                           # This documentation file
```

All `.png` plot files are generated automatically when the script is executed.

---

## Simulation Details

### Core Function: `simulate_bb84()`

The simulation engine is the `simulate_bb84()` function, which models the full BB84 protocol:

```
simulate_bb84(num_qubits=1000, eavesdrop=False, noise_level=0.0) → dict
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `num_qubits` | int | Number of qubits Alice transmits to Bob (default: 1000) |
| `eavesdrop` | bool | If True, Eve performs a full intercept-resend attack on every qubit |
| `noise_level` | float | Probability (0.0–1.0) of a random bit-flip in the quantum channel |

**Returns:** A dictionary containing:
| Key | Description |
|-----|-------------|
| `num_qubits` | Total qubits sent |
| `sifted_length` | Number of bits remaining after basis sifting (~50% of num_qubits) |
| `sifted_alice` | Alice's sifted key bits |
| `sifted_bob` | Bob's sifted key bits |
| `errors` | Number of mismatched bits in sifted key |
| `qber` | Quantum Bit Error Rate (errors / sifted_length) |

**Internal Simulation Flow:**
1. Alice generates random bits and random bases (0 = rectilinear, 1 = diagonal)
2. If `eavesdrop=True`: Eve intercepts each qubit, measures in a random basis, and resends her measurement result
3. Channel noise is applied: each bit has `noise_level` probability of being flipped
4. Bob measures each qubit in a randomly chosen basis
5. Sifting: only bits where Alice's and Bob's bases matched are kept
6. QBER is calculated on the sifted key

### Simulation Scenarios

The script runs **six simulation scenarios** using 2000 qubits per run:

#### Scenario 1: Clean BB84 (No Eve, No Noise)
- Validates protocol correctness under ideal conditions.
- Expected: QBER = 0, sifted key ≈ 1000 bits (50% of 2000).

#### Scenario 2: BB84 Under Full Intercept-Resend Attack
- Eve intercepts and measures every qubit in a random basis, then resends.
- Expected: QBER ≈ 25% (detected as eavesdropping above 11% threshold).

#### Scenario 3: QBER vs Channel Noise Sweep
- Noise level swept from 0% to 50% in 30 steps, with no eavesdropper.
- Maps the relationship between physical channel imperfections and error rate.
- Reveals the noise tolerance boundary of the protocol.

#### Scenario 4: QBER vs Partial Eavesdropper Interception
- Eve's interception fraction swept from 0% to 100% in 30 steps.
- Models a realistic scenario where Eve only intercepts a portion of the qubits.
- Shows the proportional relationship between interception rate and detectable QBER.

#### Scenario 5: Key Rate vs Fiber Distance (Theoretical)
- Models BB84 key rate decay over optical fiber using exponential attenuation: $R \propto e^{-\alpha L}$, with $\alpha = 0.046$ /km.
- Compares against classical key exchange which has no distance-dependent degradation.

#### Scenario 6: Cryptanalysis Time Comparison (Theoretical)
- Computes time-to-break in log₁₀(years) for:
  - **Symmetric keys** (128–4096 bit): Classical brute-force ($2^{n/2}$ operations) vs. Grover's algorithm ($2^{n/4}$ operations), assuming $10^{15}$ operations/second.
  - **RSA keys** (512–4096 bit): Classical GNFS factoring vs. Shor's algorithm ($O(n^3)$ operations).

### Theoretical Models

#### Fiber Attenuation Model
The BB84 key rate over optical fiber follows:

$$R(L) = e^{-\alpha L}$$

where $\alpha = 0.046$ /km (corresponding to ~0.2 dB/km loss in standard telecom fiber at 1550 nm) and $L$ is the fiber length in kilometers.

#### GNFS Factoring Complexity
The classical factoring time for an $n$-bit RSA modulus is estimated via the General Number Field Sieve:

$$T_{\text{GNFS}} \propto \exp\left(1.9 \cdot (\ln n)^{1/3} \cdot (\ln \ln n)^{2/3}\right)$$

#### Grover's Algorithm Speedup
For a symmetric key of $n$ bits, Grover's algorithm provides a quadratic speedup:
- Classical search: $O(2^{n/2})$ operations (birthday bound)
- Quantum search: $O(2^{n/4})$ operations

This effectively halves the security level: a 256-bit key provides only 128-bit security against a quantum adversary.

#### Shor's Algorithm
For an $n$-bit RSA modulus, Shor's algorithm runs in:

$$T_{\text{Shor}} = O(n^3)$$

This is polynomial time, meaning RSA keys of **any practical size** can be broken near-instantly by a sufficiently large quantum computer.

---

## Visualizations

The script generates **six separate, publication-quality plots**, each displayed in its own window and saved as an individual PNG file:

### Plot 1: BB84 Sifted Key — First 50 Bits
**File:** `plot1_bb84_sifted_key.png`

Bar chart comparing the first 50 bits of Alice's and Bob's sifted keys under clean conditions. Red vertical lines indicate positions where an eavesdropper (from Scenario 2) would have caused bit mismatches. Demonstrates that without Eve, Alice and Bob's keys match perfectly.

### Plot 2: Eavesdropper Detection via QBER
**File:** `plot2_qber_vs_interception.png`

Line plot showing QBER as a function of Eve's interception fraction (0%–100%). Features:
- **Pink line with markers:** Simulated QBER values
- **Gray dashed line:** Theoretical maximum QBER (25%) for full interception
- **Orange dashed line:** BB84 security threshold (11%)
- **Green shading:** Secure region (QBER < 11%)
- **Red shading:** Insecure region (QBER > 11%)

Key insight: Even intercepting ~45% of qubits pushes QBER above the security threshold.

### Plot 3: Effect of Channel Noise on QBER
**File:** `plot3_qber_vs_noise.png`

Line plot showing QBER vs. channel noise level (0%–50%). Demonstrates how physical channel imperfections increase QBER and at what point the protocol can no longer guarantee security. The security threshold is marked at 11%.

### Plot 4: Key Rate vs Distance — Quantum vs Classical
**File:** `plot4_key_rate_vs_distance.png`

Semi-logarithmic plot comparing:
- **BB84 key rate** (red): Exponential decay over fiber distance
- **Classical key exchange** (blue dashed): Distance-independent

Highlights the practical ~100 km limit for fiber-based BB84 and the fundamental physical constraint quantum channels face.

### Plot 5: Classical vs Quantum Attack on Symmetric Keys
**File:** `plot5_symmetric_key_attack.png`

Grouped bar chart comparing log₁₀(time to break) for symmetric keys (128–4096 bits):
- **Blue bars:** Classical brute-force attack time
- **Red bars:** Quantum (Grover's algorithm) attack time
- **Green dashed line:** Age of the universe (~10¹⁰ years)

Shows that Grover's algorithm halves the effective key length, but large symmetric keys (≥256 bits) remain secure against quantum attacks.

### Plot 6: RSA Vulnerability — Classical vs Quantum Factoring
**File:** `plot6_rsa_vulnerability.png`

Grouped bar chart comparing log₁₀(time to factor) for RSA keys (512–4096 bits):
- **Orange bars:** Classical GNFS factoring time
- **Pink bars:** Quantum (Shor's algorithm) factoring time

Dramatically illustrates how Shor's algorithm reduces factoring time from astronomically large values to negligible amounts, rendering RSA completely broken.

---

## Console Output

In addition to the plots, the script prints a detailed summary table to the console:

```
=================================================================
  QUANTUM CRYPTOGRAPHY KEY EXCHANGE — SIMULATION RESULTS
=================================================================

─────────────────────────────────────────────────────────────────
  BB84 Protocol (No Eavesdropper, No Noise)
─────────────────────────────────────────────────────────────────
  Qubits sent        : 2000
  Sifted key length  : 1020
  Bit errors         : 0
  QBER               : 0.0000  (expected ~0)

─────────────────────────────────────────────────────────────────
  BB84 Protocol (With Eavesdropper)
─────────────────────────────────────────────────────────────────
  Qubits sent        : 2000
  Sifted key length  : 1035
  Bit errors         : 286
  QBER               : 0.2763  (expected ~0.25)
  Eve detected?      : YES

─────────────────────────────────────────────────────────────────
  Security Comparison Summary
─────────────────────────────────────────────────────────────────
  ┌──────────────────┬──────────────────┬──────────────────┐
  │ Property         │ BB84 (Quantum)   │ Classical (DH)   │
  ├──────────────────┼──────────────────┼──────────────────┤
  │ Security basis   │ Quantum physics  │ Math complexity  │
  │ Forward secrecy  │ Inherent         │ Requires config  │
  │ Eve detection    │ Yes (QBER)       │ No               │
  │ Quantum-safe     │ Yes              │ No (Shor's alg.) │
  │ Distance limit   │ ~100 km (fiber)  │ Unlimited        │
  │ Infrastructure   │ Quantum channel  │ Standard network │
  └──────────────────┴──────────────────┴──────────────────┘
```

---

## How to Run

### Prerequisites

- **Python 3.8+**
- **NumPy** — numerical computation and array operations
- **Matplotlib** — plotting and visualization

### Installation

```bash
pip install numpy matplotlib
```

### Execution

```bash
python quantum_key_exchange_analysis.py
```

### What Happens When You Run It

1. **Simulation phase:** All six BB84 and cryptanalysis scenarios are computed (~2–3 seconds).
2. **Visualization phase:** Six separate plot windows open simultaneously, each showing a different analysis.
3. **File output:** Six PNG files are saved to the working directory.
4. **Console output:** A formatted summary table is printed to the terminal.
5. **Interactive viewing:** All plot windows remain open for inspection. Close them to exit the program.

### Expected Output Files

| File | Size | Content |
|------|------|---------|
| `plot1_bb84_sifted_key.png` | ~200 KB | Sifted key bit comparison |
| `plot2_qber_vs_interception.png` | ~150 KB | QBER vs interception fraction |
| `plot3_qber_vs_noise.png` | ~140 KB | QBER vs channel noise |
| `plot4_key_rate_vs_distance.png` | ~130 KB | Key rate distance comparison |
| `plot5_symmetric_key_attack.png` | ~120 KB | Symmetric key attack times |
| `plot6_rsa_vulnerability.png` | ~110 KB | RSA factoring vulnerability |

---

## Results and Findings

### Key Result 1: BB84 Successfully Detects Eavesdropping
- With **no eavesdropper**, QBER = **0.00%** — Alice and Bob share a perfect key.
- With a **full intercept-resend attack**, QBER ≈ **27.6%** — far above the 11% detection threshold.
- Even **partial eavesdropping** (intercepting a fraction of qubits) produces a detectable increase in QBER proportional to the interception rate.
- The relationship is approximately linear: $\text{QBER} \approx 0.25 \times f$, where $f$ is the interception fraction.

### Key Result 2: Channel Noise Imposes Practical Limits
- Environmental noise contributes to QBER **indistinguishably** from eavesdropping.
- The protocol can tolerate noise levels below approximately **11%** while maintaining security guarantees.
- Beyond this threshold, Alice and Bob cannot distinguish channel noise from an active attack — the key must be discarded.
- This creates a trade-off: noisier channels reduce key generation rate and may prevent secure key exchange entirely.

### Key Result 3: Distance Limitation of Quantum Channels
- Fiber-optic quantum channels suffer **exponential photon loss** (~0.2 dB/km at 1550 nm).
- Practical BB84 implementations over standard fiber are limited to roughly **100 km**.
- Beyond ~300 km, the key rate drops below $10^{-6}$ of the initial rate, making it impractical.
- **Extending range** is an active research area:
  - Quantum repeaters (entanglement swapping + quantum memory)
  - Satellite-based QKD (reduced atmospheric loss)
  - Twin-field QKD protocols (exceeding the fundamental repeaterless bound)

### Key Result 4: Classical Cryptography is Vulnerable to Quantum Attacks
- **Grover's algorithm** effectively halves symmetric key security (AES-256 → 128-bit security, AES-128 → 64-bit security).
- **Shor's algorithm** breaks RSA and Diffie-Hellman in polynomial time, reducing factoring time from billions of years to fractions of a second.
- For RSA-2048: classical factoring takes ~$10^{12}$ years; Shor's algorithm takes ~$10^{-13}$ years.
- BB84 remains secure because its security is based on **physics**, not computational assumptions.

### Key Result 5: Sifted Key Efficiency
- The sifting process retains approximately **50%** of transmitted qubits (consistent with theoretical prediction).
- In our simulation: 2000 qubits → ~1020 sifted key bits (51%).
- After error correction and privacy amplification, the final secure key would be shorter still.

### Comprehensive Comparison

| Criterion | BB84 (Quantum) | Diffie-Hellman | RSA |
|-----------|:--------------:|:--------------:|:---:|
| Security Basis | Laws of quantum physics | Discrete log problem | Integer factorization |
| Security Type | Information-theoretic | Computational | Computational |
| Information-Theoretic Security | ✅ Yes | ❌ No | ❌ No |
| Eavesdropper Detection | ✅ Built-in (QBER) | ❌ None | ❌ None |
| Quantum-Computer Resistant | ✅ Yes | ❌ No (Shor's) | ❌ No (Shor's) |
| Forward Secrecy | ✅ Inherent | ⚠️ Requires ephemeral keys | ❌ No (static keys) |
| Distance Limitation | ⚠️ ~100 km (fiber) | ✅ Unlimited | ✅ Unlimited |
| Infrastructure Requirement | ⚠️ Quantum channel needed | ✅ Standard network | ✅ Standard network |
| Key Generation Speed | ⚠️ ~kbps to Mbps | ✅ Near-instant | ✅ Near-instant |
| Maturity | Research / early commercial | Industry standard | Industry standard |
| Vulnerable to MITM | ⚠️ Requires authenticated classical channel | ⚠️ Without authentication | ⚠️ Without authentication |

---

## Limitations and Future Work

### Current Limitations

1. **Idealized Simulation:** The simulation models perfect single-photon sources and detectors; real hardware has imperfections (multi-photon pulses, dark counts, detector dead time).
2. **Single Attack Model:** Only the intercept-resend attack is simulated; more sophisticated attacks (e.g., beam-splitting, photon number splitting, Trojan horse) are not modeled.
3. **No Error Correction/Privacy Amplification:** The simulation stops at QBER estimation; the full post-processing pipeline (Cascade/LDPC error correction, universal hashing) is not implemented.
4. **Simplified Channel Model:** The noise model uses simple bit-flip errors; real quantum channels exhibit depolarization, phase errors, and other complex noise profiles.
5. **No Finite-Key Effects:** The security analysis assumes asymptotic key lengths; real implementations must account for statistical fluctuations in finite key scenarios.

### Potential Extensions

- Implement the **B92 protocol** (simplified two-state variant) and **E91 protocol** (entanglement-based) for comparison.
- Add **error correction** (Cascade protocol) and **privacy amplification** (Toeplitz hashing) to produce final secure keys.
- Model **photon number splitting (PNS)** attacks against weak coherent pulse sources.
- Implement **decoy-state BB84** which defeats PNS attacks using varying pulse intensities.
- Add a **satellite QKD** distance model (Micius satellite parameters).
- Simulate **quantum repeater chains** to model long-distance QKD networks.
- Include **post-quantum classical algorithms** (lattice-based, code-based) in the comparison.

---

## References

1. Bennett, C.H. & Brassard, G. (1984). *"Quantum cryptography: Public key distribution and coin tossing."* Proceedings of IEEE International Conference on Computers, Systems and Signal Processing, Bangalore, India, pp. 175–179.

2. Shor, P.W. (1994). *"Algorithms for quantum computation: discrete logarithms and factoring."* Proceedings of the 35th Annual Symposium on Foundations of Computer Science, pp. 124–134.

3. Grover, L.K. (1996). *"A fast quantum mechanical algorithm for database search."* Proceedings of the 28th Annual ACM Symposium on Theory of Computing, pp. 212–219.

4. Gisin, N., Ribordy, G., Tittel, W., & Zbinden, H. (2002). *"Quantum cryptography."* Reviews of Modern Physics, 74(1), 145–195.

5. Scarani, V., Bechmann-Pasquinucci, H., Cerf, N.J., Dušek, M., Lütkenhaus, N., & Peev, M. (2009). *"The security of practical quantum key distribution."* Reviews of Modern Physics, 81(3), 1301–1350.

6. Wootters, W.K. & Zurek, W.H. (1982). *"A single quantum cannot be cloned."* Nature, 299, 802–803.

7. Lo, H.K., Curty, M., & Tamaki, K. (2014). *"Secure quantum key distribution."* Nature Photonics, 8, 595–604.

8. Ekert, A.K. (1991). *"Quantum cryptography based on Bell's theorem."* Physical Review Letters, 67(6), 661–663.

9. Diffie, W. & Hellman, M. (1976). *"New directions in cryptography."* IEEE Transactions on Information Theory, 22(6), 644–654.

10. Rivest, R.L., Shamir, A., & Adleman, L. (1978). *"A method for obtaining digital signatures and public-key cryptosystems."* Communications of the ACM, 21(2), 120–126.

11. Lucamarini, M., Yuan, Z.L., Dynes, J.F., & Shields, A.J. (2018). *"Overcoming the rate–distance limit of quantum key distribution without quantum repeaters."* Nature, 557, 400–403.

12. Xu, F., Ma, X., Zhang, Q., Lo, H.K., & Pan, J.W. (2020). *"Secure quantum key distribution with realistic devices."* Reviews of Modern Physics, 92(2), 025002.

---

> **Note:** This project is intended for **educational and research purposes**. The simulations model idealized BB84 behavior; real-world QKD implementations involve additional engineering and security considerations including finite-key effects, detector imperfections, side-channel attacks, authentication requirements, and hardware-specific vulnerabilities. For production security applications, consult established QKD standards (e.g., ETSI QKD specifications).
