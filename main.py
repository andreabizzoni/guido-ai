from app.agent import Agent
from app.voice_input import VoiceInput


def main() -> None:
    print("\nProgram starting")
    agent = Agent()
    voice_input: VoiceInput | None = None
    voice_mode = False

    def on_transcription(text: str) -> None:
        nonlocal agent
        print(f"\nYou said: {text}")
        try:
            agent_answer = agent.answer(text)
            print(f"\nGuido: {agent_answer}")
        except Exception as e:
            print(f"\nError processing query: {e}")

    while True:
        try:
            if not voice_mode:
                user_query = input("\nYou: ").strip()

                if not user_query:
                    continue

                if user_query.lower() in ["exit", "quit", "q"]:
                    break

                if user_query.lower() in ["voice", "v"]:
                    # Switch to voice mode
                    try:
                        voice_input = VoiceInput(agent.client)
                        voice_input.on_transcription_complete = on_transcription
                        voice_input.start_listening()
                        voice_mode = True
                        print("\nVoice mode activated! Hold SPACE to record, release to transcribe.")
                        print("Type 'text' or 't' to return to text mode.\n")
                    except ImportError as e:
                        print(f"\nMissing required dependencies: {e}")
                        print("Please install dependencies: pip install pynput sounddevice numpy")
                    except Exception as e:
                        print(f"\nError starting voice mode: {e}")
                        print("Make sure your microphone is available and permissions are granted.")
                        print("On macOS, you may need to grant Terminal/IDE microphone access in System Settings.")
                    continue

                agent_answer = agent.answer(user_query)
                print(f"\nGuido: {agent_answer}")

            else:
                # Voice mode - wait for user input to switch back or exit
                user_input = input().strip().lower()
                if user_input in ["text", "t"]:
                    if voice_input:
                        voice_input.stop_listening()
                        voice_input.cleanup()
                        voice_input = None
                    voice_mode = False
                    print("\nSwitched to text mode.")
                elif user_input in ["exit", "quit", "q"]:
                    break

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n\nError while running Guido - {e}")

    # Cleanup
    if voice_input:
        voice_input.cleanup()

    print("\nProgram terminated\n")


if __name__ == "__main__":
    main()
