from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.template.defaultfilters import slugify
from django.conf import settings
from shortuuid.django_fields import ShortUUIDField
from taggit.managers import TaggableManager

# from .fields import OrderField, ModuleOrderField
from system_users.models import Instructor, Student, Admin

class Organization(models.Model):
    id = ShortUUIDField(primary_key=True, length=12, max_length=12, editable=False)
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='org_logos', blank=True, null=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'organizations'
        verbose_name_plural = 'Organizations'

    def __str__(self):
        return self.name
    
    def logo_url(self):
        if self.logo:
            return f'{settings.WEBSITE_URL}{self.logo.url}'
        else:
            return ''

class OrganizationAdmin(models.Model):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    position = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'admin_organizations'
        verbose_name_plural = 'Admins Organization'

    def __str__(self):
        return f"{self.organization.name} - {self.admin.first_name()}"

class OrganizationInstructor(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    class Meta:
        db_table = 'instructor_organizations'
        verbose_name_plural = 'Instructors Organization'

class OrganizationStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    class Meta:
        db_table = 'student_organizations'
        verbose_name_plural = 'Students Organization'

class Category(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    creator = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'course_category'
        verbose_name_plural = 'Course Categories'
        ordering = ['title']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        original_slug = slugify(self.title)
        queryset = Category.objects.all().filter(slug__iexact=original_slug).count()
        count = 1
        slug = original_slug
        while(queryset):
            slug = original_slug + '-' + str(count)
            count += 1
            queryset = Category.objects.all().filter(slug__iexact=slug).count()
        self.slug = slug

        super(Category, self).save(*args, **kwargs)

class Course(models.Model):
    instructor = models.ForeignKey(Instructor, related_name='courses_created', on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    course_image = models.ImageField(upload_to='courses_thumbnails', blank=True, null=True)
    is_premium = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=20, blank=True, null=True, default='Ksh')
    is_private = models.BooleanField(default=False)
    tags = TaggableManager(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'courses'
        verbose_name_plural = 'Courses'
        ordering = ['-created']

    def __str__(self):
        return self.title
    
    def course_image_url(self):
        if self.course_image:
            return f'{settings.WEBSITE_URL}{self.course_image.url}'
        return ''
    
    def save(self, *args, **kwargs):
        original_slug = slugify(self.title)
        queryset = Course.objects.all().filter(slug__iexact=original_slug).count()
        count = 1
        slug = original_slug
        while(queryset):
            slug = original_slug + '-' + str(count)
            count += 1
            queryset = Course.objects.all().filter(slug__iexact=slug).count()
        self.slug = slug

        super(Course, self).save(*args, **kwargs)

class StudentCourseEnrollment(models.Model):
    course = models.ForeignKey(Course, related_name='course_enrolled', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='student_enrolled', on_delete=models.CASCADE)
    enrolled_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Enrolled Courses'
        db_table = 'enrolled_courses'

    def __str__(self):
        return f'{self.course.title} - {self.student.username()}'
    
class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # order = OrderField(blank=True, for_fields=['course'])
    # order = ModuleOrderField(blank=True, for_fields=['course'])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'modules'
        verbose_name_plural = 'Modules'
        # ordering = ['order']

    def __str__(self):
        return f'{self.title}'

class ItemBase(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Text(ItemBase):
    text = models.TextField()

    def __str__(self):
        return self.text

class Video(ItemBase):
    url = models.URLField()

    def __str__(self):
        return self.url

class File(ItemBase):
    file = models.FileField(upload_to='file_contents')

    def __str__(self):
        return self.file

class Image(ItemBase):
    image = models.ImageField(upload_to='image_contents')

    def __str__(self):
        return self.image
    
class Content(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='contents')
    title = models.CharField(max_length=250)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in': ('text', 'video', 'image', 'file')})
    content_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'content_id')