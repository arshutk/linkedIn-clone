from django.contrib import admin

from organization import models

admin.site.register(models.Organization)
admin.site.register(models.OrganizationDetail)
admin.site.register(models.OrganizationProfile)
admin.site.register(models.OrganizationStaff)
# admin.site.register(models.OrganizationAnalytic)
# admin.site.register(models.JobVacancy)