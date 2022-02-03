# from django.db import models


# class ProductManager(models.Manager):
#     def published(self):
#         from Products.models import Product  # Import here to prevent circular imports

#         return self.filter(status=Product.PUBLISHED)


# class LineInInvoiceManager(models.Manager):
#     def published(self):
#         from Products.models import LineInInvoice

#         # Import here to prevent circular imports

#         return self.filter(status=LineInInvoice.PUBLISHED)


# class JobManager(models.Manager):
#     def published(self):
#         from Persons.models import Job

#         # Import here to prevent circular imports

#         return self.filter(status=Job.PUBLISHED)


# class EmployeeManager(models.Manager):
#     def published(self):
#         from Persons.models import Employee

#         # Import here to prevent circular imports

#         return self.filter(status=Employee.PUBLISHED)
