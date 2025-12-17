from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg, Count
from .models import CourtReview


@receiver(post_save, sender=CourtReview)
def update_court_rating_on_save(sender, instance, created, **kwargs):
    """
    Automatically update court rating when a review is created or updated
    """
    court = instance.court

    # Only recalculate if the review is visible
    if instance.is_visible:
        reviews = CourtReview.objects.filter(
            court=court,
            is_visible=True
        )

        # Calculate average rating
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        court.average_rating = round(avg_rating, 2) if avg_rating else 0.00

        # Update total reviews count
        court.total_reviews = reviews.count()

        court.save(update_fields=['average_rating', 'total_reviews'])


@receiver(post_delete, sender=CourtReview)
def update_court_rating_on_delete(sender, instance, **kwargs):
    """
    Automatically update court rating when a review is deleted
    """
    court = instance.court

    reviews = CourtReview.objects.filter(
        court=court,
        is_visible=True
    )

    # Calculate average rating
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    court.average_rating = round(avg_rating, 2) if avg_rating else 0.00

    # Update total reviews count
    court.total_reviews = reviews.count()

    court.save(update_fields=['average_rating', 'total_reviews'])
