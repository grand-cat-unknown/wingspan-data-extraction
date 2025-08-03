# Wingspan Data Extraction

A Python tool that extracts scoring data from Wingspan board game images using Google's Gemini AI. This tool processes images of Wingspan scoring sheets and converts them into structured JSON data.

## Overview

This project uses computer vision and LLM capabilities to automatically extract tabular scoring data from Wingspan game photos. It identifies and extracts values for different scoring categories including birds, bonus cards, end-of-round goals, eggs, and more.

## Features

- 🎯 **Automated Data Extraction**: Uses Google Gemini AI to extract scoring data from images
- 📊 **Structured Output**: Returns data in JSON format with clear categorization
- 💰 **Cost Tracking**: Monitors API usage and associated costs
- 📁 **Batch Processing**: Can process multiple images at once
- 🔄 **Error Handling**: Graceful handling of processing errors

## Setup

### Prerequisites

- Python 3.8+
- Google Gemini API key
- `uv` for dependency management (recommended)

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd wingspan-data-extraction
   ```
2. **Install dependencies**

   Using uv (recommended):

   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -r requirements.txt
   ```

   Or using pip:

   ```bash
   pip install -r requirements.txt
   ```
3. **Set up environment variables**

   Create a `.env` file in the project root:

   ```bash
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Usage

### Basic Usage

The main functionality is in `read_data.py`. You can use it in several ways:

#### 1. Process a Directory of Images

By default, the script processes all PNG files in the `image_data` directory:

```bash
python read_data.py
```

#### 2. Process a Single Image

```python
from read_data import extract_tables_with_llm

# Extract data from a single image
result = extract_tables_with_llm("path/to/your/image.png")
print(result)
```

#### 3. Process Custom Directory

```python
from read_data import extract_tables_from_images

# Process images from a custom directory
results = extract_tables_from_images("your_custom_directory")
```

### Input Requirements

- **Image Format**: PNG files
- **Image Content**: Clear photos of Wingspan scoring sheets
- **Directory Structure**: Place images in a directory (default: `wingspan_data_rotated`)

### Output Structure

The tool extracts the following scoring categories:

```json
{
  "data": {
    "multi_player": ["Player1", "Player2", "Player3"],
    "vogels": [25, 30, 28],
    "bonuskaarten": [8, 12, 10],
    "einde_ronde_doelen": [15, 18, 12],
    "eieren": [6, 8, 7],
    "voedsel_op_kaarten": [3, 5, 4],
    "weggestopte_kaarten": [2, 3, 1],
    "totaal": [59, 76, 62]
  },
  "usage": {
    "input_tokens": 1250,
    "output_tokens": 180,
    "total_tokens": 1430
  },
  "cost": {
    "input_cost": 0.000125,
    "output_cost": 0.000072,
    "total_cost": 0.000197,
    "input_cost_per_million": 0.1,
    "output_cost_per_million": 0.4
  }
}
```

### Output Files

- **Individual JSON files**: Created in `{input_directory}_output/`
- **Console output**: Summary of all processed files

## Data Categories

The tool extracts data for these Wingspan scoring categories:

| Category                | Description              | Data Type        |
| ----------------------- | ------------------------ | ---------------- |
| `multi_player`        | Player names             | Array of strings |
| `vogels`              | Bird points              | Array of numbers |
| `bonuskaarten`        | Bonus card points        | Array of numbers |
| `einde_ronde_doelen`  | End-of-round goal points | Array of numbers |
| `eieren`              | Egg points               | Array of numbers |
| `voedsel_op_kaarten`  | Food on cards points     | Array of numbers |
| `weggestopte_kaarten` | Tucked card points       | Array of numbers |
| `totaal`              | Total scores             | Array of numbers |

## Configuration

### Cost Management

You can customize the cost calculation by modifying the cost parameters:

```python
result = extract_tables_with_llm(
    "image.png",
    input_cost_per_million=0.1,    # Cost per million input tokens
    output_cost_per_million=0.4    # Cost per million output tokens
)
```

### Model Configuration

The tool uses `gemini-2.5-flash-lite-preview-06-17` by default. You can modify the model in the `extract_tables_with_llm` function if needed.

## Deployment

### Google Cloud Run

This project is designed to be deployable on Google Cloud Run. For deployment:

1. **Create a Dockerfile** (example):

   ```dockerfile
   FROM python:3.11-slim

   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt

   COPY . .

   CMD ["python", "read_data.py"]
   ```
2. **Deploy to Cloud Run**:

   ```bash
   gcloud run deploy wingspan-data-extraction \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

## Error Handling

The tool includes robust error handling:

- Continues processing other images if one fails
- Logs errors with specific file information
- Returns partial results for successful extractions

## Dependencies

- `google-genai`: Google Gemini AI client
- `pillow`: Image processing capabilities
- `python-dotenv`: Environment variable management

## Troubleshooting

### Common Issues

1. **Missing API Key**: Ensure `GEMINI_API_KEY` is set in your `.env` file
2. **Image Quality**: Ensure images are clear and well-lit
3. **File Format**: Only PNG files are supported by default
4. **Directory Not Found**: Check that the input directory exists and contains PNG files

### Getting Help

- Check that your Gemini API key is valid and has sufficient quota
- Ensure images contain visible Wingspan scoring tables
- Verify that the image text is in the expected language (Dutch categories)

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]
