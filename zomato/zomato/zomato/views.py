from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from zomato.server.main import RestaurantRAG

# Load model once globally
chatbot = RestaurantRAG(data_dir=r"C:\Users\ASUS\Desktop\zomato_assignment\zomato\zomato\data")

@csrf_exempt
def chatbot_view(request):
    if request.method == "POST":
        user_query = request.POST.get("query", "")
        if user_query:
            answer = chatbot.answer_query(user_query)
            return JsonResponse({"response": answer})
    return render(request, "chatbot/chat.html")
