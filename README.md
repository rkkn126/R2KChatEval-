# R2K ChatEval Framework

## Overview

R2K ChatEval is an advanced, Python-based framework engineered for the comprehensive evaluation of chatbot responses. As a local, zero-cost evaluation framework, it is built to be fast, flexible, and transparent. It operates without dependencies on external LLMs, API calls, or cloud services, allowing users to simply plug in their chatbot API, customize the configuration, and run the evaluation.
The framework introduces a suite of innovative features, including multi-modal metric fusion, dynamic evaluation mode switching, content safety verification with contextual exception handling, and API failure resilience through graceful degradation. A key strength of the framework is its ability to operate effectively without ground truth data, establishing it as a versatile tool for AI developers focused on model selection and refinement.
The framework is designed for high adaptability. Users, including AI researchers,product owners AI QE, can reference its approach and customize the code and configurations to meet specific business requirements. For instance, the weights of evaluation metrics can be adjusted to align with business priorities when assessing model performance. This flexibility positions R2K ChatEval as a powerful tool for AI Quality Engineering, ensuring that chatbot solutions meet both technical standards and strategic business objectives.

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


2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up environment variables**:
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

