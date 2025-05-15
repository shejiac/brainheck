import base64
import requests
import jiwer
import os

# === Test dataset: list of (file_path, ground_truth_text) ===
test_data = [
    ("/home/jupyter/brainheck/asr/iamthebesthumantoeverexist.wav", "i am the best human to ever exist"),
    ("/home/jupyter/brainheck/asr/iaskofu.wav", "i ask that you do not choose immediately to shut this out"),
]

# === Format request payload ===
instances = []
for idx, (path, _) in enumerate(test_data):
    with open(path, "rb") as f:
        audio_bytes = f.read()
        b64_audio = base64.b64encode(audio_bytes).decode("utf-8")
        instances.append({"key": idx, "b64": b64_audio})

payload = {"instances": instances}
url = "http://localhost:5001/asr"
headers = {"Content-Type": "application/json"}

# === Send POST request ===
response = requests.post(url, headers=headers, json=payload)
predictions = response.json()["predictions"]

# === WER transform as specified by challenge ===
transform = jiwer.Compose([
    jiwer.ToLowerCase(),
    jiwer.SubstituteRegexes({"-": " "}),
    jiwer.RemovePunctuation(),
    jiwer.ReduceToListOfListOfWords(),
])

# === Print results ===
print("\n--- Batch ASR Evaluation ---")
for idx, (predicted, (_, ground_truth)) in enumerate(zip(predictions, test_data)):
    wer = jiwer.wer(
        ground_truth,
        predicted,
        truth_transform=transform,
        hypothesis_transform=transform,
    )
    score = max(0, 1 - wer)

    print(f"\n[Sample {idx}]")
    print(f"Prediction:   {predicted}")
    print(f"Ground Truth: {ground_truth}")
    print(f"WER:          {wer:.4f}")
    print(f"Score:        {score:.4f}")
