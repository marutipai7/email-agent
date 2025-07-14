from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Conversation, ChatSession
from .ollama_chat import scrape_duckduckgo
from .ollama_instance import get_cached_ollama_model
import time
import logging
import ollama
logger = logging.getLogger(__name__)

# Show chat interface and previous sessions
@login_required
def chat_view(request):
    sessions = ChatSession.objects.filter(user=request.user).order_by('-created_at')
    session_id = request.GET.get('session')

    # Get active session
    if session_id:
        try:
            active_session = ChatSession.objects.get(id=session_id, user=request.user)
        except ChatSession.DoesNotExist:
            return redirect('new_chat')
    else:
        active_session = sessions.first()

    chat_history = (
        Conversation.objects.filter(session=active_session)
        .order_by('timestamp') if active_session else []
    )

    return render(request, 'chat.html', {
        'chat_history': chat_history,
        'sessions': sessions,
        'active_session': active_session
    })

# Create a new session
@login_required
def new_chat_view(request):
    session = ChatSession.objects.create(user=request.user)
    return redirect(f"{reverse('chat')}?session={session.id}")

# Handle AJAX + Streaming response
@csrf_exempt
@login_required
def stream_chat_response(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid method'}, status=405)

    session_id = request.GET.get('session_id')
    query = request.GET.get('query')

    if not session_id or not query:
        return JsonResponse({'error': 'Missing session_id or query'}, status=400)

    try:
        session = ChatSession.objects.get(id=session_id, user=request.user)
    except ChatSession.DoesNotExist:
        return JsonResponse({'error': 'Invalid session'}, status=404)

    # Scrape + Construct final prompt
    context_info = scrape_duckduckgo(query)
    final_input = f"{query}\n\nContext:\n{context_info}"

    model = get_cached_ollama_model()
    start_time = time.time()

    def event_stream():
        full_response = ""
        try:
            # Use Ollama's native streaming
            for chunk in ollama.chat(
                model="deepseek-r1:1.5b",
                messages=[{"role": "user", "content": final_input}],
                stream=True
            ):
                text = chunk.get("message", {}).get("content", "")
                full_response += text
                yield f"data: {text}\n\n"

        except Exception as e:
            logger.exception("Error while streaming Ollama response")
            yield f"data: [Error receiving response]\n\n"

        elapsed_time = round(time.time() - start_time, 2)

        # Save conversation at end
        Conversation.objects.create(
            user=request.user,
            session=session,
            query=query,
            response=full_response
        )
        yield f"data:__END__|{elapsed_time}\n\n"

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')
