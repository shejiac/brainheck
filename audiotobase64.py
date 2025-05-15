import base64
import pyperclip
import json

with open("C:\\Users\\cshej\\Downloads\\iaskofu.wav", "rb") as f:
    audio_bytes = f.read()

b64_audio = base64.b64encode(audio_bytes).decode("utf-8")

# Wrap in correct JSON payload
payload = {
    "instances": [
        {
            "key": 0,
            "b64": b64_audio
        }
    ]
}

# Copy entire JSON to clipboard
json_payload = json.dumps(payload)
pyperclip.copy(json_payload)

with open("C:\\Users\\cshej\\Downloads\\iaskofu_payload.json", "w") as out:
    out.write(json_payload)

print("✅ Copied full JSON to clipboard.")
