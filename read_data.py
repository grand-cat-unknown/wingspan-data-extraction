import base64
import os
import glob
import json
from google import genai
from google.genai import types

from dotenv import load_dotenv

load_dotenv()


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def extract_tables_with_llm(
    image_path, input_cost_per_million=0.1, output_cost_per_million=0.4
):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.5-flash-lite-preview-06-17"

    # Read and encode image
    with open(image_path, "rb") as f:
        image_data = f.read()

    schema = {
        "type": "object",
        "properties": {
            "multi_player": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of strings for Multi-player row",
            },
            "vogels": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of numbers for Vogels row",
            },
            "bonuskaarten": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of numbers for Bonuskaarten row",
            },
            "einde_ronde_doelen": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of numbers for 'Einde ronde'-Doelen row",
            },
            "eieren": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of numbers for Eieren row",
            },
            "voedsel_op_kaarten": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of numbers for Voedsel op kaarten row",
            },
            "weggestopte_kaarten": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of numbers for Weggestopte kaarten row",
            },
            "totaal": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of numbers for Totaal row",
            },
        },
        "required": [
            "multi_player",
            "vogels",
            "bonuskaarten",
            "einde_ronde_doelen",
            "eieren",
            "voedsel_op_kaarten",
            "weggestopte_kaarten",
            "totaal",
        ],
    }

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text="Extract the scoring table from this Wingspan game image. For each row labeled 'Multi-player', 'Vogels', 'Bonuskaarten', '\"Einde ronde\"-Doelen', 'Eieren', 'Voedsel op kaarten', 'Weggestopte kaarten', 'Totaal', return the list of values. For Multi-player return strings, for all others return numbers."
                ),
                types.Part.from_bytes(data=image_data, mime_type="image/png"),
            ],
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_budget=0,
        ),
        response_mime_type="application/json",
        response_schema=schema,
    )

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )

    input_tokens = response.usage_metadata.prompt_token_count
    output_tokens = response.usage_metadata.candidates_token_count
    total_tokens = response.usage_metadata.total_token_count

    input_cost = (input_tokens / 1000000) * input_cost_per_million
    output_cost = (output_tokens / 1000000) * output_cost_per_million
    total_cost = input_cost + output_cost

    result = {
        "data": json.loads(response.text),
        "usage": {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
        },
        "cost": {
            "input_cost": input_cost,
            "output_cost": output_cost,
            "total_cost": total_cost,
            "input_cost_per_million": input_cost_per_million,
            "output_cost_per_million": output_cost_per_million,
        },
    }

    return result


def extract_tables_from_images(data_dir="images"):
    png_files = glob.glob(os.path.join(data_dir, "*.png"))
    output_dir = data_dir + "_output"

    os.makedirs(output_dir, exist_ok=True)

    all_results = {}

    for file in png_files:
        print(f"Processing {file}...")
        try:
            table_data = extract_tables_with_llm(file)
            filename = os.path.basename(file)
            json_filename = filename.replace(".png", ".json")
            output_path = os.path.join(output_dir, json_filename)

            with open(output_path, "w") as f:
                json.dump(table_data, f, indent=2)

            all_results[filename] = table_data
        except Exception as e:
            print(f"Error processing {file}: {e}")
            continue

    return all_results


if __name__ == "__main__":
    results = extract_tables_from_images()
    print("Tables extracted and saved to wingspan_data_sample_rotated_output/ folder")
    print(json.dumps(results, indent=2))
