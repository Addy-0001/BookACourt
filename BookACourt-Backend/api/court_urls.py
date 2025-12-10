from django.urls import path, include
from rest_framework_nested import routers
from .court_views import (
    CourtCategoryViewSet,
    CourtRegistrationViewSet,
    CourtViewSet,
    CourtReviewViewSet,
    CourtBlockedSlotViewSet,
    DynamicPricingViewSet,
    EquipmentItemViewSet
)

# Create main router
router = routers.DefaultRouter()
router.register(r'categories', CourtCategoryViewSet, basename='court-category')
router.register(r'registrations', CourtRegistrationViewSet,
                basename='court-registration')
router.register(r'courts', CourtViewSet, basename='court')

# Create nested routers for court-specific resources
courts_router = routers.NestedDefaultRouter(router, r'courts', lookup='court')
courts_router.register(r'reviews', CourtReviewViewSet,
                       basename='court-reviews')
courts_router.register(
    r'blocked-slots', CourtBlockedSlotViewSet, basename='court-blocked-slots')
courts_router.register(r'pricing', DynamicPricingViewSet,
                       basename='court-pricing')
courts_router.register(r'equipment', EquipmentItemViewSet,
                       basename='court-equipment')

# URL patterns
urlpatterns = [
    path('', include(router.urls)),
    path('', include(courts_router.urls)),
]
