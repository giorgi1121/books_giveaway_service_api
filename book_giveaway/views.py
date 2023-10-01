from drf_spectacular.utils import extend_schema
from drf_spectacular import generate_schema

@extend_schema(public=True)
def get_schema(request):
    return generate_schema(request)
