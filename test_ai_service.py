from services.ai_service import ask_gemini


question = "What is the total revenue?"

answer = ask_gemini(question)

print(answer)