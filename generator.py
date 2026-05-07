import os
import requests
import re
import json

def generate_ursina_code(user_prompt):
    # GitHub Secrets වලින් Token එක ලබා ගැනීම
    token = os.getenv("GITHUB_TOKEN")
    
    # GitHub Models API Endpoint (GPT-4o සඳහා)
    endpoint = "https://models.inference.ai.azure.com/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # GPT-4o මොඩලය සඳහා අවශ්‍ය දත්ත
    payload = {
        "messages": [
            {
                "role": "system", 
                "content": (
                    "You are a professional Ursina Engine developer. "
                    "Write ONLY pure Python code to create a 3D anime-style scene. "
                    "Do NOT include 'app = Ursina()' or 'app.run()'. "
                    "Focus on creating high-quality entities, animations, and shaders. "
                    "Output ONLY the code inside triple backticks."
                )
            },
            {"role": "user", "content": f"Create a 3D scene of: {user_prompt}"}
        ],
        "model": "gpt-4o", # මෙන්න මෙතන තමයි මොඩලය සඳහන් කරන්නේ
        "temperature": 0.7,
        "max_tokens": 2048
    }

    print(f"Requesting AI for: {user_prompt}")
    
    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        
        # මෙතනදී අපි API එකේ Response එක හරියටම පරීක්ෂා කරනවා
        if response.status_code != 200:
            print(f"Error from API: {response.status_code}")
            print(f"Response: {response.text}")
            return

        result = response.json()
        
        # 'choices' තිබේදැයි පරීක්ෂා කර කෝඩ් එක වෙන් කර ගැනීම
        if 'choices' in result:
            full_text = result['choices'][0]['message']['content']
            
            # Markdown Code Blocks වලින් කෝඩ් එක පමණක් වෙන් කර ගැනීම
            code_match = re.search(r"```python\n(.*?)\n```", full_text, re.DOTALL)
            if not code_match:
                code_match = re.search(r"```\n(.*?)\n```", full_text, re.DOTALL)
            
            final_code = code_match.group(1) if code_match else full_text
            
            # පද්ධතිය විසින් සාදන ලද බව තහවුරු කිරීමට කමෙන්ට් එකක් එක් කිරීම
            final_code = f"# Created by Hasith - Alpha AI\n{final_code}"
            
            with open("animation_logic.py", "w") as f:
                f.write(final_code)
            print("Successfully generated animation_logic.py")
        else:
            print("Unexpected API Response Format. No 'choices' found.")
            print(json.dumps(result, indent=2))

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Workflow එකෙන් එවන Prompt එක ලබා ගැනීම
    prompt = os.getenv("USER_PROMPT", "A simple 3D anime scene")
    generate_ursina_code(prompt)
