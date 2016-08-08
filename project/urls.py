from django.conf.urls import patterns, include, url
from django.contrib import admin
from accounts.views import index
from side.views import *
from talents.views import *
from project import settings
import os
from django.conf.urls.static import static
from manager import urls as manager_urls
urlpatterns = [
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #config by libaokun
    url(r'^accounts/', include('accounts.urls', namespace="accounts")),
    url(r'^$',index, name='index'),
    url(r'^refresh/$', 'accounts.views.refresh', name='refresh'),

    url(r'^receive/','resume.views.receive',name = 'receive'),
    url(r'^import_resume/','resume.views.import_resume',name='import_resume'),
    url(r'^repeat/','resume.views.repeat', name='repeat'),
    url(r'^import_ResumeID/','resume.views.import_ResumeID',name = 'import_ResumeID'),
    url(r'^check_importid/','resume.views.check_importid',name = 'check_importid'),
    url(r'^fail_importid/','resume.views.fail_importid',name = 'fail_importid'),
    url(r'^import_choice/','resume.views.import_choice',name = 'import_choice'),
    url(r'^import_resume2/','resume.views.import_resume2',name = 'import_resume2'),  
    url(r'^all_user/','resume.views.all_user',name = 'all_user'), 
    url(r'^manage_importedid/','resume.views.manage_importedid',name = 'manage_importedid'),
    url(r'^ownimport_id/','resume.views.ownimport_id',name = 'ownimport_id'),
    url(r'^check_idgroup/','resume.views.check_idgroup',name = 'check_idgroup'),
    url(r'^updata_resume/(\d+)','resume.views.updata_resume',name = 'updata_resume'),
    url(r'^down_file/([\s\S]*)','resume.views.down_file',name = 'down_file'),
    url(r'^id_processed/','resume.views.id_processed',name = 'id_processed'),

    url(r'^mywrite/(?P<resume_id>[^/]+)/','talents.views.mywrite',name = 'mywrite'),
    url(r'^myread/','talents.views.myread',name = 'myread'),
    url(r'^talents/',include('talents.urls',namespace="talents")),
    #config by linana
    url(r'^side/', include('side.urls', namespace="side")),
    url(r'^static/?P<path>.*/$', 'django.views.static.serve',{'document_root': settings.STATIC_ROOT}),

    url(r'^manager/', include('manager.urls', namespace='manager')),
]
#urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
