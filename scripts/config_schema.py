import json
from copia.cli.config import Profile

def generate_schema() -> dict:
    profile_schema = Profile.model_json_schema()
    
    # inject enumDescriptions manually since it's non-standard
    if "properties" in profile_schema:
        adapter = profile_schema["properties"].get("adapter", {})
        if "enum" in adapter:
            adapter["enumDescriptions"] = ["MySQL / MariaDB", "PostgreSQL"]

    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "$id": "https://raw.githubusercontent.com/gitmobkab/copia/main/docs/configuration/schema.json",
        "title": "Copia Configuration",
        "description": "Configuration schema for copia - https://gitmobkab.github.io/copia/configuration",
        "type": "object",
        "properties": {
            "profiles": {
                "type": "object",
                "description": "Named database connection profiles.",
                "additionalProperties": {"$ref": "#/$defs/Profile"},
            }
        },
        "$defs": {"Profile": profile_schema},
    }

if __name__ == "__main__":
    schema = generate_schema()
    output = "docs/configuration/schema.json"
    with open(output, "w") as f:
        json.dump(schema, f, indent=4)