# R2K ChatEval Framework

## Overview

R2K ChatEval is an advanced, Python-based framework designed for comprehensive evaluation of chatbot responses. Developed by Rama Nagireddi, this framework introduces several innovative features, including multi-modal metric fusion, dynamic evaluation mode switching, content safety verification with contextual exception handling, and API failure resilience with graceful degradation. It is particularly notable for its ability to function effectively even without ground truth, making it a versatile tool for AI developers in selecting and refining chatbot models.

## Features

- **Multi-modal Metric Fusion Engine**: Combines various metrics (BLEU, ROUGE, Cosine Similarity, Length Ratio) for a holistic evaluation when ground truth is available.
- **Dynamic Evaluation Mode Switching**: Automatically adapts evaluation methodology based on the availability of ground truth, performing comparative analysis or intrinsic quality assessment as needed.
- **Content Safety Verification**: Incorporates a robust mechanism to identify and flag unsafe content, with intelligent exception handling to prevent false positives.
- **API Failure Resilience**: Designed to gracefully degrade and handle API errors, ensuring continuous operation and reliable evaluation.
- **Embedded Entropy-based Novelty Detection**: Assesses the intrinsic quality of responses, even without a reference, by analyzing lexical diversity and information density.
- **Config-driven**: Easily customizable through a `config.json` file, allowing users to adjust API settings, evaluation weights, and scoring parameters.
- **Robust Test Case Loader**: Handles test cases efficiently, including those with or without reference answers, and provides warnings for missing references.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/R2K-ChatEval.git
    cd R2K-ChatEval
    ```

2.  **Create a virtual environment** (optional as per your usage):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables**:
    Create a `.env` file in the root directory and add your chatbot API key:
    ```
    API_KEY="your_chatbot_api_key_here"
    ```

## Usage

1.  **Configure `config.json`**:
    Adjust the `api_settings`, `evaluation_weights`, `scoring_parameters`, and `metric_labels` as per your requirements.

2.  **Prepare `test_cases.txt`**:
    Create a file with your test questions and optional reference answers. Each question and its corresponding reference (if any) should be on separate lines.
    Example:
    ```
    What is the capital of France?
    Paris
    Tell me a joke.
    N/A
    ```

3.  **Run the evaluation**:
    ```bash
    python src/chateval.py
    ```
    The script will prompt you to enter the paths for your test cases file and the desired output report file.

## Project Structure

```
R2K-ChatEval/
├── src/
│   └── chateval.py
├── tests/
│   ├── test_cases.txt
│   └── test_cases_2007_output.txt
├── docs/
│   └── R2K_ChatEval-Framework.pptx
├── config.json
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## Author

This framework was developed by **Rama Nagireddi, rkkn126@gmail.com**.

## License

This project is open-source and available under the [MIT License](LICENSE).

## Acknowledgements

Special thanks to the open-source community for providing essential libraries and tools that made this project possible.

