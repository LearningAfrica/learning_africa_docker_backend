from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from taggit.serializers import TagListSerializerField

from . import models

from system_users.models import Instructor, Admin
from system_users.serializers import StudentSerializer, InstructorSerializer

class CreateOrganizationAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Organization
        fields = ['id', 'name', 'logo']

    def create(self, validated_data):
        admin = Admin.objects.get(user__id=self.context['user_id'])
        if not admin:
            raise serializers.ValidationError({'error': 'You are not allowed to perform this action'})
        organization = models.Organization.objects.create(**validated_data)
        models.OrganizationAdmin.objects.create(admin=admin, organization=organization)
        return organization

class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Organization
        fields = ['id', 'name', 'logo_url']

class CreateCategorySerializer(serializers.ModelSerializer):

    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = models.Category
        fields = ['id', 'organization', 'title', 'slug'] 

    def create(self, validated_data):
        creator = Instructor.objects.get(user_id=self.context['user_id'])
        course_category = models.Category.objects.create(creator=creator, **validated_data)
        return course_category

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = ['id', 'title', 'slug', 'created', 'updated']

class InstructorOrgSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OrganizationInstructor
        fields = ['id', 'organization']

class CourseStudentSerializer(serializers.ModelSerializer):

    student = StudentSerializer()

    class Meta:
        model = models.StudentCourseEnrollment
        fields = ['id', 'student', 'enrolled_time']

class SimpleCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = ['id','title']

class CreateCourseSerializer(serializers.ModelSerializer):

    tags = TagListSerializerField()

    class Meta:
        model = models.Course
        fields = ['id', 'organization', 'category', 'title', 'overview', 'course_image', 'is_premium', 'price', 'is_private', 'tags']

    def create(self, validated_data):
        instructor = Instructor.objects.get(user_id=self.context['user_id'])
        # course_data = validated_data.pop('course')
        return models.Course.objects.create(instructor=instructor, **validated_data)

class CourseSerializer(serializers.ModelSerializer):

    instructor = InstructorSerializer(read_only=True)
    category = SimpleCategorySerializer(read_only=True)
    tags = TagListSerializerField()

    class Meta:
        model = models.Course
        fields = ['id', 'instructor', 'title', 'slug', 'overview', 'course_image_url', 'created', 'category', 'tags']

class CreateModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Module
        fields = ['id', 'course', 'title', 'description']

class ModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Module
        fields = ['id', 'course', 'title', 'description']
    
class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Text
        fields = ['text']

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Video
        fields = ['url']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = ['image']

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.File
        fields = ['file']

class CreateContentSerializer(serializers.ModelSerializer):   

    text = serializers.CharField(required=False)
    file = serializers.FileField(required=False)
    image = serializers.ImageField(required=False)
    url = serializers.URLField(required=False)

    class Meta:
        model = models.Content
        fields = ['module','content_type', 'title', 'text', 'url', 'file', 'image']

    def create(self, validated_data):
        content_type = validated_data.pop('content_type')
        title = validated_data.pop('title')
        
        if content_type.model == 'text':
            instance = models.Text.objects.create(**validated_data)
        elif content_type.model == 'video':
            instance = models.Video.objects.create(**validated_data)
        elif content_type.model == 'file':
            instance = models.File.objects.create(**validated_data)
        elif content_type.model == 'image':
            instance = models.Image.objects.create(**validated_data)
        
        content = models.Content.objects.create(title=title, content_type=content_type, content_id=instance.id)
        return content

# class UpdateContentSerializer(serializers.ModelSerializer):

class ContentSerializer(serializers.ModelSerializer):

    content_object = serializers.SerializerMethodField()

    class Meta:
        model = models.Content
        fields = ['id', 'title', 'content_type', 'content_object']

    def get_content_object(self, instance):
        content_object = instance.content_object
        content_type = ContentType.objects.get_for_model(content_object)

        if content_type.model == 'text':
            text_serializer = TextSerializer(content_object)
            return text_serializer.data
        elif content_type.model == 'video':
            video_serializer = VideoSerializer(content_object)
            return video_serializer.data
        elif content_type.model == 'file':
            file_serializer = FileSerializer(content_object)
            return file_serializer.data
        elif content_type.model == 'image':
            image_serializer = ImageSerializer(content_object)
            return image_serializer.data
        
        return None
    
    def update(self, instance, validated_data):
        # content_data = validated_data.get('content', {})
        content_type = validated_data.get('content_type')

        instance.title = validated_data.get('title', instance.title)
        instance.content_type = content_type
        instance.save()

        # Update content object based on content type
        content_object = instance.content_object
        print(content_object)

        try:
            if content_type.model == 'text':
                text_data = validated_data.get('text', {})
                content_serializer = TextSerializer(content_object, data=text_data, partial=True)

                if content_object and content_serializer.is_valid():
                    content_serializer.save()
        except Exception as e:
            return serializers.ValidationError({'error': 'error modify content'})
        return instance
    
# Student Accessing Course, Module and Contents

class StudentContentSerializer(serializers.ModelSerializer):

    content_object = serializers.SerializerMethodField()

    class Meta:
        model = models.Content
        fields = ['id', 'title', 'content_type', 'content_object']

    def get_content_object(self, instance):
        content_object = instance.content_object
        content_type = ContentType.objects.get_for_model(content_object)

        if content_type.model == 'text':
            text_serializer = TextSerializer(content_object)
            return text_serializer.data
        elif content_type.model == 'video':
            video_serializer = VideoSerializer(content_object)
            return video_serializer.data
        elif content_type.model == 'file':
            file_serializer = FileSerializer(content_object)
            return file_serializer.data
        elif content_type.model == 'image':
            image_serializer = ImageSerializer(content_object)
            return image_serializer.data
        
        return None

class StudentModuleContentSerializer(serializers.ModelSerializer):

    contents = StudentContentSerializer()

    class Meta:
        model = models.Module
        fields = ['contents']

class StudentModuleSerializer(serializers.ModelSerializer):

    contents = StudentModuleContentSerializer(many=True)

    class Meta:
        model = models.Module
        fields = ['id', 'title', 'description', 'contents']

class CourseModulesSerializer(serializers.ModelSerializer):

    modules = StudentModuleSerializer()

    class Meta:
        model = models.Course
        fields = ['id', 'modules']

class CourseWithContentSerializer(serializers.ModelSerializer):

    # subject = SimpleSubjectSerializer()
    owner = InstructorSerializer(read_only=True)
    modules = CourseModulesSerializer(many=True, read_only=True)

    class Meta:
        model = models.Course
        fields = ['id', 'owner', 'title', 'overview', 'created', 'updated', 'modules']