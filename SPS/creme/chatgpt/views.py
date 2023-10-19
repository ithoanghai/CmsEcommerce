from django.shortcuts import render
from django.conf import settings
import openai

# Lấy API key từ settings.py
api_key = settings.OPENAI.get('CHAT_API_KEY')

# Khởi tạo API client
openai.api_key = api_key

def chat_with_gpt(request):
    generated_script = None

    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        if user_input:
            # Sử dụng GPT-3 để tạo kịch bản dựa trên user_input
            response = openai.Completion.create(
                engine="davinci",
                prompt=user_input,
                max_tokens=150
            )
            generated_script = response.choices[0].text

    return render(request, 'pinax/chatgpt/chat_form.html', {'generated_script': generated_script})
