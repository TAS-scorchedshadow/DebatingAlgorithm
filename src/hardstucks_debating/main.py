import argparse
from hardstucks_debating.debate_runner import DebateRunner
from hardstucks_debating.formats.traditional import TraditionalDebateFormat
from hardstucks_debating.formats.british_parliamentary import BritishParliamentaryFormat
from hardstucks_debating.formats.neo import NewTraditional
from hardstucks_debating.debate_io import DebateIO


def main():
    """Main entry point with interactive format selection or command-line arguments."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Debate room assignment using min-cost max-flow algorithm",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Interactive mode:
    python main.py

  Command-line mode:
    python main.py -i examples/input.csv -o output.csv -f traditional
    python main.py -i examples/input.csv -o output.csv -f bp
        """,
    )
    parser.add_argument("-i", "--input", type=str, help="Input CSV file path")
    parser.add_argument("-o", "--output", type=str, help="Output CSV file path")
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        choices=["traditional", "bp", "british_parliamentary", "neo"],
        help="Debate format (traditional, bp/british_parliamentary, or neo)",
    )

    args = parser.parse_args()

    # Determine if we're in interactive or CLI mode
    # If all arguments are provided, skip interactive prompts
    use_cli_mode = args.input and args.output and args.format

    io = DebateIO()

    # Get format (from CLI or interactive)
    if args.format:
        format_choice = "british_parliamentary" if args.format == "bp" else args.format
    else:
        format_choice = io.get_debate_format()

    # Create appropriate strategy based on selection
    if format_choice == "traditional":
        strategy = TraditionalDebateFormat()
    elif format_choice in ["british_parliamentary", "bp"]:
        strategy = BritishParliamentaryFormat()
    elif format_choice == "neo":
        strategy = NewTraditional()
    else:
        print(f"Unknown format: {format_choice}")
        exit(1)

    # Create runner with custom IO parameters if provided
    runner = DebateRunner(strategy)

    # Override runner's IO methods if CLI arguments provided
    if use_cli_mode:
        # Monkey-patch the IO methods to return CLI arguments
        runner.io.get_input_file = lambda: args.input
        runner.io.get_output_file = lambda: (
            args.output if args.output.endswith(".csv") else args.output + ".csv"
        )
    else:
        # Use interactive mode with defaults if partially specified
        runner.io.get_input_file = lambda: io.get_input_file(args.input)
        runner.io.get_output_file = lambda: io.get_output_file(args.output)

    runner.run()


if __name__ == "__main__":
    main()
