import os
import sys
import time
import subprocess
import psutil

from evaluation.ground_truth import GROUND_TRUTH


def create_detector(name):

    if name == "spaCy":
        from detection.spacy_detector import SpacyDetector
        return SpacyDetector()

    elif name == "Hugging Face":
        from detection.hf_detector_class import HuggingFaceDetector
        return HuggingFaceDetector()

    elif name == "GLiNER":
        from detection.gliner_detector_class import GlinerDetector
        return GlinerDetector()

    else:
        raise ValueError(f"Unknown detector: {name}")


def run_benchmark(name):

    process = psutil.Process(os.getpid())

    print(f"\n===== {name} =====")

    # Measure detector/model loading time
    start_loading = time.perf_counter()

    detector = create_detector(name)

    end_loading = time.perf_counter()

    loading_time = end_loading - start_loading

    memory_after_loading = (
        process.memory_info().rss / (1024 * 1024)
    )

    # Warm-up
    for example in GROUND_TRUTH:
        detector.detect(example["text"])

    # Measure inference time
    repetitions = 3
    inference_times = []

    for _ in range(repetitions):

        start_inference = time.perf_counter()

        for example in GROUND_TRUTH:
            detector.detect(example["text"])

        end_inference = time.perf_counter()

        inference_times.append(
            end_inference - start_inference
        )

    average_inference_time = (
        sum(inference_times) / len(inference_times)
    )
    number_of_examples = len(GROUND_TRUTH)

    average_time_per_example = (
        average_inference_time / number_of_examples
    )    
    memory_after_inference = (
        process.memory_info().rss / (1024 * 1024)
    )

    print(
        f"Model loading time: "
        f"{loading_time:.4f} seconds"
    )
    print(
    f"Number of examples: "
    f"{number_of_examples}"
    )

    print(
    f"Average inference time per example: "
    f"{average_time_per_example:.6f} seconds"
    )
    
    print(
        f"Memory after model loading: "
        f"{memory_after_loading:.2f} MB"
    )

    print(
        f"Average inference time: "
        f"{average_inference_time:.4f} seconds"
    )

    print(
        f"Memory after inference: "
        f"{memory_after_inference:.2f} MB"
    )


def main():

    detector_names = [
        "spaCy",
        "Hugging Face",
        "GLiNER"
    ]

    for name in detector_names:

        subprocess.run(
            [
                sys.executable,
                "-m",
                "evaluation.performance",
                name
            ],
            check=True
        )


if __name__ == "__main__":

    if len(sys.argv) > 1:
        run_benchmark(sys.argv[1])
    else:
        main()