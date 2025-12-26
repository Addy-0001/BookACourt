from django.core.management.base import BaseCommand
from user_management.models import User, UserRole, Friendship
import random


class Command(BaseCommand):
    help = 'Seeds the database with sample friendships between players'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding friendships...')

        # Get all players
        players = list(User.objects.filter(role=UserRole.PLAYER))

        if len(players) < 2:
            self.stdout.write(self.style.ERROR('Not enough players to create friendships.'))
            return

        created_count = 0
        
        # Create friendships for each player
        for player in players:
            # Each player will have 2-8 friend connections
            num_friends = random.randint(2, min(8, len(players) - 1))
            
            # Get potential friends (exclude self and existing connections)
            existing_connections = set()
            
            # Get existing friendships (both directions)
            existing_from = Friendship.objects.filter(from_user=player).values_list('to_user_id', flat=True)
            existing_to = Friendship.objects.filter(to_user=player).values_list('from_user_id', flat=True)
            
            existing_connections.update(existing_from)
            existing_connections.update(existing_to)
            existing_connections.add(player.id)
            
            # Filter potential friends
            potential_friends = [p for p in players if p.id not in existing_connections]
            
            if not potential_friends:
                continue
            
            # Select random friends
            num_friends = min(num_friends, len(potential_friends))
            friends = random.sample(potential_friends, num_friends)
            
            for friend in friends:
                # Determine friendship status
                status = random.choices(
                    ['ACCEPTED', 'PENDING', 'REJECTED'],
                    weights=[0.7, 0.2, 0.1]  # 70% accepted, 20% pending, 10% rejected
                )[0]
                
                # Create friendship
                Friendship.objects.create(
                    from_user=player,
                    to_user=friend,
                    status=status
                )
                
                created_count += 1

        total_friendships = Friendship.objects.count()
        accepted = Friendship.objects.filter(status='ACCEPTED').count()
        pending = Friendship.objects.filter(status='PENDING').count()
        rejected = Friendship.objects.filter(status='REJECTED').count()

        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully created {created_count} new friendships'))
        self.stdout.write(self.style.SUCCESS(f'Total friendships: {total_friendships}'))
        self.stdout.write(self.style.SUCCESS(f'  - Accepted: {accepted}'))
        self.stdout.write(self.style.SUCCESS(f'  - Pending: {pending}'))
        self.stdout.write(self.style.SUCCESS(f'  - Rejected: {rejected}'))