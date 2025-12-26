from django.core.management.base import BaseCommand
from django.utils import timezone
from booking_management.models import (
    Booking, CancellationPolicy, BookingNotification,
    EquipmentRental, MatchEvent, MatchParticipant,
    PlayerRating, BookingShare, RecurringBooking
)
from court_management.models import Court, EquipmentItem
from user_management.models import User, UserRole
from faker import Faker
import random
from datetime import datetime, time, timedelta
from decimal import Decimal

fake = Faker()


class Command(BaseCommand):
    help = 'Seeds the database with sample bookings and related data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=100,
            help='Number of bookings to create'
        )

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        self.stdout.write('Seeding bookings...')

        # Get necessary data
        courts = list(Court.objects.filter(is_active=True))
        players = list(User.objects.filter(role=UserRole.PLAYER))

        if not courts:
            self.stdout.write(self.style.ERROR(
                'No courts found. Please run seed_courts first.'))
            return

        if not players:
            self.stdout.write(self.style.ERROR(
                'No players found. Please run seed_users first.'))
            return

        # Create cancellation policies for courts that don't have one
        for court in courts:
            if not hasattr(court, 'cancellation_policy'):
                CancellationPolicy.objects.create(
                    court=court,
                    cancellation_deadline_hours=24,
                    full_refund_hours=48,
                    partial_refund_hours=24,
                    partial_refund_percentage=50,
                    no_show_penalty_percentage=100,
                    policy_text=f"Cancellation policy for {court.name}: Full refund if cancelled 48 hours before, 50% refund if cancelled 24 hours before."
                )

        # Create bookings
        statuses = ['CONFIRMED', 'CONFIRMED', 'CONFIRMED',
                    'COMPLETED', 'PENDING', 'CANCELLED']
        payment_methods = ['ONLINE', 'ONLINE', 'CASH', 'OFFLINE']
        payment_statuses = ['COMPLETED', 'COMPLETED', 'PENDING', 'REFUNDED']

        created_bookings = []
        for i in range(count):
            court = random.choice(courts)
            player = random.choice(players)

            # Random date (past 30 days to future 60 days)
            days_offset = random.randint(-30, 60)
            booking_date = timezone.now().date() + timedelta(days=days_offset)

            # Random time slot
            start_hour = random.randint(6, 20)
            start_time = time(start_hour, 0)
            end_time = time(start_hour + random.randint(1, 3), 0)

            # Check if slot is available
            existing = Booking.objects.filter(
                court=court,
                booking_date=booking_date,
                start_time=start_time
            ).exists()

            if existing:
                continue

            # Calculate pricing
            duration_seconds = (datetime.combine(booking_date, end_time) -
                                datetime.combine(booking_date, start_time)).seconds
            duration_hours = Decimal(str(duration_seconds / 3600))
            base_amount = court.base_hourly_rate * duration_hours

            loyalty_points_used = random.randint(
                0, min(50, player.loyalty_points))
            discount_amount = Decimal(str(loyalty_points_used * 0.1))
            total_amount = base_amount - discount_amount

            status = random.choice(statuses)
            payment_status = random.choice(payment_statuses)

            # Adjust status for past dates
            if booking_date < timezone.now().date():
                status = random.choice(
                    ['COMPLETED', 'COMPLETED', 'CANCELLED', 'NO_SHOW'])
                payment_status = 'COMPLETED' if status == 'COMPLETED' else random.choice(
                    ['COMPLETED', 'REFUNDED'])

            booking = Booking.objects.create(
                court=court,
                player=player,
                booking_date=booking_date,
                start_time=start_time,
                end_time=end_time,
                status=status,
                payment_method=random.choice(payment_methods),
                payment_status=payment_status,
                base_amount=base_amount,
                discount_amount=discount_amount,
                loyalty_points_used=loyalty_points_used,
                total_amount=total_amount,
                notes=fake.sentence() if random.random() < 0.3 else '',
                special_requests=fake.sentence() if random.random() < 0.2 else '',
                is_walk_in=random.choice(
                    [True, False]) if random.random() < 0.1 else False,
                created_by=player
            )

            if booking.is_walk_in:
                booking.walk_in_guest_name = fake.name()
                booking.save()

            # Handle cancelled bookings
            if status == 'CANCELLED':
                booking.cancelled_at = timezone.now() - timedelta(days=random.randint(1, 10))
                booking.cancellation_reason = random.choice([
                    'Schedule conflict',
                    'Weather conditions',
                    'Personal emergency',
                    'Found alternative venue'
                ])
                booking.refund_amount = total_amount * Decimal('0.9')
                booking.save()

            created_bookings.append(booking)

            # Create notifications (80% chance)
            if random.random() < 0.8:
                BookingNotification.objects.create(
                    booking=booking,
                    user=player,
                    notification_type=random.choice(
                        ['CONFIRMATION', 'REMINDER', 'MODIFICATION']),
                    message=f"Your booking for {court.name} on {booking_date} has been confirmed.",
                    is_read=random.choice([True, False]),
                    sent_via_email=random.choice([True, False]),
                    sent_via_sms=random.choice([True, False]),
                    sent_via_push=random.choice([True, False])
                )

            # Add equipment rentals (30% chance)
            if random.random() < 0.3:
                equipment_items = list(court.equipment.filter(is_active=True))
                if equipment_items:
                    num_items = random.randint(1, min(3, len(equipment_items)))
                    for equipment in random.sample(equipment_items, num_items):
                        EquipmentRental.objects.create(
                            booking=booking,
                            equipment=equipment,
                            quantity=random.randint(1, 3),
                            rental_cost=equipment.rental_rate,
                            status=random.choice(
                                ['ACTIVE', 'RETURNED', 'RETURNED']),
                            returned_at=timezone.now() if random.random() < 0.7 else None
                        )

            self.stdout.write(f'Created booking: {booking.booking_reference}')

        # Create match events
        self.stdout.write('\nCreating match events...')
        num_matches = min(count // 5, len(created_bookings))

        # Filter bookings that don't have match events yet
        available_bookings = [
            b for b in created_bookings
            if not hasattr(b, 'match_event') and
            b.booking_date >= timezone.now().date() - timedelta(days=7)
        ]

        matches_created = 0
        for i in range(min(num_matches, len(available_bookings))):
            booking = available_bookings[i]

            try:
                # Double check if booking already has a match event
                if MatchEvent.objects.filter(booking=booking).exists():
                    continue

                match = MatchEvent.objects.create(
                    court=booking.court,
                    booking=booking,
                    title=f"{booking.court.court_type} Match - {fake.catch_phrase()}",
                    description=fake.paragraph(nb_sentences=2),
                    sport_type=booking.court.court_type,
                    created_by=booking.player,
                    max_players=random.randint(4, 12),
                    current_players=1,
                    match_date=booking.booking_date,
                    match_time=booking.start_time,
                    duration_hours=random.randint(1, 3),
                    status=random.choice(
                        ['OPEN', 'FULL', 'IN_PROGRESS', 'COMPLETED']),
                    skill_level=random.choice(
                        ['BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'ANY'])
                )

                # Add creator as participant
                MatchParticipant.objects.create(
                    match_event=match,
                    player=booking.player,
                    is_confirmed=True,
                    attended=True if match.status == 'COMPLETED' else False
                )

                # Add other participants
                num_participants = random.randint(2, match.max_players - 1)
                participants = random.sample(
                    players, min(num_participants, len(players)))

                for participant in participants:
                    if participant != booking.player:
                        MatchParticipant.objects.create(
                            match_event=match,
                            player=participant,
                            is_confirmed=random.choice([True, True, False]),
                            attended=True if match.status == 'COMPLETED' else False
                        )
                        match.current_players += 1

                match.save()

                # Add player ratings for completed matches
                if match.status == 'COMPLETED':
                    all_participants = list(match.participants.all())
                    for participant in all_participants:
                        # Each participant rates 1-3 other participants
                        num_to_rate = random.randint(
                            1, min(3, len(all_participants) - 1))
                        others = [
                            p for p in all_participants if p.player != participant.player]

                        for other in random.sample(others, min(num_to_rate, len(others))):
                            # Check if rating already exists
                            if not PlayerRating.objects.filter(
                                match_event=match,
                                rated_by=participant.player,
                                rated_player=other.player
                            ).exists():
                                PlayerRating.objects.create(
                                    match_event=match,
                                    rated_by=participant.player,
                                    rated_player=other.player,
                                    rating=random.randint(3, 5),
                                    feedback=fake.sentence() if random.random() < 0.5 else '',
                                    misconduct_reported=random.random() < 0.05,
                                    misconduct_details=fake.sentence() if random.random() < 0.05 else ''
                                )

                matches_created += 1
                self.stdout.write(f'Created match event: {match.title}')

            except Exception as e:
                self.stdout.write(self.style.WARNING(
                    f'Skipped match creation: {str(e)}'))
                continue

        # Create booking shares (10% of bookings)
        self.stdout.write('\nCreating booking shares...')
        bookings_to_share = random.sample(
            created_bookings,
            min(count // 10, len(created_bookings))
        )

        for booking in bookings_to_share:
            share = BookingShare.objects.create(
                booking=booking,
                share_token=fake.uuid4()[:32],
                shared_by=booking.player,
                max_joins=random.randint(3, 8),
                expires_at=timezone.now() + timedelta(days=random.randint(7, 30))
            )

            # Add some joined users
            num_joined = random.randint(
                0, min(share.max_joins - 1, len(players)))
            joined_users = random.sample(players, num_joined)
            share.joined_users.set(joined_users)

        # Create recurring bookings
        self.stdout.write('\nCreating recurring bookings...')
        num_recurring = min(count // 10, len(players))

        for i in range(num_recurring):
            player = random.choice(players)
            court = random.choice(courts)

            RecurringBooking.objects.create(
                court=court,
                player=player,
                frequency=random.choice(['WEEKLY', 'BIWEEKLY', 'MONTHLY']),
                day_of_week=random.randint(0, 6),
                start_time=time(random.randint(6, 18), 0),
                end_time=time(random.randint(7, 20), 0),
                start_date=timezone.now().date(),
                end_date=timezone.now().date() + timedelta(days=random.randint(90, 365)),
                base_amount=court.base_hourly_rate,
                payment_method=random.choice(['ONLINE', 'CASH']),
                status=random.choice(
                    ['ACTIVE', 'ACTIVE', 'PAUSED', 'CANCELLED']),
                notes=fake.sentence(),
                created_by=player
            )

        # Print summary
        total_bookings = Booking.objects.count()
        total_matches = MatchEvent.objects.count()
        total_equipment_rentals = EquipmentRental.objects.count()
        total_notifications = BookingNotification.objects.count()
        total_recurring = RecurringBooking.objects.count()

        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully created:'))
        self.stdout.write(self.style.SUCCESS(
            f'  - {len(created_bookings)} new bookings (Total: {total_bookings})'))
        self.stdout.write(self.style.SUCCESS(
            f'  - {matches_created} new match events (Total: {total_matches})'))
        self.stdout.write(self.style.SUCCESS(
            f'  - {total_equipment_rentals} equipment rentals'))
        self.stdout.write(self.style.SUCCESS(
            f'  - {total_notifications} notifications'))
        self.stdout.write(self.style.SUCCESS(
            f'  - {total_recurring} recurring bookings'))
