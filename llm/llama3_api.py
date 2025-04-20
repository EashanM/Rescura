from groq import Groq

client = Groq(api_key="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")

def ask_llama3(user_prompt, system_prompt="You are a first aid assistant.", max_tokens=512, temperature=0.2):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=max_tokens,
        temperature=temperature
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    user_prompt = "What are the symptoms of a heart attack?"
    response = ask_llama3(user_prompt)
    print("Response:", response)
# This code uses the Groq API to interact with the Llama 3 model.
# Make sure to replace  "YOUR_GROQ_API_KEY" with your actual API key.