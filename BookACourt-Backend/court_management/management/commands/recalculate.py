from django.core.management.base import BaseCommand
from django.db.models import Avg, Count
from court_management.models import Court, CourtReview


class Command(BaseCommand):
    help = 'Recalculate all court ratings and review counts'

    def handle(self, *args, **kwargs):
        courts = Court.objects.all()
        updated_count = 0

        for court in courts:
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
            updated_count += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f'Updated {court.name}: {court.average_rating} stars ({court.total_reviews} reviews)'
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully updated {updated_count} court(s)'
            )
        )
