import subprocess
from shutil import which

class Clipboarder:
    # Based on pre-selected executable, return the corresponding shell command
    def get_command(self):
        # For the moment, only xclip and xsel are supported
        if self.executable == "xclip":
            return [self.executable, "-i", "-selection", "clipboard"]
        elif self.executable == "xsel":
            return [self.executable, "-i", "-b"]
        # TODO: Check whether wl-copy is usable in current environment
            
        return args

    # Get a lambda function to adjust snippet immediately prior to its provision
    def configure_preprocessor(self, preprocessor):
        match preprocessor:
            case None: # If user argued no preprocessor, just pass through
                return lambda body: body
            case "tex-inline":
                return lambda body: "$" + body + "$"
            case "tex-block":
                return lambda body: "$$" + body + "$$"
            case _:    # Matches if user argued an unrecognized preprocessor
                print("Unrecognized preprocessor; attempting to provide as-is")
                return lambda body: body

    def __init__(self, preprocessor=None):
        # Determine most suitable interface to the system clipboard
        # For the moment, only xclip and xsel are supported
        if   which("xclip"): self.executable = "xclip"
        elif which("xsel"): self.executable = "xsel"
        else:
            raise SystemExit(f"Error: No supported clipboard interface found")
        
        self.command = self.get_command()
        self.preprocessor = self.configure_preprocessor(preprocessor)

    # Convert list of strings to newline-separated string for the clipboard
    def format_for_clipboard(self, body):
        if type(body) is not list:
            raise SystemExit(f"Error: Noncompliant snippet body\n\t--> {body}")

        formatted_string = "" # To be populated with clipboard-formatted body
        num_lines = len(body) # Each non-final line is to be delimited by '\n'
        line_index = 0        # Used to ID final line and skip appending '\n'
        # Concatenate newline-separated lines into one copyable string
        while line_index < num_lines:
            formatted_string += body[line_index]
            if line_index < num_lines - 1: formatted_string += "\n"
            line_index += 1

        # Any final adjustments are done by the preprocessor lambda function
        return formatted_string
    
    # Hand over formatted input body to the pre-configured subprocess
    def provide(self, snippet):
        # Catch any goofy misconfigurations
        if not self.executable or not self.command:
            print("Clipboarder Error: Unconfigured provision interface")
            return
        if not snippet.get("body"):
            print("Clipboarder Error: Tried to provide snippet without body")
            return

        # Catch any errors in body syntax
        formatted_body = self.format_for_clipboard(snippet["body"])

        # Offer user some feedback in the CLI to indicate success
        print(f"Providing: {self.preprocessor(formatted_body)}")

        # Execute the now-validated configuration
        subprocess.run(
            self.command,
            input=self.preprocessor(formatted_body), # Gets passed as STDIN
            encoding="utf-8",
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )

