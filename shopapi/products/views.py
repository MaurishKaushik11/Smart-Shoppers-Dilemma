import asyncio
from django.http import JsonResponse, HttpRequest
from django.views.decorators.http import require_GET

from .services.aggregator import aggregate_products


@require_GET
async def search_products(request: HttpRequest):
    query = request.GET.get("q", "").strip()
    if not query:
        return JsonResponse({"error": "Missing required query parameter 'q'"}, status=400)

    try:
        # Run aggregator (async) and return Pydantic model JSON
        result = await aggregate_products(query)
        return JsonResponse(result.model_dump(), status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
