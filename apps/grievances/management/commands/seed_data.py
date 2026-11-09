from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.grievances.models import Department, OfficerProfile, CitizenProfile


class Command(BaseCommand):
    help = 'Seeds initial department hierarchy and administrative/officer user accounts.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding department and user data...")

        departments_data = [
            {'org_code': 'MIN_WATER', 'org_name': 'Ministry of Jal Shakti / Water Resources', 'default_sla_days': 15, 'daily_capacity': 8},
            {'org_code': 'MIN_SANAT', 'org_name': 'Department of Drinking Water and Sanitation', 'default_sla_days': 10, 'daily_capacity': 12},
            {'org_code': 'MIN_ROADS', 'org_name': 'Ministry of Road Transport and Highways', 'default_sla_days': 20, 'daily_capacity': 6},
            {'org_code': 'MIN_POWER', 'org_name': 'Ministry of Power', 'default_sla_days': 7, 'daily_capacity': 15},
            {'org_code': 'MIN_FINAN', 'org_name': 'Department of Financial Services (Pensions/Banking)', 'default_sla_days': 30, 'daily_capacity': 10},
        ]

        created_depts = {}
        for d in departments_data:
            dept, _ = Department.objects.get_or_create(
                org_code=d['org_code'],
                defaults=d
            )
            created_depts[d['org_code']] = dept

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@jiit.ac.in', 'admin123')
            self.stdout.write(self.style.SUCCESS("Created Superuser: admin / admin123"))

        if not User.objects.filter(username='officer_water').exists():
            officer_user = User.objects.create_user('officer_water', 'officer@jiit.ac.in', 'officer123', first_name="Rajesh", last_name="Kumar")
            OfficerProfile.objects.create(
                user=officer_user,
                department=created_depts['MIN_WATER'],
                designation="Senior Nodal Officer"
            )
            self.stdout.write(self.style.SUCCESS("Created Officer: officer_water / officer123"))

        if not User.objects.filter(username='citizen_user').exists():
            citizen_user = User.objects.create_user('citizen_user', 'citizen@jiit.ac.in', 'citizen123', first_name="Amit", last_name="Sharma")
            CitizenProfile.objects.create(
                user=citizen_user,
                phone_number="9876543210",
                state="Uttar Pradesh",
                district="Gautam Buddha Nagar",
                pincode="201301"
            )
            self.stdout.write(self.style.SUCCESS("Created Citizen: citizen_user / citizen123"))

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully."))