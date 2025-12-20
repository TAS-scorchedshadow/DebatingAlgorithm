from debate_runner import DebateRunner
from debate_formats.traditional import TraditionalDebateFormat


def main():
    strategy = TraditionalDebateFormat()
    runner = DebateRunner(strategy)
    runner.run()

if __name__ == "__main__":
    main()
