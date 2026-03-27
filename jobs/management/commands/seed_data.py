"""
Seed the database with realistic sample job postings and test users.

Usage:
    python manage.py seed_data
    python manage.py seed_data --clear     # wipe existing data first
"""
import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile
from jobs.models import JobPosting

JOBS = [
    {
        "title": "Senior Backend Engineer",
        "description": (
            "We are looking for a Senior Backend Engineer to design and implement "
            "scalable REST APIs using Python and Django. You will work closely with "
            "frontend teams and DevOps to ship reliable, well-tested features. "
            "Strong understanding of PostgreSQL, Redis, and containerised deployments required."
        ),
        "location": "Remote",
        "company_name": "Stripe",
        "salary_range": "$160,000 – $210,000",
        "application_link": "https://stripe.com/jobs/senior-backend-engineer",
    },
    {
        "title": "Frontend Engineer (React)",
        "description": (
            "Join our product team to build beautiful, performant user interfaces. "
            "You will own features end-to-end using React, TypeScript, and GraphQL. "
            "Experience with design systems, accessibility standards, and CI/CD pipelines "
            "is a strong plus."
        ),
        "location": "San Francisco, CA",
        "company_name": "Figma",
        "salary_range": "$140,000 – $185,000",
        "application_link": "https://figma.com/careers/frontend-engineer",
    },
    {
        "title": "Staff Machine Learning Engineer",
        "description": (
            "Lead the development of ML infrastructure that powers our recommendation "
            "and ranking systems serving 500 M+ users. You will mentor junior engineers, "
            "drive architectural decisions, and collaborate with research scientists. "
            "PhD or equivalent industry experience in ML required."
        ),
        "location": "New York, NY",
        "company_name": "Spotify",
        "salary_range": "$220,000 – $280,000",
        "application_link": "https://spotify.com/jobs/staff-ml-engineer",
    },
    {
        "title": "DevOps / Platform Engineer",
        "description": (
            "Own our Kubernetes-based cloud infrastructure on AWS. Responsibilities include "
            "improving deployment pipelines, observability tooling, and reliability SLOs. "
            "You should be comfortable with Terraform, Helm, Prometheus, and Python scripting."
        ),
        "location": "Remote",
        "company_name": "Cloudflare",
        "salary_range": "$150,000 – $195,000",
        "application_link": "https://cloudflare.com/careers/devops-engineer",
    },
    {
        "title": "iOS Engineer",
        "description": (
            "Build and ship new features in our iOS app used by millions of consumers daily. "
            "You will work in Swift, follow Apple HIG guidelines, and collaborate with product "
            "designers to deliver polished, performant experiences. SwiftUI experience preferred."
        ),
        "location": "Austin, TX",
        "company_name": "Apple",
        "salary_range": "$175,000 – $230,000",
        "application_link": "https://jobs.apple.com/ios-engineer",
    },
    {
        "title": "Full-Stack Engineer (Node + React)",
        "description": (
            "Help us grow our SaaS platform from 10 K to 1 M users. You will contribute to "
            "both the Node.js API and the React dashboard, write integration tests, and "
            "participate in on-call rotations. We value pragmatism, clear communication, "
            "and a product-minded engineering culture."
        ),
        "location": "Remote",
        "company_name": "Linear",
        "salary_range": "$130,000 – $170,000",
        "application_link": "https://linear.app/careers/full-stack-engineer",
    },
    {
        "title": "Security Engineer",
        "description": (
            "Protect our infrastructure and customer data. You will conduct threat modelling, "
            "pen-testing, and security code reviews. Own the bug bounty programme and "
            "coordinate incident response. Deep experience with OWASP, cloud IAM, "
            "and secrets management required."
        ),
        "location": "Seattle, WA",
        "company_name": "Amazon",
        "salary_range": "$180,000 – $240,000",
        "application_link": "https://amazon.jobs/security-engineer",
    },
    {
        "title": "Data Engineer",
        "description": (
            "Design and maintain data pipelines that ingest, transform, and serve petabytes "
            "of event data to analysts and ML teams. You will work with Spark, dbt, Airflow, "
            "and Snowflake. Strong SQL skills and experience building reliable batch and "
            "streaming pipelines are essential."
        ),
        "location": "Chicago, IL",
        "company_name": "Brex",
        "salary_range": "$135,000 – $175,000",
        "application_link": "https://brex.com/careers/data-engineer",
    },
    {
        "title": "Engineering Manager — Platform",
        "description": (
            "Lead a team of 6 platform engineers responsible for shared infrastructure, "
            "internal tooling, and developer experience. You will run quarterly planning, "
            "grow your team through coaching and hiring, and partner with product to define "
            "the roadmap. Prior hands-on engineering experience required."
        ),
        "location": "Remote",
        "company_name": "Vercel",
        "salary_range": "$200,000 – $260,000",
        "application_link": "https://vercel.com/careers/engineering-manager-platform",
    },
    {
        "title": "Backend Engineer — Payments",
        "description": (
            "Work on the core payments platform processing billions of dollars monthly. "
            "Responsibilities include designing fault-tolerant microservices, integrating "
            "with card networks, and maintaining compliance with PCI-DSS. "
            "Experience with Go or Java and distributed systems is highly desirable."
        ),
        "location": "New York, NY",
        "company_name": "Ramp",
        "salary_range": "$155,000 – $200,000",
        "application_link": "https://ramp.com/careers/backend-engineer-payments",
    },
    {
        "title": "Junior Frontend Developer",
        "description": (
            "A great opportunity to start your frontend career. You will work alongside "
            "senior engineers to build React components, fix bugs, and improve test coverage. "
            "We offer mentorship, structured onboarding, and a clear growth path."
        ),
        "location": "Remote",
        "company_name": "Notion",
        "salary_range": "$80,000 – $110,000",
        "application_link": "https://notion.so/careers/junior-frontend-developer",
    },
    {
        "title": "Site Reliability Engineer",
        "description": (
            "Ensure the availability, latency, and efficiency of our distributed services. "
            "You will write runbooks, build alerting dashboards in Grafana, and participate "
            "in blameless post-mortems. Strong Linux internals knowledge and Python scripting "
            "skills required."
        ),
        "location": "San Francisco, CA",
        "company_name": "Datadog",
        "salary_range": "$165,000 – $215,000",
        "application_link": "https://datadog.com/careers/sre",
    },
]

TEST_USERS = [
    {
        "username": "basic_user",
        "email": "basic@techhire.dev",
        "password": "TestPass123!",
        "tier": "basic",
    },
    {
        "username": "premium_user",
        "email": "premium@techhire.dev",
        "password": "TestPass123!",
        "tier": "premium",
    },
]


class Command(BaseCommand):
    help = "Seed the database with sample job postings and test users."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete all existing JobPostings and non-superuser accounts before seeding.",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            deleted, _ = JobPosting.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"  Cleared {deleted} job postings."))
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.WARNING("  Cleared non-superuser accounts."))

        # ── Create job postings ───────────────────────────────────────────────
        created_jobs = 0
        for job_data in JOBS:
            _, created = JobPosting.objects.get_or_create(
                title=job_data["title"],
                company_name=job_data["company_name"],
                defaults=job_data,
            )
            if created:
                created_jobs += 1

        self.stdout.write(self.style.SUCCESS(f"✅  Created {created_jobs} job postings."))

        # ── Create test users ─────────────────────────────────────────────────
        for u in TEST_USERS:
            user, created = User.objects.get_or_create(
                username=u["username"],
                defaults={"email": u["email"]},
            )
            if created:
                user.set_password(u["password"])
                user.save()
                user.profile.membership_tier = u["tier"]
                user.profile.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✅  Created user '{u['username']}' (tier: {u['tier']}) "
                        f"— password: {u['password']}"
                    )
                )
            else:
                self.stdout.write(f"⏭   User '{u['username']}' already exists, skipped.")

        self.stdout.write(self.style.SUCCESS("\n🎉  Seed complete!"))
        self.stdout.write(
            "\nTest credentials:\n"
            "  basic_user   / TestPass123!  →  Basic tier (fields masked)\n"
            "  premium_user / TestPass123!  →  Premium tier (fields revealed)\n"
        )
