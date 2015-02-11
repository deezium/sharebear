from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from sharebear_app.views import *

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sharebear.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'sharebear_app.views.index', name='index'),
    url(r'^login$', 'sharebear_app.views.login_view'),
    url(r'^logout$', 'sharebear_app.views.logout_view'),
    url(r'^signup$', 'sharebear_app.views.signup'),
    # url(r'^feelings$', 'sharebear_app.views.public'),
    url(r'^users/$', 'sharebear_app.views.users'),
    url(r'^users/(?P<username>\w.{0,30})/$', 'sharebear_app.views.users', name='users-username'),
    url(r'^edit/$', 'sharebear_app.views.edit_profile'),
    #url(r'^inbox/$', 'sharebear_app.views.inbox', name='messages_inbox'),
    url(r'^feed/$', 'sharebear_app.views.feed', name='messages_feed'),
    #url(r'^feed_reply/(?P<user_id>[\d]+)/$', 'sharebear_app.views.feedreply', name='feed_reply'),
    #url(r'^outbox/$', 'sharebear_app.views.outbox', name='messages_outbox'),
    #url(r'^metaoutbox/$', 'sharebear_app.views.metaoutbox', name='messages_metaoutbox'),
    url(r'^compose/$', 'sharebear_app.views.compose', name='messages_compose'),
    #url(r'^compose/(?P<recipient>[\w.@+-]+)/$', 'sharebear_app.views.compose', name='messages_compose_to'),
    #url(r'^reply/(?P<message_id>[\d]+)/$', 'sharebear_app.views.reply', name='messages_reply'),
    #url(r'^view/(?P<message_id>[\d]+)/$', 'sharebear_app.views.view', name='messages_detail'),
    url(r'^message/(?P<message_id>[\d]+)/$', 'sharebear_app.views.messageview', name='messages_view'),
    #url(r'^metaview/(?P<meta_message_id>[\d]+)/$', 'sharebear_app.views.metaview', name='meta_messages_detail'),
    #url(r'^conversations/$', 'sharebear_app.views.conversationbox', name='conversationbox'),
    #url(r'^conversation/(?P<conversation_id>[\d]+)/$', 'sharebear_app.views.conversations', name='conversations_detail'),
    #url(r'^convo_reply/(?P<conversation_id>[\d]+)/$', 'sharebear_app.views.convoreply', name='conversations_reply'),
    url(r'^recipients/(?P<message_id>[\d]+)/$', 'sharebear_app.views.recipients', name='messages_recipients'),
    #url(r'^delete/(?P<message_id>[\d]+)/$', 'sharebear_app.views.delete', name='messages_delete'),
    #url(r'^undelete/(?P<message_id>[\d]+)/$', 'sharebear_app.views.undelete', name='messages_undelete'),
    #url(r'^trash$', 'sharebear_app.views.trash', name='messages_trash'),
    url(r'^settings$', 'sharebear_app.views.edit_profile', name='settings_page'),
    url(r'accounts/', include('allauth.urls')),
    #url(r'^random/$', 'sharebear_app.views.random', name='messages_random'),
    #url(r'^randomreply/(?P<meta_message_id>[\d]+)/$', 'sharebear_app.views.randomreply', name='messages_randomreply'),
    url(r'^like/(?P<feed_story_id>[\d]+)/$', 'sharebear_app.views.like', name='story_like'),
    url('',include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
   ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

urlpatterns += staticfiles_urlpatterns()

    # REMOVE STATIC LINE FOR PRODUCTION?
    # FIGURE OUT HOW TO SEPARATE MEDIA URL FROM STATIC URL AND MOVE CUSTOM.CSS TO WHERE STATIC URL IS