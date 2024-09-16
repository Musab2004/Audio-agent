import asyncio
from stt import speech_to_text
from tts import TextToSpeech
from llm import LLM

class TalkingAgent:
    def __init__(self):
        self.transcription_response = ""
        self.stt = speech_to_text        
        self.tts = TextToSpeech()
        self.llm = LLM()

    async def start(self):
        def handle_full_sentence(full_sentence):
            self.transcription_response = full_sentence

        # Loop indefinitely until "goodbye" is detected
        while True:
            await self.stt(handle_full_sentence)
            
            # Check for "goodbye" to exit the loop
            if "goodbye" in self.transcription_response.lower():
                break
            
            if self.transcription_response != "":
                response = self.llm.process(self.transcription_response)

                self.tts.speak(response)

                # Reset transcription_response for the next loop iteration
                self.transcription_response = ""

if __name__ == "__main__":
    agent = TalkingAgent()
    asyncio.run(agent.start())