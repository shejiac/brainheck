"""Manages the ASR model."""

"""Manages the ASR model."""

import whisper
import tempfile
import os

class ASRManager:
    def __init__(self):
        # Load the Whisper model once
        self.model = whisper.load_model("base")  # Can change to "small", "medium", or "large"

    def asr(self, audio_bytes: bytes) -> str:
        """
        Performs ASR transcription on an audio file.

        Args:
            audio_bytes: The audio file in bytes.

        Returns:
            A string containing the transcription of the audio.
        """
        tmp_path = None  # Declare in outer scope for cleanup

        try:
            # Write audio bytes to a temporary file (delete=False avoids Windows locking issue)
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
                tmpfile.write(audio_bytes)
                tmpfile.flush()
                tmp_path = tmpfile.name

            # Transcribe using Whisper
            result = self.model.transcribe(tmp_path)
            return result["text"]

        except Exception as e:
            return f"❌ Error: {str(e)}"

        finally:
            # Clean up the temp file if it was created
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)
