from datetime import datetime, timezone
from bson import ObjectId
from django.db.models import Q  # just to keep imports stable if needed
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django_ratelimit.decorators import ratelimit
from .mongo_models import Shop
from .serializers import ShopSerializer
from .permissions import IsOwner  # still used for explicit object checks
from .utils import bounding_box, haversine_km


def _to_dict(doc: Shop, include_distance=False):
    data = {
        'id': str(doc.id),
        'vendor_id': doc.vendor_id,
        'name': doc.name,
        'owner_name': doc.owner_name,
        'business_type': doc.business_type or '',
        'latitude': float(doc.latitude),
        'longitude': float(doc.longitude),
        'created_at': doc.created_at,
        'updated_at': doc.updated_at,
    }
    if include_distance and hasattr(doc, 'distance_km'):
        data['distance_km'] = doc.distance_km
    return data


class ShopViewSet(viewsets.ViewSet):
    """
    MongoEngine-backed ViewSet.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        vendor_id = request.user.id
        qs = Shop.objects(vendor_id=vendor_id).order_by('-created_at')
        bt = request.query_params.get('business_type')
        if bt:
            qs = qs.filter(business_type__iexact=bt)
        # simple manual pagination compatible with DRF settings
        page_size = int(request.query_params.get('page_size') or 20)
        page = int(request.query_params.get('page') or 1)
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        items = [ _to_dict(doc) for doc in qs[start:end] ]
        return Response({
            'count': total,
            'next': None,  # keep minimal; can compute URLs if needed
            'previous': None,
            'results': items,
        })

    def create(self, request):
        serializer = ShopSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        now = datetime.now(timezone.utc)
        doc = Shop(
            vendor_id=request.user.id,
            name=serializer.validated_data['name'],
            owner_name=serializer.validated_data['owner_name'],
            business_type=serializer.validated_data.get('business_type', ''),
            latitude=serializer.validated_data['latitude'],
            longitude=serializer.validated_data['longitude'],
            created_at=now,
            updated_at=now,
        ).save()
        return Response(_to_dict(doc), status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            doc = Shop.objects.get(id=ObjectId(pk))
        except Exception:
            return Response({'detail': 'Not found'}, status=404)
        if doc.vendor_id != request.user.id:
            return Response({'detail': 'Forbidden'}, status=403)
        return Response(_to_dict(doc))

    def update(self, request, pk=None):
        try:
            doc = Shop.objects.get(id=ObjectId(pk))
        except Exception:
            return Response({'detail': 'Not found'}, status=404)
        if doc.vendor_id != request.user.id:
            return Response({'detail': 'Forbidden'}, status=403)
        serializer = ShopSerializer(data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        for f in ['name', 'owner_name', 'business_type', 'latitude', 'longitude']:
            setattr(doc, f, serializer.validated_data.get(f, getattr(doc, f)))
        doc.updated_at = datetime.now(timezone.utc)
        doc.save()
        return Response(_to_dict(doc))

    def partial_update(self, request, pk=None):
        try:
            doc = Shop.objects.get(id=ObjectId(pk))
        except Exception:
            return Response({'detail': 'Not found'}, status=404)
        if doc.vendor_id != request.user.id:
            return Response({'detail': 'Forbidden'}, status=403)
        serializer = ShopSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        for f, v in serializer.validated_data.items():
            if f in ['name', 'owner_name', 'business_type', 'latitude', 'longitude']:
                setattr(doc, f, v)
        doc.updated_at = datetime.now(timezone.utc)
        doc.save()
        return Response(_to_dict(doc))

    def destroy(self, request, pk=None):
        try:
            doc = Shop.objects.get(id=ObjectId(pk))
        except Exception:
            return Response({'detail': 'Not found'}, status=404)
        if doc.vendor_id != request.user.id:
            return Response({'detail': 'Forbidden'}, status=403)
        doc.delete()
        return Response(status=204)

    @method_decorator(ratelimit(key='ip', rate='30/m', block=True))
    @action(detail=False, methods=['get'], url_path='nearby', permission_classes=[AllowAny])
    def nearby(self, request):
        # read & validate inputs
        try:
            lat = float(request.query_params.get('lat'))
            lng = float(request.query_params.get('lng'))
        except (TypeError, ValueError):
            return Response({'detail': 'lat and lng are required float query params.'}, status=400)

        radius_km = request.query_params.get('radius', 5)
        try:
            radius_km = float(radius_km)
        except ValueError:
            return Response({'detail': 'radius must be a float.'}, status=400)

        # bounding box prefilter
        lat_min, lat_max, lng_min, lng_max = bounding_box(lat, lng, radius_km)
        candidates = Shop.objects(
            latitude__gte=lat_min, latitude__lte=lat_max,
            longitude__gte=lng_min, longitude__lte=lng_max
        )

        results = []
        for doc in candidates:
            d = haversine_km(lat, lng, float(doc.latitude), float(doc.longitude))
            if d <= radius_km:
                doc.distance_km = round(d, 3)
                results.append(doc)
        results.sort(key=lambda s: getattr(s, 'distance_km', 0.0))
        data = [_to_dict(doc, include_distance=True) for doc in results]
        return Response(data, status=200)