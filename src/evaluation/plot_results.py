import os
import matplotlib.pyplot as plt


RESULTS_DIR = "results"

os.makedirs(RESULTS_DIR, exist_ok=True)


detectors = [
    "spaCy",
    "Hugging Face",
    "GLiNER"
]


# ============================================================
# 1. F1 SCORE
# ============================================================

f1_scores = [
    0.538,
    0.809,
    0.945
]

plt.figure(figsize=(8, 5))

plt.bar(detectors, f1_scores)

plt.ylabel("F1 Score")
plt.title("Overall Detection F1 Score")
plt.ylim(0, 1)

for i, value in enumerate(f1_scores):
    plt.text(
        i,
        value + 0.02,
        f"{value:.3f}",
        ha="center"
    )

plt.tight_layout()

plt.savefig(
    os.path.join(
        RESULTS_DIR,
        "f1_comparison.png"
    ),
    dpi=200
)

plt.close()


# ============================================================
# 2. INFERENCE TIME
# ============================================================

inference_times = [
    0.007005,
    0.024019,
    0.057125
]

plt.figure(figsize=(8, 5))

plt.bar(detectors, inference_times)

plt.ylabel("Seconds per Example")
plt.title("Average Inference Time per Example")

for i, value in enumerate(inference_times):
    plt.text(
        i,
        value + 0.001,
        f"{value:.4f}s",
        ha="center"
    )

plt.tight_layout()

plt.savefig(
    os.path.join(
        RESULTS_DIR,
        "inference_time_comparison.png"
    ),
    dpi=200
)

plt.close()


# ============================================================
# 3. END-TO-END EXACT OUTPUT MATCH
# ============================================================

exact_match = [
    0.028,
    0.528,
    0.806
]

plt.figure(figsize=(8, 5))

plt.bar(detectors, exact_match)

plt.ylabel("Exact Output Match Rate")
plt.title("End-to-End Exact Output Match")
plt.ylim(0, 1)

for i, value in enumerate(exact_match):
    plt.text(
        i,
        value + 0.02,
        f"{value * 100:.1f}%",
        ha="center"
    )

plt.tight_layout()

plt.savefig(
    os.path.join(
        RESULTS_DIR,
        "exact_output_match.png"
    ),
    dpi=200
)

plt.close()


print("Plots generated successfully.")

print(f"- {RESULTS_DIR}/f1_comparison.png")
print(f"- {RESULTS_DIR}/inference_time_comparison.png")
print(f"- {RESULTS_DIR}/exact_output_match.png")