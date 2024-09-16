from deepgram import DeepgramClient, SpeakOptions
from dotenv import load_dotenv
import subprocess
import os
import tempfile

load_dotenv()


class TextToSpeech:
    def __init__(self):
        self.api_key = os.getenv("DEEPGRAM_API_KEY")
        self.deepgram = DeepgramClient(self.api_key)

    def speak(self, text, model="aura-stella-en"):
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
                temp_filename = temp_file.name

            # Generate the audio file
            options = SpeakOptions(model=model)
            text_dict = {"text": text}
            self.deepgram.speak.v("1").save(temp_filename, text_dict, options)

            # Play the audio file using ffplay
            if os.path.exists(temp_filename):
                subprocess.run(["ffplay", "-nodisp", "-autoexit", temp_filename])
            else:
                print(f"Error: {temp_filename} not found.")

        except Exception as e:
            print(f"Exception: {e}")

        finally:
            # Remove the temporary audio file
            if os.path.exists(temp_filename):
                os.remove(temp_filename)


def main():

    player = TextToSpeech()

    text = "Aqib is person. erganzen sie ?"
    player.speak(text)


if __name__ == "__main__":
    main()
