from django.db import models


class JobPosting(models.Model):
    """
    Represents a single job listing on TechHire.
    
    Public fields  : title, description, location
    Premium fields : company_name, salary_range, application_link
    """

    # ── Public fields (visible to everyone) ──────────────────────────────────
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)

    # ── Premium fields (masked for Basic users) ───────────────────────────────
    company_name = models.CharField(max_length=200)
    salary_range = models.CharField(
        max_length=100,
        help_text='e.g. "$120,000 – $160,000"',
    )
    application_link = models.URLField(max_length=500)

    # ── Metadata ──────────────────────────────────────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Job Posting"
        verbose_name_plural = "Job Postings"

    def __str__(self):
        return f"{self.title} @ {self.company_name}"
