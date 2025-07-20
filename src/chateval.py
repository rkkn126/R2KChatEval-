
"""
=============================================
R2K ChatEval
Author: Rama Nagireddi
=============================================
"""


# Import necessary libraries
import math
import time
import json
import os
import nltk
import requests
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from rouge_score import rouge_scorer
from sentence_transformers import SentenceTransformer, util
from dotenv import load_dotenv

# Download required NLTK data if not already present
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)
load_dotenv()
class ACEF_Evaluator:
    """
    Advanced Chatbot Evaluation Framework (Patent Pending)
    A comprehensive, config-driven framework for evaluating chatbot responses.
    """

    def __init__(self, config_path='config.json'):
        """
        Initializes the evaluator with configuration and necessary models.
        Args:
            config_path (str): Path to the JSON configuration file.
        """
        self._load_config(config_path)
        self.embed_model = SentenceTransformer(self.config['embedding_model'])
        self.stop_words = set(stopwords.words('english'))
        self.rouge_scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
        self.smoothing = nltk.translate.bleu_score.SmoothingFunction().method4
        self.metric_labels = self.config.get('metric_labels', {})

    def _load_config(self, path):
        """Loads configuration from a JSON file with error handling."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            print("Configuration loaded successfully.")
        except FileNotFoundError:
            raise SystemExit(f"FATAL: Configuration file not found at {path}. Please create it.")
        except json.JSONDecodeError:
            raise SystemExit(f"FATAL: Invalid JSON in configuration file {path}.")
        except Exception as e:
            raise SystemExit(f"FATAL: An unexpected error occurred while loading config: {e}")

    def check_content_safety(self, text):
        """Innovation 3: Content safety verification with contextual exception handling."""
        text_lower = text.lower()
        safety_config = self.config['content_safety']
        for word in safety_config['banned_words']:
            if word in text_lower:
                if any(exception in text_lower for exception in safety_config['safe_exceptions']):
                    continue
                return False, f"Content flag: {word}"
        return True, "Content verified"

    def evaluate_with_ground_truth(self, response, ground_truth):
        """Innovation 1: Multi-modal metric fusion engine."""
        res_tokens = word_tokenize(response.lower())
        gt_tokens = word_tokenize(ground_truth.lower())

        bleu = nltk.translate.bleu_score.sentence_bleu([gt_tokens], res_tokens, smoothing_function=self.smoothing)
        rouge = self.rouge_scorer.score(ground_truth, response)

        res_embed = self.embed_model.encode(response, convert_to_tensor=True)
        gt_embed = self.embed_model.encode(ground_truth, convert_to_tensor=True)
        cosine_sim = util.pytorch_cos_sim(res_embed, gt_embed).item()

        metrics = {
            'BLEU': round(bleu, 4),
            'ROUGE-1': round(rouge['rouge1'].fmeasure, 4),
            'ROUGE-2': round(rouge['rouge2'].fmeasure, 4),
            'ROUGE-L': round(rouge['rougeL'].fmeasure, 4),
            'Cosine Similarity': round(cosine_sim, 4),
            'Length Ratio': round(len(res_tokens) / len(gt_tokens), 2) if gt_tokens else 0
        }

        weights = self.config['evaluation_weights']['comparative']
        overall = (
                          weights['bleu'] * bleu +
                          weights['rouge_1'] * rouge['rouge1'].fmeasure +
                          weights['rouge_2'] * rouge['rouge2'].fmeasure +
                          weights['cosine_similarity'] * cosine_sim
                  ) * 100
        return metrics, overall

    def evaluate_without_ground_truth(self, response):
        """Innovation 6: Embedded entropy-based novelty detection."""
        tokens = word_tokenize(response.lower())
        total_tokens = len(tokens)
        if total_tokens == 0:
            return {}, 0.0

        freq = nltk.FreqDist(tokens)
        entropy = -sum((c / total_tokens) * math.log2(c / total_tokens) for c in freq.values())

        ends_with_period = int(response.strip().endswith(('.', '!', '?')))
        relevance_score = min(1.0, entropy / self.config['scoring_parameters']['relevance_entropy_divisor'])

        metrics = {
            'Token Count': total_tokens,
            'Entropy': round(entropy, 2),
            'Ends with Period': ends_with_period,
            'Relevance Score': relevance_score
        }

        weights = self.config['evaluation_weights']['intrinsic']
        max_token_cap = self.config['scoring_parameters']['max_token_penalty_cap']
        overall = (
                          weights['ends_with_period'] * metrics['Ends with Period'] +
                          weights['relevance_score'] * metrics['Relevance Score'] +
                          weights['token_count_factor'] * min(1, total_tokens / max_token_cap)
                  ) * 100
        return metrics, overall

    def evaluate_response(self, response, reference, response_time):
        """Innovation 2: Dynamic evaluation mode switching."""
        result = {'Actual Response': response}
        valid_reference = reference and reference.strip().upper() not in ["", "N/A", "NULL"]

        if valid_reference:
            metrics, overall = self.evaluate_with_ground_truth(response, reference)
            result['Evaluation Mode'] = 'Comparative Analysis'
        else:
            metrics, overall = self.evaluate_without_ground_truth(response)
            result['Evaluation Mode'] = 'Intrinsic Quality Assessment'

        metrics['Response Time'] = round(response_time, 3)
        result.update(metrics)
        result.update(self._calculate_text_metrics(response))

        is_safe, safety_msg = self.check_content_safety(response)
        result['Content Safe'] = is_safe
        result['Safety Message'] = safety_msg

        time_penalty = min(1, response_time / self.config['scoring_parameters']['time_penalty_divisor'])
        result['Overall Score'] = round(overall * (1 - time_penalty), 2)
        return result

    def _calculate_text_metrics(self, text):
        """Computes various structural and lexical properties of the text."""
        words = [w for w in word_tokenize(text) if w.isalpha()]
        sentences = sent_tokenize(text)
        content_words = [w for w in words if w.lower() not in self.stop_words]
        word_count = len(words)
        sentence_count = len(sentences) or 1

        return {
            'Word Count': word_count,
            'Sentence Count': sentence_count,
            'Words/Sentence': round(word_count / sentence_count, 2),
            'Lexical Diversity': round(len(set(words)) / word_count, 3) if word_count else 0,
            'Info Density': round(len(content_words) / word_count * 100, 1) if word_count else 0,
            'Avg Word Length': round(sum(len(w) for w in words) / word_count, 2) if word_count else 0
        }

    def query_chatbot(self, question):
        """Innovation 7: API failure resilience with graceful degradation."""
        api_conf = self.config['api_settings']
        api_key = os.getenv("API_KEY")
        #print(api_key)
        #api_key = os.getenv(api_conf['api_key_env'])

        if not api_key:
            #print(f"Warning: Environment variable API_KEY not set. API calls may fail.")
            error_message = "FATAL: Environment variable 'API_KEY' not found or .env file is missing/incorrect."
            print(error_message)
            #print(api_key)
        payload = {"message": question, "model": api_conf['model_name'], "conversation_history": []}
        start = time.time()

        try:
            response = requests.post(
                api_conf['url'],
                json=payload,
                timeout=api_conf['timeout'],
                headers={"Authorization": f"Bearer {api_key}"}
            )
            response.raise_for_status()
            api_response = response.json().get('response', '')
        except requests.exceptions.RequestException as e:
            api_response = f"API Error: {e}"
            print(f"API Request Error: {e}")
        except json.JSONDecodeError:
            api_response = "System Error: Invalid JSON response from API"
            print("API JSON Decode Error: Invalid response format.")
        except Exception as e:
            api_response = f"System Error: An unexpected error occurred: {e}"
            print(f"Unexpected API Error: {e}")

        return api_response, time.time() - start

    def _load_test_cases(self, file_path):
        """Robust test case loader with comment handling and pairing."""
        test_cases = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]

                # Pair questions and answers
                for i in range(0, len(lines), 2):
                    question = lines[i]
                    # Check if a reference answer exists
                    if i + 1 < len(lines):
                        reference = lines[i + 1]
                        test_cases.append((question, reference))
                    else:
                        test_cases.append((question, "N/A"))
                        print(f"Warning: Last question '{question}' is missing a reference answer.")

            if not test_cases:
                print("Warning: No valid test cases found in the file.")
            return test_cases
        except FileNotFoundError:
            raise IOError(f"Test case file not found: {file_path}")
        except Exception as e:
            raise IOError(f"Test case loading failed: {e}")

    def save_results(self, results, output_path):
        """Saves the formatted evaluation report to a specified output file."""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for res in results:
                    f.write(f"\n[Test Case {res['Test ID']}]\n")
                    f.write(f"Question: {res['Question']}\n")
                    f.write(f"Reference: {res['Reference']}\n")
                    f.write(
                        f"Response: {res['Actual Response'][:200]}{'...' if len(res['Actual Response']) > 200 else ''}\n")
                    f.write(f"Evaluation Mode: {res['Evaluation Mode']}\n")
                    f.write(f"Overall Score: {res['Overall Score']}%\n")
                    f.write(f"Content Safe: {res['Content Safe']} ({res['Safety Message']})\n\nMetrics:\n")

                    for metric, value in res.items():
                        if metric in self.metric_labels:
                            label = self.metric_labels[metric]
                            f.write(f"- {metric}: {value} ({label})\n")
                    f.write("\n" + "=" * 80 + "\n")
            print(f"Results successfully saved to {output_path}")
        except Exception as e:
            print(f"Result saving failed: {e}")

    def run_evaluation(self, input_path, output_path):
        """Executes the full chatbot evaluation pipeline."""
        try:
            test_cases = self._load_test_cases(input_path)
        except IOError as e:
            print(e)
            return []

        results = []
        for idx, (question, reference) in enumerate(test_cases, 1):
            print(f"\n--- Running Test Case {idx} ---")
            print(f"Question: {question}")
            response, response_time = self.query_chatbot(question)
            evaluation = self.evaluate_response(response, reference, response_time)
            evaluation.update({'Test ID': idx, 'Question': question, 'Reference': reference})
            results.append(evaluation)
            print(
                f"Result: Score={evaluation['Overall Score']}% | Time={response_time:.2f}s | Words={evaluation['Word Count']}")

        if results:
            self.save_results(results, output_path)
        return results


if __name__ == "__main__":
    try:
        evaluator = ACEF_Evaluator(config_path='config.json')

        input_file = input("Enter the path to your test cases file: ").strip()
        output_file = input("Enter the path for the output report: ").strip()

        print("\nStarting Advanced Chatbot Evaluation Framework (contact Rama Nagireddi for any additional details)...")
        evaluator.run_evaluation(input_file, output_file)
        print("\nEvaluation completed.")
    except SystemExit as e:
        print(e)