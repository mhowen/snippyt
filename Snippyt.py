import argparse, os
import Parser
from Clipboarder import Clipboarder

# Create a minimal snippets.json file that encourages user additions
def create_default_snippets_file():
    print("Creating default snippets.json source file...")

    with open("snippets.json", mode="w", encoding="utf-8") as f:
        f.write('{\n\t"Example Snippet": {\n')
        f.write('\t\t"prefix": "example",\n')
        f.write('\t\t"body": ["Demo Snippet"],\n')
        f.write('\t\t"description": "Add your own snippets to this file"\n')
        f.write('\t}\n}\n')

# Check for snippets.json and create it if it doesn't exist
def get_default_snippets_file():
    if not os.path.isfile("snippets.json"):
        try: create_default_snippets()
        except Exception:
            raise SystemExit("Error: Couldn't create default source file")

    # Return a list containing just the now-verified-to-exist file
    return ["snippets.json"]

if __name__ == "__main__":
    # Configure argparser and parse CLI args
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "SNIPPET",
        help="Key string associated with desired Snippet in source file(s)",
    )
    argparser.add_argument(
        "-p", "--preprocessor",
        help="Name of preprocessor to invoke before providing Snippet",
    )
    argparser.add_argument(
        "-f", "--files",
        help="Path(s) to source JSON file(s) to read instead of default",
        nargs="*", # User can list as many source files as they like
    )
    args = argparser.parse_args()

    # If user specified no source file(s), parse the default source file
    if not args.files: args.files = get_default_snippets_file()

    # Load in snippet data from source file(s)
    snippets = Parser.parse_source_files(args.files)

    # Ensure requested snippet is present before continuing
    if not snippets.get(args.SNIPPET):
        raise SystemExit(f"Key Error: Snippet '{args.SNIPPET}' not found")

    # Configure a Clipboarder object with user-argued preprocessor, if any
    cb = Clipboarder(args.preprocessor)

    # Attempt to preprocess and provide the snippet
    selected = snippets[args.SNIPPET]
    cb.provide(selected)

