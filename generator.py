import os
import requests
import re

def generate_ursina_code(user_prompt):
    token = os.getenv("GITHUB_TOKEN")
    endpoint = "https://models.inference.ai.azure.com/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    system_message = (
        "You are an expert Ursina Engine developer. Generate Python code for a 3D anime scene. "
        "IMPORTANT: Only define entities, shaders, and animations. "
        "Do not include 'app = Ursina()' or 'app.run()'. "
        "Use 'Entity', 'color', 'Entity.default_shader = lit_with_shadows_shader' for better visuals."
    )
    
    payload = {
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_prompt}
        ],
        "model": "gpt-4o",
        "temperature": 0.7
    }

    response = requests.post(endpoint, headers=headers, json=payload)
    full_response = response.json()['choices'][0]['message']['content']
    
    # Python code එක විතරක් වෙන් කර ගැනීම
    code_match = re.search(r"```python\n(.*?)\n```", full_response, re.DOTALL)
    code = code_match.group(1) if code_match else full_response
    
    with open("animation_logic.py", "w") as f:
        f.write(code)

if __name__ == "__main__":
    prompt = os.getenv("USER_PROMPT", "A simple anime character in a park")
    generate_ursina_code(prompt)
