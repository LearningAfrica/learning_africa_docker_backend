# Generated by Django 4.2.7 on 2024-06-06 13:10

from django.db import migrations, models
import django.db.models.deletion
import shortuuid.django_fields
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        ('system_users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system_users.instructor')),
            ],
            options={
                'verbose_name_plural': 'Course Categories',
                'db_table': 'course_category',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('overview', models.TextField()),
                ('course_image', models.ImageField(blank=True, null=True, upload_to='courses_thumbnails')),
                ('is_premium', models.BooleanField(default=False)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('currency', models.CharField(blank=True, default='Ksh', max_length=20, null=True)),
                ('is_private', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='courses.category')),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses_created', to='system_users.instructor')),
            ],
            options={
                'verbose_name_plural': 'Courses',
                'db_table': 'courses',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to='file_contents')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='image_contents')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', shortuuid.django_fields.ShortUUIDField(alphabet=None, editable=False, length=12, max_length=12, prefix='', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='org_logos')),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Organizations',
                'db_table': 'organizations',
            },
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('text', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('url', models.URLField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StudentCourseEnrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrolled_time', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_enrolled', to='courses.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_enrolled', to='system_users.student')),
            ],
            options={
                'verbose_name_plural': 'Enrolled Courses',
                'db_table': 'enrolled_courses',
            },
        ),
        migrations.CreateModel(
            name='OrganizationStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.organization')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system_users.student')),
            ],
            options={
                'verbose_name_plural': 'Students Organization',
                'db_table': 'student_organizations',
            },
        ),
        migrations.CreateModel(
            name='OrganizationInstructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system_users.instructor')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.organization')),
            ],
            options={
                'verbose_name_plural': 'Instructors Organization',
                'db_table': 'instructor_organizations',
            },
        ),
        migrations.CreateModel(
            name='OrganizationAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(blank=True, max_length=200, null=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system_users.admin')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.organization')),
            ],
            options={
                'verbose_name_plural': 'Admins Organization',
                'db_table': 'admin_organizations',
            },
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='courses.course')),
            ],
            options={
                'verbose_name_plural': 'Modules',
                'db_table': 'modules',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.organization'),
        ),
        migrations.AddField(
            model_name='course',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('content_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(limit_choices_to={'model__in': ('text', 'video', 'image', 'file')}, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contents', to='courses.module')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.organization'),
        ),
    ]
