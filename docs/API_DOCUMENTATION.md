# R2K ChatEval Framework - API Documentation

## Overview

The R2K ChatEval Framework provides a comprehensive API for evaluating chatbot responses through the `ACEF_Evaluator` class. This document outlines all available methods and their usage.

## Class: ACEF_Evaluator

### Constructor

```python
ACEF_Evaluator(config_path='config.json')
```

**Parameters:**
- `config_path` (str): Path to the JSON configuration file

**Example:**
```python
from chateval import ACEF_Evaluator
evaluator = ACEF_Evaluator('config.json')
```

### Methods

#### evaluate_response(response, reference, response_time)

Evaluates a chatbot response using either comparative analysis (with ground truth) or intrinsic quality assessment (without ground truth).

**Parameters:**
- `response` (str): The chatbot's response to evaluate
- `reference` (str): Ground truth reference (use "N/A" if not available)
- `response_time` (float): Time taken to generate the response in seconds

**Returns:**
- `dict`: Comprehensive evaluation results including metrics and overall score

**Example:**
```python
result = evaluator.evaluate_response(
    response="The capital of France is Paris.",
    reference="Paris",
    response_time=0.5
)
print(f"Overall Score: {result['Overall Score']}%")
```

#### evaluate_with_ground_truth(response, ground_truth)

Performs comparative analysis when ground truth is available.

**Parameters:**
- `response` (str): The chatbot's response
- `ground_truth` (str): The reference answer

**Returns:**
- `tuple`: (metrics_dict, overall_score)

#### evaluate_without_ground_truth(response)

Performs intrinsic quality assessment without requiring ground truth.

**Parameters:**
- `response` (str): The chatbot's response

**Returns:**
- `tuple`: (metrics_dict, overall_score)

#### check_content_safety(text)

Verifies content safety with contextual exception handling.

**Parameters:**
- `text` (str): Text to check for safety

**Returns:**
- `tuple`: (is_safe_bool, safety_message_str)

**Example:**
```python
is_safe, message = evaluator.check_content_safety("This is a safe message")
print(f"Safe: {is_safe}, Message: {message}")
```

#### query_chatbot(question)

Queries the configured chatbot API with error resilience.

**Parameters:**
- `question` (str): Question to send to the chatbot

**Returns:**
- `tuple`: (response_str, response_time_float)

#### run_evaluation(input_path, output_path)

Executes the complete evaluation pipeline on a test case file.

**Parameters:**
- `input_path` (str): Path to test cases file
- `output_path` (str): Path for output report

**Returns:**
- `list`: List of evaluation results

**Example:**
```python
results = evaluator.run_evaluation('test_cases.txt', 'results.txt')
```

#### save_results(results, output_path)

Saves formatted evaluation results to a file.

**Parameters:**
- `results` (list): List of evaluation result dictionaries
- `output_path` (str): Path to save the formatted report

## Configuration

The framework uses a JSON configuration file with the following structure:

```json
{
  "api_settings": {
    "url": "your_chatbot_api_url",
    "model_name": "your_model_name",
    "timeout": 60
  },
  "embedding_model": "all-MiniLM-L6-v2",
  "content_safety": {
    "banned_words": ["hate", "violence", "inappropriate_word"],
    "safe_exceptions": ["anti-violence", "non-violent"]
  },
  "evaluation_weights": {
    "comparative": {
      "bleu": 0.20,
      "rouge_1": 0.15,
      "rouge_2": 0.15,
      "cosine_similarity": 0.50
    },
    "intrinsic": {
      "ends_with_period": 0.3,
      "relevance_score": 0.4,
      "token_count_factor": 0.3
    }
  },
  "scoring_parameters": {
    "time_penalty_divisor": 10,
    "relevance_entropy_divisor": 5,
    "max_token_penalty_cap": 100
  }
}
```

## Error Handling

The framework includes robust error handling for:

- Missing configuration files
- Invalid JSON configuration
- API connection failures
- Missing environment variables
- Invalid test case formats

All errors are logged with descriptive messages to aid in debugging.

## Metrics Explained

### Comparative Analysis Metrics (with ground truth):
- **BLEU**: Measures precision of n-gram matches
- **ROUGE-1/2/L**: Measures recall of unigrams, bigrams, and longest common subsequence
- **Cosine Similarity**: Measures semantic similarity using embeddings
- **Length Ratio**: Compares response length to reference

### Intrinsic Quality Metrics (without ground truth):
- **Token Count**: Number of tokens in the response
- **Entropy**: Lexical diversity measure
- **Ends with Period**: Proper sentence completion
- **Relevance Score**: Derived from entropy analysis

### Universal Metrics:
- **Response Time**: Time taken to generate response
- **Word Count**: Number of words
- **Sentence Count**: Number of sentences
- **Lexical Diversity**: Unique words / total words
- **Info Density**: Content words percentage
- **Average Word Length**: Character count per word

## Best Practices

1. **Configuration**: Always validate your config.json before running evaluations
2. **Environment Variables**: Set up your .env file with proper API credentials
3. **Test Cases**: Format test cases with questions and references on separate lines
4. **Batch Processing**: Use `run_evaluation()` for processing multiple test cases
5. **Error Monitoring**: Check logs for API failures and configuration issues

## Support

For additional support or questions about the R2K ChatEval Framework, please contact Rama Nagireddi or refer to the project documentation.

