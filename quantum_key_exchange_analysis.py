"""
Quantum Cryptography Key Exchange Analysis
============================================
Analyzes the BB84 quantum key distribution protocol and compares it
with classical key exchange techniques (Diffie-Hellman, RSA).

Includes simulations and matplotlib visualizations for:
  - BB84 protocol simulation and key agreement rates
  - Eavesdropper detection via quantum bit error rate (QBER)
  - Security comparison between quantum and classical approaches
  - Effect of quantum channel noise on key generation
"""

import random
import math
import matplotlib.pyplot as plt
import numpy as np

random.seed(42)
np.random.seed(42)

def simulate_bb84(num_qubits=1000, eavesdrop=False, noise_level=0.0):
    alice_bits = [random.randint(0, 1) for _ in range(num_qubits)]
    alice_bases = [random.randint(0, 1) for _ in range(num_qubits)]

    eve_bases = [random.randint(0, 1) for _ in range(num_qubits)]
    eve_bits = []

    transmitted_bits = list(alice_bits)

    if eavesdrop:
        for i in range(num_qubits):
            if eve_bases[i] == alice_bases[i]:
                eve_bits.append(alice_bits[i])
            else:
                eve_bits.append(random.randint(0, 1))
            transmitted_bits[i] = eve_bits[i]

    for i in range(num_qubits):
        if random.random() < noise_level:
            transmitted_bits[i] ^= 1

    bob_bases = [random.randint(0, 1) for _ in range(num_qubits)]
    bob_bits = []
    for i in range(num_qubits):
        if bob_bases[i] == alice_bases[i]:
            bob_bits.append(transmitted_bits[i])
        else:
            bob_bits.append(random.randint(0, 1))

    sifted_alice = []
    sifted_bob = []
    for i in range(num_qubits):
        if alice_bases[i] == bob_bases[i]:
            sifted_alice.append(alice_bits[i])
            sifted_bob.append(bob_bits[i])

    errors = sum(a != b for a, b in zip(sifted_alice, sifted_bob))
    qber = errors / len(sifted_alice) if sifted_alice else 0.0

    return {
        "num_qubits": num_qubits,
        "sifted_length": len(sifted_alice),
        "sifted_alice": sifted_alice,
        "sifted_bob": sifted_bob,
        "errors": errors,
        "qber": qber,
        "eavesdrop": eavesdrop,
        "noise_level": noise_level,
    }


NUM_QUBITS = 2000

result_clean = simulate_bb84(NUM_QUBITS, eavesdrop=False, noise_level=0.0)
result_eve = simulate_bb84(NUM_QUBITS, eavesdrop=True, noise_level=0.0)

noise_levels = np.linspace(0, 0.5, 30)
qber_vs_noise = []
sifted_len_vs_noise = []
for nl in noise_levels:
    r = simulate_bb84(NUM_QUBITS, eavesdrop=False, noise_level=nl)
    qber_vs_noise.append(r["qber"])
    sifted_len_vs_noise.append(r["sifted_length"])

intercept_fractions = np.linspace(0, 1.0, 30)
qber_vs_intercept = []
for frac in intercept_fractions:
    n = NUM_QUBITS
    alice_bits = [random.randint(0, 1) for _ in range(n)]
    alice_bases = [random.randint(0, 1) for _ in range(n)]
    transmitted = list(alice_bits)
    for i in range(n):
        if random.random() < frac:
            eve_base = random.randint(0, 1)
            if eve_base == alice_bases[i]:
                measured = alice_bits[i]
            else:
                measured = random.randint(0, 1)
            transmitted[i] = measured
    bob_bases = [random.randint(0, 1) for _ in range(n)]
    sifted_a, sifted_b = [], []
    for i in range(n):
        if alice_bases[i] == bob_bases[i]:
            sifted_a.append(alice_bits[i])
            sifted_b.append(transmitted[i])
    errs = sum(a != b for a, b in zip(sifted_a, sifted_b))
    qber_val = errs / len(sifted_a) if sifted_a else 0
    qber_vs_intercept.append(qber_val)

distances_km = np.linspace(0, 300, 100)
alpha_fiber = 0.046
bb84_key_rate = np.exp(-alpha_fiber * distances_km)
bb84_key_rate = np.clip(bb84_key_rate, 0, 1)
classical_rate = np.ones_like(distances_km) * 1.0

key_sizes = [128, 256, 512, 1024, 2048, 4096]
log10_2 = math.log10(2)
log10_ops_per_year = math.log10(1e15 * 3.15e7)  # ~22.5
classical_break_log_years = [(k / 2) * log10_2 - log10_ops_per_year for k in key_sizes]
quantum_break_log_years = [(k / 4) * log10_2 - log10_ops_per_year for k in key_sizes]

rsa_sizes = [512, 1024, 2048, 3072, 4096]
rsa_classical_log = []
for bits in rsa_sizes:
    ln_n = bits * math.log(2)
    ln_ln_n = math.log(ln_n)
    log10_complexity = 1.9 * (ln_n ** (1 / 3)) * (ln_ln_n ** (2 / 3)) * math.log10(math.e)
    log10_years = log10_complexity - log10_ops_per_year
    rsa_classical_log.append(log10_years)

rsa_quantum_log = [math.log10(bits ** 3) - log10_ops_per_year for bits in rsa_sizes]

plt.style.use("seaborn-v0_8-whitegrid")
plt.ion()

# Plot 1: BB84 Sifted Key Comparison
fig1, ax1 = plt.subplots(figsize=(12, 5))
sample = min(50, result_clean["sifted_length"], result_eve["sifted_length"])
x_idx = np.arange(sample)
width = 0.35
ax1.bar(x_idx - width / 2, result_clean["sifted_alice"][:sample],
        width, label="Alice's bits", color="#2196F3", alpha=0.85)
ax1.bar(x_idx + width / 2, result_clean["sifted_bob"][:sample],
        width, label="Bob's bits (no Eve)", color="#4CAF50", alpha=0.85)
mismatches_eve = [i for i in range(sample)
                  if result_eve["sifted_alice"][i] != result_eve["sifted_bob"][i]]
for m in mismatches_eve:
    ax1.axvline(m, color="red", alpha=0.25, linewidth=1)
ax1.set_xlabel("Sifted Key Bit Index")
ax1.set_ylabel("Bit Value")
ax1.set_title("BB84 Sifted Key — First 50 Bits")
ax1.legend(loc="upper right", fontsize=8)
ax1.set_yticks([0, 1])
plt.tight_layout()
plt.savefig("plot1_bb84_sifted_key.png", dpi=200, bbox_inches="tight")

# Plot 2: QBER vs Eavesdropper Interception Fraction
fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.plot(intercept_fractions * 100, np.array(qber_vs_intercept) * 100,
         "o-", color="#E91E63", markersize=4, linewidth=2, label="Measured QBER")
ax2.axhline(y=25, color="gray", linestyle="--", linewidth=1, label="Theoretical max (25%)")
ax2.axhline(y=11, color="orange", linestyle="--", linewidth=1, label="Security threshold (11%)")
ax2.fill_between(intercept_fractions * 100, 11, 50,
                 alpha=0.10, color="red", label="Insecure region")
ax2.fill_between(intercept_fractions * 100, 0, 11,
                 alpha=0.10, color="green", label="Secure region")
ax2.set_xlabel("Eve's Interception Fraction (%)")
ax2.set_ylabel("Quantum Bit Error Rate — QBER (%)")
ax2.set_title("Eavesdropper Detection via QBER")
ax2.legend(fontsize=7, loc="upper left")
ax2.set_xlim(0, 100)
ax2.set_ylim(0, 35)
plt.tight_layout()
plt.savefig("plot2_qber_vs_interception.png", dpi=200, bbox_inches="tight")

# Plot 3: QBER vs Channel Noise
fig3, ax3 = plt.subplots(figsize=(10, 6))
ax3.plot(noise_levels * 100, np.array(qber_vs_noise) * 100,
         "s-", color="#9C27B0", markersize=4, linewidth=2, label="QBER (no Eve)")
ax3.axhline(y=11, color="orange", linestyle="--", linewidth=1, label="Security threshold (11%)")
ax3.fill_between(noise_levels * 100, 0, 11,
                 alpha=0.10, color="green")
ax3.fill_between(noise_levels * 100, 11, 55,
                 alpha=0.10, color="red")
ax3.set_xlabel("Channel Noise Level (%)")
ax3.set_ylabel("QBER (%)")
ax3.set_title("Effect of Quantum Channel Noise on QBER")
ax3.legend(fontsize=8)
ax3.set_ylim(0, 55)
plt.tight_layout()
plt.savefig("plot3_qber_vs_noise.png", dpi=200, bbox_inches="tight")

# Plot 4: Key Generation Rate vs Distance
fig4, ax4 = plt.subplots(figsize=(10, 6))
ax4.semilogy(distances_km, bb84_key_rate, linewidth=2.5,
             color="#FF5722", label="BB84 (fiber, ~0.2 dB/km)")
ax4.semilogy(distances_km, classical_rate, linewidth=2.5,
             linestyle="--", color="#3F51B5", label="Classical (network-based)")
ax4.axvline(x=100, color="gray", linestyle=":", alpha=0.5)
ax4.text(102, 0.5, "~100 km practical\nlimit (fiber)", fontsize=7, color="gray")
ax4.set_xlabel("Distance (km)")
ax4.set_ylabel("Relative Key Rate")
ax4.set_title("Key Rate vs Distance — Quantum vs Classical")
ax4.legend(fontsize=8)
ax4.set_ylim(1e-7, 2)
plt.tight_layout()
plt.savefig("plot4_key_rate_vs_distance.png", dpi=200, bbox_inches="tight")

# Plot 5: Time to Break Symmetric Keys
fig5, ax5 = plt.subplots(figsize=(10, 6))
x_pos = np.arange(len(key_sizes))
width = 0.35
bars1 = ax5.bar(x_pos - width / 2, classical_break_log_years, width,
                label="Classical attack", color="#2196F3", alpha=0.85)
bars2 = ax5.bar(x_pos + width / 2, quantum_break_log_years, width,
                label="Quantum (Grover's)", color="#F44336", alpha=0.85)
ax5.set_xlabel("Symmetric Key Size (bits)")
ax5.set_ylabel("log10(Time to Break in years)")
ax5.set_title("Classical vs Quantum Attack on Symmetric Keys")
ax5.set_xticks(x_pos)
ax5.set_xticklabels(key_sizes)
ax5.legend(fontsize=8)
ax5.axhline(y=10, color="green", linestyle="--", alpha=0.5, linewidth=1)
ax5.text(0, 11, "Age of Universe", fontsize=7, color="green")
plt.tight_layout()
plt.savefig("plot5_symmetric_key_attack.png", dpi=200, bbox_inches="tight")

# Plot 6: RSA Factoring — Classical vs Shor's Algorithm
fig6, ax6 = plt.subplots(figsize=(10, 6))
x_rsa = np.arange(len(rsa_sizes))
ax6.bar(x_rsa - width / 2, rsa_classical_log, width,
        label="Classical (GNFS)", color="#FF9800", alpha=0.85)
ax6.bar(x_rsa + width / 2, rsa_quantum_log, width,
        label="Quantum (Shor's)", color="#E91E63", alpha=0.85)
ax6.set_xlabel("RSA Key Size (bits)")
ax6.set_ylabel("log10(Time to Factor in years)")
ax6.set_title("RSA Vulnerability — Classical vs Quantum Factoring")
ax6.set_xticks(x_rsa)
ax6.set_xticklabels(rsa_sizes)
ax6.legend(fontsize=8)
plt.tight_layout()
plt.savefig("plot6_rsa_vulnerability.png", dpi=200, bbox_inches="tight")

plt.ioff()
plt.show()


print("=" * 65)
print("  QUANTUM CRYPTOGRAPHY KEY EXCHANGE — SIMULATION RESULTS")
print("=" * 65)

print(f"\n{'─'*65}")
print("  BB84 Protocol (No Eavesdropper, No Noise)")
print(f"{'─'*65}")
print(f"  Qubits sent        : {result_clean['num_qubits']}")
print(f"  Sifted key length  : {result_clean['sifted_length']}")
print(f"  Bit errors         : {result_clean['errors']}")
print(f"  QBER               : {result_clean['qber']:.4f}  (expected ~0)")

print(f"\n{'─'*65}")
print("  BB84 Protocol (With Eavesdropper)")
print(f"{'─'*65}")
print(f"  Qubits sent        : {result_eve['num_qubits']}")
print(f"  Sifted key length  : {result_eve['sifted_length']}")
print(f"  Bit errors         : {result_eve['errors']}")
print(f"  QBER               : {result_eve['qber']:.4f}  (expected ~0.25)")
print(f"  Eve detected?      : {'YES' if result_eve['qber'] > 0.11 else 'NO'}")

print(f"\n{'─'*65}")
print("  Security Comparison Summary")
print(f"{'─'*65}")
print("  ┌──────────────────┬──────────────────┬──────────────────┐")
print("  │ Property         │ BB84 (Quantum)   │ Classical (DH)   │")
print("  ├──────────────────┼──────────────────┼──────────────────┤")
print("  │ Security basis   │ Quantum physics  │ Math complexity  │")
print("  │ Forward secrecy  │ Inherent         │ Requires config  │")
print("  │ Eve detection    │ Yes (QBER)       │ No               │")
print("  │ Quantum-safe     │ Yes              │ No (Shor's alg.) │")
print("  │ Distance limit   │ ~100 km (fiber)  │ Unlimited        │")
print("  │ Infrastructure   │ Quantum channel  │ Standard network │")
print("  └──────────────────┴──────────────────┴──────────────────┘")

print(f"\n{'─'*65}")
print("  Plots saved to: plot1 through plot6 PNG files")
print("=" * 65)
