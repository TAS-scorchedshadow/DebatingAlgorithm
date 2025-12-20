from debate_runner import DebateRunner
from debate_formats.british_parliamentary import BritishParliamentaryFormat


def main():
    strategy = BritishParliamentaryFormat()
    runner = DebateRunner(strategy)
    runner.run()

if __name__ == "__main__":
    main()
