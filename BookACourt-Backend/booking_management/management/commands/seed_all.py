from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Seeds the entire database with sample data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=50,
            help='Number of users to create'
        )
        parser.add_argument(
            '--courts',
            type=int,
            default=20,
            help='Number of courts to create'
        )
        parser.add_argument(
            '--bookings',
            type=int,
            default=100,
            help='Number of bookings to create'
        )
        parser.add_argument(
            '--flush',
            action='store_true',
            help='Flush database before seeding (WARNING: This will delete all data!)'
        )

    def handle(self, *args, **kwargs):
        users_count = kwargs['users']
        courts_count = kwargs['courts']
        bookings_count = kwargs['bookings']
        should_flush = kwargs['flush']

        self.stdout.write(self.style.WARNING('\n' + '='*50))
        self.stdout.write(self.style.WARNING('BookACourt Database Seeder'))
        self.stdout.write(self.style.WARNING('='*50 + '\n'))

        if should_flush:
            self.stdout.write(self.style.WARNING('⚠️  WARNING: This will DELETE all existing data!'))
            confirm = input('Are you sure you want to continue? (yes/no): ')
            
            if confirm.lower() != 'yes':
                self.stdout.write(self.style.ERROR('Seeding cancelled.'))
                return
            
            self.stdout.write(self.style.WARNING('\nFlushing database...'))
            call_command('flush', '--no-input')
            self.stdout.write(self.style.SUCCESS('✓ Database flushed\n'))

        # Step 1: Seed Users
        self.stdout.write(self.style.WARNING('Step 1/4: Seeding Users...'))
        self.stdout.write('-' * 50)
        call_command('seed_users', count=users_count)
        self.stdout.write(self.style.SUCCESS('✓ Users seeded\n'))

        # Step 2: Seed Courts
        self.stdout.write(self.style.WARNING('Step 2/4: Seeding Courts...'))
        self.stdout.write('-' * 50)
        call_command('seed_courts', count=courts_count)
        self.stdout.write(self.style.SUCCESS('✓ Courts seeded\n'))

        # Step 3: Seed Bookings
        self.stdout.write(self.style.WARNING('Step 3/4: Seeding Bookings...'))
        self.stdout.write('-' * 50)
        call_command('seed_bookings', count=bookings_count)
        self.stdout.write(self.style.SUCCESS('✓ Bookings seeded\n'))

        # Step 4: Seed Friendships
        self.stdout.write(self.style.WARNING('Step 4/4: Seeding Friendships...'))
        self.stdout.write('-' * 50)
        call_command('seed_friendships')
        self.stdout.write(self.style.SUCCESS('✓ Friendships seeded\n'))

        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('✓ Database seeding completed successfully!'))
        self.stdout.write(self.style.SUCCESS('='*50))
        
        self.stdout.write('\n📊 Summary:')
        self.stdout.write(f'  • Users: ~{users_count}')
        self.stdout.write(f'  • Courts: ~{courts_count}')
        self.stdout.write(f'  • Bookings: ~{bookings_count}')
        self.stdout.write(f'  • Friendships: Auto-generated')
        self.stdout.write(f'  • Reviews: Auto-generated')
        self.stdout.write(f'  • Match Events: Auto-generated\n')
        
        self.stdout.write('🔑 Test Credentials:')
        self.stdout.write('  Super User:')
        self.stdout.write('    Phone: +9779801234567')
        self.stdout.write('    Password: admin123\n')
        
        self.stdout.write('  Regular Users:')
        self.stdout.write('    Phone: Any generated number')
        self.stdout.write('    Password: password123\n')