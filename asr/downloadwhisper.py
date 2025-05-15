import whisper

# Replace "base" with "tiny", "small", "medium", or "large" if needed
model = whisper.load_model("base", download_root="models/openai-whisper")
