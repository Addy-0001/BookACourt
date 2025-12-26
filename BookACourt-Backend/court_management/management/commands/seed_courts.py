from django.core.management.base import BaseCommand
from django.utils import timezone
from court_management.models import (
    CourtCategory, Court, CourtImage, DynamicPricing,
    CourtBlockedSlot, CourtReview, EquipmentItem
)
from user_management.models import User, UserRole
from faker import Faker
import random
from datetime import time, timedelta

fake = Faker()


class Command(BaseCommand):
    help = 'Seeds the database with sample courts and related data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=20,
            help='Number of courts to create'
        )

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        self.stdout.write('Seeding courts...')

        # Create categories
        categories_data = [
            {'name': 'Basketball', 'description': 'Basketball courts for competitive and casual play'},
            {'name': 'Tennis', 'description': 'Professional and recreational tennis courts'},
            {'name': 'Badminton', 'description': 'Indoor badminton courts'},
            {'name': 'Football', 'description': 'Football fields for matches and training'},
            {'name': 'Volleyball', 'description': 'Indoor and outdoor volleyball courts'},
            {'name': 'Futsal', 'description': 'Indoor futsal courts'},
        ]

        categories = []
        for cat_data in categories_data:
            category, created = CourtCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description'], 'is_active': True}
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Get court owners
        owners = list(User.objects.filter(role=UserRole.COURT_OWNER))
        if not owners:
            self.stdout.write(self.style.ERROR('No court owners found. Please run seed_users first.'))
            return

        managers = list(User.objects.filter(role=UserRole.COURT_MANAGER))
        players = list(User.objects.filter(role=UserRole.PLAYER))

        # Create courts
        court_types = ['Basketball', 'Tennis', 'Badminton', 'Football', 'Volleyball', 'Futsal']
        cities = ['Kathmandu', 'Pokhara', 'Lalitpur', 'Bhaktapur', 'Biratnagar']
        amenities_list = [
            'Parking,Locker Rooms,Water Fountain,Seating Area',
            'Parking,Changing Rooms,Shower,Cafeteria',
            'Locker Rooms,Water Fountain,First Aid,Lighting',
            'Parking,Seating,Water,Restrooms,Equipment Rental',
            'Parking,Locker Rooms,Cafeteria,Wi-Fi,Air Conditioning'
        ]

        for i in range(count):
            owner = random.choice(owners)
            category = random.choice(categories)
            city = random.choice(cities)
            court_type = category.name

            court = Court.objects.create(
                name=f"{fake.company()} {court_type} Court",
                owner=owner,
                category=category,
                address=fake.address(),
                city=city,
                latitude=fake.latitude(),
                longitude=fake.longitude(),
                description=fake.paragraph(nb_sentences=3),
                court_type=court_type,
                is_indoor=random.choice([True, False]),
                capacity=random.randint(10, 50),
                amenities=random.choice(amenities_list),
                base_hourly_rate=random.randint(500, 3000),
                opening_time=time(6, 0),
                closing_time=time(22, 0),
                is_active=True,
                is_verified=random.choice([True, True, True, False]),  # 75% verified
                phone_number=f'+977{fake.numerify("##########")}',
                email=fake.email()
            )

            # Add managers (1-3 managers per court)
            if managers:
                court_managers = random.sample(managers, min(random.randint(1, 3), len(managers)))
                court.managers.set(court_managers)

            self.stdout.write(f'Created court: {court.name}')

            # Create dynamic pricing for some courts (60% chance)
            if random.random() < 0.6:
                # Peak hours pricing (morning)
                DynamicPricing.objects.create(
                    court=court,
                    start_time=time(6, 0),
                    end_time=time(9, 0),
                    days_of_week='0,1,2,3,4',  # Weekdays
                    hourly_rate=court.base_hourly_rate * 1.2,
                    description='Morning Peak Hours',
                    is_active=True
                )

                # Peak hours pricing (evening)
                DynamicPricing.objects.create(
                    court=court,
                    start_time=time(17, 0),
                    end_time=time(21, 0),
                    days_of_week='0,1,2,3,4',  # Weekdays
                    hourly_rate=court.base_hourly_rate * 1.5,
                    description='Evening Peak Hours',
                    is_active=True
                )

                # Weekend pricing
                DynamicPricing.objects.create(
                    court=court,
                    start_time=time(8, 0),
                    end_time=time(20, 0),
                    days_of_week='5,6',  # Weekend
                    hourly_rate=court.base_hourly_rate * 1.3,
                    description='Weekend Rate',
                    is_active=True
                )

            # Add equipment items
            equipment_by_type = {
                'Basketball': ['Basketball', 'Jersey Set', 'Score Board'],
                'Tennis': ['Tennis Racket', 'Tennis Balls Set', 'Ball Machine'],
                'Badminton': ['Badminton Racket', 'Shuttlecocks Set', 'Net'],
                'Football': ['Football', 'Cones Set', 'Goal Net'],
                'Volleyball': ['Volleyball', 'Net', 'Knee Pads'],
                'Futsal': ['Futsal Ball', 'Jersey Set', 'Goal Net']
            }

            equipment_items = equipment_by_type.get(court_type, ['Equipment'])
            for item_name in equipment_items:
                EquipmentItem.objects.create(
                    court=court,
                    name=item_name,
                    description=f'{item_name} available for rent',
                    quantity_total=random.randint(5, 20),
                    quantity_available=random.randint(3, 15),
                    rental_rate=random.randint(50, 500),
                    damage_penalty=random.randint(500, 2000),
                    is_active=True
                )

            # Add blocked slots for some courts (30% chance)
            if random.random() < 0.3:
                for j in range(random.randint(1, 3)):
                    blocked_date = timezone.now().date() + timedelta(days=random.randint(1, 30))
                    CourtBlockedSlot.objects.create(
                        court=court,
                        blocked_date=blocked_date,
                        start_time=time(random.randint(9, 14), 0),
                        end_time=time(random.randint(15, 18), 0),
                        reason=random.choice([
                            'Maintenance',
                            'Private Event',
                            'Tournament',
                            'Cleaning'
                        ]),
                        notes=fake.sentence(),
                        blocked_by=owner
                    )

            # Add reviews from players
            if players:
                num_reviews = random.randint(3, 15)
                reviewers = random.sample(players, min(num_reviews, len(players)))
                
                for player in reviewers:
                    # Check if review already exists
                    if not CourtReview.objects.filter(court=court, player=player).exists():
                        review = CourtReview.objects.create(
                            court=court,
                            player=player,
                            rating=random.randint(3, 5),
                            review_text=fake.paragraph(nb_sentences=2),
                            is_visible=True,
                            is_flagged=False
                        )

                        # 40% chance owner responds
                        if random.random() < 0.4:
                            review.owner_response = fake.paragraph(nb_sentences=1)
                            review.responded_at = timezone.now()
                            review.save()

        total_courts = Court.objects.count()
        total_equipment = EquipmentItem.objects.count()
        total_reviews = CourtReview.objects.count()

        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully created:'))
        self.stdout.write(self.style.SUCCESS(f'  - {len(categories)} categories'))
        self.stdout.write(self.style.SUCCESS(f'  - {total_courts} courts'))
        self.stdout.write(self.style.SUCCESS(f'  - {total_equipment} equipment items'))
        self.stdout.write(self.style.SUCCESS(f'  - {total_reviews} reviews'))