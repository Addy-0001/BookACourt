from django.core.management.base import BaseCommand
from django.utils import timezone
from user_management.models import User, UserRole, PlayerStats, UserPreference
from faker import Faker
import random

fake = Faker()


class Command(BaseCommand):
    help = 'Seeds the database with sample users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=50,
            help='Number of users to create'
        )

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        self.stdout.write('Seeding users...')

        # Create a super user
        if not User.objects.filter(role=UserRole.SUPER_USER).exists():
            super_user = User.objects.create_superuser(
                phone_number='+9779801234567',
                password='admin123',
                full_name='Admin User',
                email='admin@bookacourt.com',
                city='Kathmandu'
            )
            self.stdout.write(self.style.SUCCESS(f'Created super user: {super_user.phone_number}'))

        # Create court owners
        owner_count = max(5, count // 10)
        for i in range(owner_count):
            phone = f'+977{fake.numerify("##########")}'
            
            # Skip if phone already exists
            if User.objects.filter(phone_number=phone).exists():
                continue
                
            user = User.objects.create_user(
                phone_number=phone,
                password='password123',
                full_name=fake.name(),
                email=fake.email(),
                role=UserRole.COURT_OWNER,
                is_phone_verified=True,
                city=random.choice(['Kathmandu', 'Pokhara', 'Lalitpur', 'Bhaktapur', 'Biratnagar']),
                address=fake.address(),
                date_of_birth=fake.date_of_birth(minimum_age=25, maximum_age=60),
            )
            self.stdout.write(f'Created court owner: {user.phone_number}')

        # Create court managers
        manager_count = max(8, count // 8)
        for i in range(manager_count):
            phone = f'+977{fake.numerify("##########")}'
            
            if User.objects.filter(phone_number=phone).exists():
                continue
                
            user = User.objects.create_user(
                phone_number=phone,
                password='password123',
                full_name=fake.name(),
                email=fake.email(),
                role=UserRole.COURT_MANAGER,
                is_phone_verified=True,
                city=random.choice(['Kathmandu', 'Pokhara', 'Lalitpur', 'Bhaktapur', 'Biratnagar']),
                address=fake.address(),
                date_of_birth=fake.date_of_birth(minimum_age=22, maximum_age=50),
            )
            self.stdout.write(f'Created court manager: {user.phone_number}')

        # Create players
        player_count = count - owner_count - manager_count
        for i in range(player_count):
            phone = f'+977{fake.numerify("##########")}'
            
            if User.objects.filter(phone_number=phone).exists():
                continue
                
            user = User.objects.create_user(
                phone_number=phone,
                password='password123',
                full_name=fake.name(),
                email=fake.email(),
                role=UserRole.PLAYER,
                is_phone_verified=random.choice([True, True, True, False]),  # 75% verified
                city=random.choice(['Kathmandu', 'Pokhara', 'Lalitpur', 'Bhaktapur', 'Biratnagar']),
                address=fake.address(),
                date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=50),
                loyalty_points=random.randint(0, 500)
            )

            # Create player stats
            PlayerStats.objects.create(
                player=user,
                total_bookings=random.randint(0, 50),
                total_matches_played=random.randint(0, 30),
                matches_won=random.randint(0, 20),
                matches_lost=random.randint(0, 15),
                sportsmanship_rating=round(random.uniform(3.0, 5.0), 2),
                total_ratings_received=random.randint(0, 25),
                no_show_count=random.randint(0, 3)
            )

            # Create user preferences
            UserPreference.objects.create(
                user=user,
                email_notifications=random.choice([True, False]),
                sms_notifications=random.choice([True, False]),
                push_notifications=random.choice([True, True, False]),  # More likely to be enabled
                preferred_sports=random.choice([
                    'Basketball,Football',
                    'Tennis,Badminton',
                    'Football',
                    'Basketball',
                    'Volleyball,Badminton'
                ]),
                preferred_time_slots=random.choice([
                    'morning',
                    'evening',
                    'morning,evening',
                    'afternoon'
                ])
            )

            self.stdout.write(f'Created player: {user.phone_number}')

        total_users = User.objects.count()
        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully created users. Total users: {total_users}'))