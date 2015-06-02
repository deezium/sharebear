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
    url(r'^$', 'sharebear_app.views.adsindex', name='adsindex'),
    url(r'^index/$', 'sharebear_app.views.index', name='index'),
    url(r'^campaignrequest$', 'sharebear_app.views.campaignrequest', name='campaignrequest'),
    url(r'^success$', 'sharebear_app.views.campaignsuccess', name='campaignsuccess'),
    url(r'^login$', 'sharebear_app.views.login_view'),
    url(r'^logout$', 'sharebear_app.views.logout_view'),
    url(r'^signup$', 'sharebear_app.views.signup'),
    url(r'^subscribe$', 'sharebear_app.views.subscribe', name='mailing_subscribe'),
    url(r'^users/$', 'sharebear_app.views.users'),
    url(r'^users/(?P<username>\w.{0,30})/$', 'sharebear_app.views.users', name='users_username'),
    url(r'^edit/$', 'sharebear_app.views.edit_profile'),
    url(r'^editname/$', 'sharebear_app.views.edit_username'),
    url(r'^feed/$', 'sharebear_app.views.feed', name='messages_feed'),
    url(r'^all/$', 'sharebear_app.views.all', name='messages_all'),
    url(r'^trap/$', 'sharebear_app.views.trap', name='messages_trap'),
    #url(r'^trap/top$', 'sharebear_app.views.traptop', name='messages_traptop'),
    url(r'^house/$', 'sharebear_app.views.house', name='messages_house'),
    url(r'^trance/$', 'sharebear_app.views.trance', name='messages_trance'),
    url(r'^bass/$', 'sharebear_app.views.bass', name='messages_bass'),
    url(r'^harddance/$', 'sharebear_app.views.harddance', name='messages_harddance'),
    url(r'^fuckgenres/$', 'sharebear_app.views.fuckgenres', name='messages_fuckgenres'),
    url(r'^featured/(?P<entry_id>[\d]+)/$', 'sharebear_app.views.featured', name='artist_featured'),
    url(r'^featurededit/(?P<entry_id>[\d]+)/$', 'sharebear_app.views.featurededit', name='artist_featured_edit'),
    url(r'^featuredupdate/(?P<entry_id>[\d]+)$', 'sharebear_app.views.update_featuredentry'),
    url(r'^shares/(?P<username>\w.{0,30})/$', 'sharebear_app.views.shares', name='messages_shares'),
    #url(r'^feed_reply/(?P<user_id>[\d]+)/$', 'sharebear_app.views.feedreply', name='feed_reply'),
    #url(r'^outbox/$', 'sharebear_app.views.outbox', name='messages_outbox'),
    #url(r'^metaoutbox/$', 'sharebear_app.views.metaoutbox', name='messages_metaoutbox'),
    url(r'^compose/$', 'sharebear_app.views.compose', name='messages_compose'),
    url(r'^featuredcompose/$', 'sharebear_app.views.featuredcompose', name='featured_compose'),
    #url(r'^compose/(?P<recipient>[\w.@+-]+)/$', 'sharebear_app.views.compose', name='messages_compose_to'),
    #url(r'^reply/(?P<message_id>[\d]+)/$', 'sharebear_app.views.reply', name='messages_reply'),
    #url(r'^view/(?P<message_id>[\d]+)/$', 'sharebear_app.views.view', name='messages_detail'),
    url(r'^message/(?P<message_id>[\d]+)/$', 'sharebear_app.views.messageview', name='messages_view'),
    #url(r'^metaview/(?P<meta_message_id>[\d]+)/$', 'sharebear_app.views.metaview', name='meta_messages_detail'),
    url(r'^recipients/(?P<message_id>[\d]+)/$', 'sharebear_app.views.recipients', name='messages_recipients'),
    url(r'^delete/(?P<message_id>[\d]+)/$', 'sharebear_app.views.delete', name='messages_delete'),
    url(r'^settings$', 'sharebear_app.views.edit_profile', name='settings_page'),
    url(r'accounts/', include('allauth.urls')),
    #url(r'^random/$', 'sharebear_app.views.random', name='messages_random'),
    #url(r'^randomreply/(?P<meta_message_id>[\d]+)/$', 'sharebear_app.views.randomreply', name='messages_randomreply'),
    url(r'^like/(?P<message_id>[\d]+)/$', 'sharebear_app.views.like', name='message_like'),
    #url(r'^stats/(?P<message_id>[\d]+)/$', 'sharebear_app.views.stats', name='message_stats'),
    url(r'^play/(?P<message_id>[\d]+)/$', 'sharebear_app.views.play', name='track_play'),
    url(r'^follow/(?P<user_id>[\d]+)$', 'sharebear_app.views.follow', name='user_follow'),
    url(r'^likes/(?P<username>\w.{0,30})/$', 'sharebear_app.views.likes', name='user_likes'),
    url(r'^edit/(?P<username>\w.{0,30})/$', 'sharebear_app.views.edit', name='user_edit'),
    url('',include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^comments/', include('django_comments.urls')),
   ) 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


    # REMOVE STATIC LINE FOR PRODUCTION?
    # FIGURE OUT HOW TO SEPARATE MEDIA URL FROM STATIC URL AND MOVE CUSTOM.CSS TO WHERE STATIC URL IS