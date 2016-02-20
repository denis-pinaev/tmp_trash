from django.conf.urls.defaults import patterns, include, url
import settings

urlpatterns = patterns('',
    url(r'^import/*$', 'imp_exp.views.import_person', {}, 'imp_exp_import'),
    url(r'^export/*$', 'imp_exp.views.export_person', {}, 'imp_exp_export'),
)