#coding=utf-8

from django.contrib.auth.models import Group, Permission
#from django.utils.translation import ugettext as _
#from django.utils.translation import gettext_lazy as _

_ = lambda s: s


perms = dict()
perms["perm_system_settings"] = "Can view system settings" # only superadmin
perms["perm_settings"] = "Can view settings" # only admins
perms["perm_setup"] = "Can view setup" # only admins
perms["perm_monitoring"] = "Can view monitoring" # only admins
perms["perm_logs"] = "Can view logs" # for admins & moderator
perms["perm_logs_sessions"] = "Can view sessions logs"
perms["perm_logs_clear"] = "Can clear logs"
perms["perm_logs_export"] = "Can expport logs"
perms["perm_lists"] = "Can view lists" # for admins & moderator
perms["perm_lists_edit"] = "Can edit lists"
perms["perm_maps"] = "Can view maps"
perms["perm_maps_edit"] = "Can view maps"
perms["perm_security"] = "Can view security"
perms["perm_view"] = "Can view view"
perms["perm_wizard"] = "Can view wizard"
perms["perm_security_main"] = "Can view security main"
perms["perm_distortion"] = "Can view distotion"

perms["perm_videoarchive"] = "Can view videoarchive block"
perms["perm_videoarchive_settings"] = "Can view videoarchive settings"
perms["perm_videoarchive_tasks"] = "Can view videoarchive tasks page"
perms["perm_videoarchive_processes"] = "Can view videoarchive processes page"
perms["perm_videoarchive_journal"] = "Can view videoarchive journal page"
perms["perm_videoarchive_calendar"] = "Can view videoarchive calendar page"
perms["perm_videoarchive_videos"] = "Can view videoarchive videos page"
perms["perm_videoarchive_analysis"] = "Can view videoarchive analysis"
perms["perm_videoarchive_add_task"] = "Can add videoarchive tasks"
perms["perm_videoarchive_delete_task"] = "Can delete videoarchive tasks"
perms["perm_videoarchive_stop_process"] = "Can stop videoarchive processes"
perms["perm_videoarchive_delete_video"] = "Can delete videoarchive videos"
perms["perm_videoarchive_export_video"] = "Can export videoarchive videos"

#
# ВНИМАНИЕ!!! 
# добавление любого пермишена подлежит согласованию
#


#
# def\s[a-zA-Z_]*\(request
#

PERMISSIONS = () # Created by next for
for perm in perms: PERMISSIONS += ((perm, perms[perm]),)

def create_groups():
    
    dict_all_perms = dict()
    for perm in perms: dict_all_perms[perm] = Permission.objects.get(codename=perm)
    
        
    def get_perms(str_perms):
        return [dict_all_perms[str_perm] for str_perm in str_perms]
        
        
    models_all_perms = [Permission.objects.get(codename=perm) for perm in perms]
    
    group_superuser, create = Group.objects.get_or_create(name=_("group_superuser"))
    group_administrator, create = Group.objects.get_or_create(name=_("group_administrator"))
    group_moderator, create = Group.objects.get_or_create(name=_("group_moderator"))
    group_operator, create = Group.objects.get_or_create(name=_("group_operator"))
    group_security, create = Group.objects.get_or_create(name=_("group_security"))
    group_access_denied, create = Group.objects.get_or_create(name=_("group_access_denied"))
    
    # Set permissions for superuser
    group_superuser.permissions = models_all_perms 
    # Set permissions for other users
    group_administrator.permissions = get_perms(["perm_settings", "perm_monitoring", "perm_logs", "perm_lists", "perm_lists_edit", 
                                                 "perm_logs_sessions", "perm_logs_clear", "perm_logs_export", "perm_security", 
                                                 "perm_view", "perm_wizard", "perm_security_main", "perm_distortion", "perm_setup",
                                                 "perm_videoarchive", "perm_videoarchive_settings", "perm_videoarchive_analysis",
                                                 "perm_videoarchive_tasks", "perm_videoarchive_add_task", "perm_videoarchive_delete_task",  
                                                 "perm_videoarchive_processes", "perm_videoarchive_stop_process", "perm_videoarchive_delete_video",
                                                 "perm_videoarchive_export_video", "perm_videoarchive_journal", "perm_videoarchive_videos",
                                                 "perm_videoarchive_calendar"])
    group_moderator.permissions = get_perms(["perm_logs", "perm_lists", "perm_view", "perm_security_main", "perm_distortion",
                                             "perm_videoarchive", "perm_videoarchive_analysis", "perm_videoarchive_tasks", "perm_videoarchive_processes",
                                             "perm_videoarchive_journal", "perm_videoarchive_videos", "perm_videoarchive_add_task", "perm_videoarchive_delete_task",
                                             "perm_videoarchive_calendar", "perm_videoarchive_analysis", "perm_videoarchive_stop_process",
                                             "perm_videoarchive_export_video"])
    group_operator.permissions = get_perms(["perm_view", "perm_security_main"])
    group_security.permissions = get_perms(["perm_security"])
    group_access_denied.permissions = get_perms([])



