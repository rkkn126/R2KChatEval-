#!/usr/bin/env python3
"""
Example usage of the R2K ChatEval Framework
Author: Rama Nagireddi
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chateval import ACEF_Evaluator

def main():
    """
    Example demonstrating how to use the R2K ChatEval Framework
    """
    print("R2K ChatEval Framework - Example Usage")
    print("=" * 50)
    
    # Initialize the evaluator
    try:
        evaluator = ACEF_Evaluator(config_path='../config.json')
        print("✓ Evaluator initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize evaluator: {e}")
        return
    
    # Example 1: Evaluate a single response with ground truth
    print("\n1. Evaluating response with ground truth:")
    response = "The capital of France is Paris."
    ground_truth = "Paris"
    response_time = 0.5
    
    result = evaluator.evaluate_response(response, ground_truth, response_time)
    print(f"   Response: {response}")
    print(f"   Ground Truth: {ground_truth}")
    print(f"   Overall Score: {result['Overall Score']}%")
    print(f"   Evaluation Mode: {result['Evaluation Mode']}")
    
    # Example 2: Evaluate a response without ground truth
    print("\n2. Evaluating response without ground truth:")
    response = "Why did the scarecrow win an award? Because he was outstanding in his field!"
    response_time = 0.3
    
    result = evaluator.evaluate_response(response, "N/A", response_time)
    print(f"   Response: {response}")
    print(f"   Overall Score: {result['Overall Score']}%")
    print(f"   Evaluation Mode: {result['Evaluation Mode']}")
    
    # Example 3: Content safety check
    print("\n3. Content safety verification:")
    unsafe_response = "I hate this stupid system"
    safe_response = "I disagree with this approach"
    
    is_safe1, msg1 = evaluator.check_content_safety(unsafe_response)
    is_safe2, msg2 = evaluator.check_content_safety(safe_response)
    
    print(f"   Unsafe response: '{unsafe_response}' -> Safe: {is_safe1} ({msg1})")
    print(f"   Safe response: '{safe_response}' -> Safe: {is_safe2} ({msg2})")
    
    print("\n" + "=" * 50)
    print("Example completed successfully!")

if __name__ == "__main__":
    main()

