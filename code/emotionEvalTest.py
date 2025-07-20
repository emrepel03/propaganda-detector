from evaluators.emotionEval import EmotionEval


# Instantiate EmotionEval class
evaluator = EmotionEval()

# Test Text
with open("evaluators/TestArticle.txt", "r") as file:
    test_text = file.read()

# Call evaluate method
result = evaluator.evaluate("evaluators/TestArticle.txt")
print(result)
