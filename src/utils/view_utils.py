from django.shortcuts import get_object_or_404
from involvement.models import Position


def get_position_by_pk(request, position_id):
    return get_object_or_404(Position, pk=position_id)
