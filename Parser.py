import json

def transform_vscode_snippet(snippet_object):
    # Copy actual parameter into a new object to be transformed and returned
    t = snippet_object.copy()

    # Transform t as necessary such that the following hold:
    #   1. t.prefix is of type String
    #   2. t.body   is of type List<String>
    #   3. t.description exists, defaulting to t.prefix if absent
    if type(t["prefix"]) is     list: t["prefix"] = str(t["prefix"][0])
    if type(t["body"])   is not list: t["body"]   = [str(t["body"])]
    if not t.get("description"): t["description"] = t["prefix"]

    # Return transformed copy to Caller
    return t

# Custom dict parser to be used as object_hook in json.load()
# Routes input snippet object to the correct transformation function
def transform_source_object(snippet_object):
    # For now, only VSCode Snippet-like source objects are supported
    if "prefix" in snippet_object and "body" in snippet_object:
        return transform_vscode_snippet(snippet_object)

    # TODO: Inform user of unsupported snippet object syntax
    return snippet_object

# Parse JSON source file(s) from input list into a single program object
def parse_source_files(filepaths):
    # Create a blank dict that we'll then populate with parsed Snippet data
    snippets = dict()
    
    # Do the parsing, catching any related userspace errors
    try:
        for path in filepaths:
            with open(path, mode="r", encoding="utf-8") as f:
                source_dict = json.load(f, object_hook=transform_source_object)
                snippets.update(source_dict) # add all k/v pairs to unified dict
    except FileNotFoundError:
        raise SystemExit(f"Error: Source JSON file at path '{path}' not found")
    except json.decoder.JSONDecodeError:
        raise SystemExit(f"Error: JSON syntax error in file at '{path}'")
        
    return snippets

