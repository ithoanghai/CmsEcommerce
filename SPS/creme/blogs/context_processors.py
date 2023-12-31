from .conf import settings


def scoped(request):
    return {
        "scoper_lookup": request.resolver_match.kwargs.get(settings.BLOG_SCOPING_URL_VAR)
        if request.resolver_match else ""
    }
