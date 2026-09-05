from app.services.llm_service import generate_answer


context = """
Supervised learning is a machine learning
technique where a model learns from labeled
training data.

For example, a model can learn to classify
emails as spam or not spam using labeled
examples.
"""


question = "What is supervised learning?"


answer = generate_answer(
    question,
    context
)


print("\n==============================")
print("AI ANSWER")
print("==============================\n")

print(answer)