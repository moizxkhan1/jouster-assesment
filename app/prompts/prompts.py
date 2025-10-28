"""
Prompts for generating text analysis results
"""

COMPREHENSIVE_ANALYSIS_PROMPT = """
Analyze the following text and provide a comprehensive analysis.

For the given text, generate:
- title: A descriptive title (max 8 words). If there's an existing title, use it. Otherwise, generate a brief title.
- summary: A concise 1-2 sentence summary focusing on the main points and key information.
- sentiment: The overall sentiment of the text. Must be exactly one of: "positive", "negative", or "neutral".
- topics: An array of exactly 3 key topics or themes from the text. Each topic should be 1-3 words.

Text: {text}
"""
