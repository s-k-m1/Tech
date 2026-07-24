from django.http import JsonResponse
from django.db import connections
from django.core.cache import cache
from django.conf import settings
import redis


def health_check(request):
    return JsonResponse({
        "status": "healthy",
        "service": "sk-tech-api",
        "version": "1.0.0",
    }, status=200)


def readiness_check(request):
    db_ok = False
    redis_ok = False
    celery_ok = False

    try:
        connections["default"].cursor().execute("SELECT 1")
        db_ok = True
    except Exception:
        pass

    try:
        r = redis.from_url(settings.REDIS_URL.split(",")[0] if isinstance(settings.REDIS_URL, str) else settings.REDIS_URL)
        r.ping()
        redis_ok = True
    except Exception:
        pass

    try:
        from celery.app.control import Inspect
        from config.celery import app
        i = Inspect(app=app)
        stats = i.stats()
        celery_ok = stats is not None and len(stats) > 0
    except Exception:
        pass

    all_ok = db_ok and redis_ok and celery_ok

    return JsonResponse({
        "status": "ready" if all_ok else "degraded",
        "checks": {
            "database": "ok" if db_ok else "fail",
            "redis": "ok" if redis_ok else "fail",
            "celery": "ok" if celery_ok else "fail",
        },
    }, status=200 if all_ok else 503)
