
import subprocess

def ask_ollama(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", "mistral"],
            input=prompt.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60
        )
        output = result.stdout.decode('utf-8')
        return output.split(">>>")[-1].strip()
    except Exception as e:
        return f"⚠️ Error: {e}"

if __name__ == "__main__":
    print("🧠 Local Chatbot (Mistral via Ollama) is live! Type your message below (type 'exit' to quit):")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Chatbot session ended.")
            break
        response = ask_ollama(user_input)
        print("Bot:", response)
