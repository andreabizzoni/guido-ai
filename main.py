from app.agent import Agent


def main() -> None:
    print("\nProgram starting")
    agent = Agent()

    while True:
        try:
            user_query = input("\nYou: ").strip()

            if not user_query:
                continue

            if user_query.lower() in ["exit", "quit", "q"]:
                break

            agent_answer = agent.answer(user_query)

            print(f"\nGuido: {agent_answer}")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n\nError while running Guido - {e}")

    print("\nProgram terminated\n")


if __name__ == "__main__":
    main()
