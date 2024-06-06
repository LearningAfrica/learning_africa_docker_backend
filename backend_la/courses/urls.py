from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

router.register('categories', views.CategoryViewSet, basename='categories')
router.register('courses', views.CourseViewSet, basename='courses')
router.register('contents', views.ContentViewSet, basename='contents')
router.register('organizations', views.OrganizationViewSet, basename='organizations')
router.register('instructor_orgs', views.InstructorOrgViewSet, basename='instructor_orgs')

course_router = routers.NestedDefaultRouter(router, 'courses', lookup='course')
course_router.register('modules', views.ModuleViewSet, basename='modules')
course_router.register('students', views.CourseStudentViewSet, basename='students')


module_router = routers.NestedDefaultRouter(course_router, 'modules', lookup='module')
module_router.register('contents', views.ContentViewSet, basename='contents')


urlpatterns = router.urls + course_router.urls + module_router.urls