#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

import config_export
import export_funcs

from xml.etree.ElementTree import ElementTree, Element
from StringIO import StringIO

lst = os.listdir(config_export.tar_dir)
for l in lst:
    d = config_export.tar_dir+l
    if os.path.isfile(d): os.unlink(d)

# Обязательные данные
root = Element("info")
root.append(export_funcs.get_all_params(export_funcs.get_info('videoclient_camera'), "camera"))
root.append(export_funcs.get_balancer_params(export_funcs.get_info('videoclient_balancer'), "balancer"))
tree = ElementTree(root)

f = StringIO()
tree.write(f, 'UTF-8')

fl = open(config_export.fname, "w")
fl.write(str(f.getvalue()))
fl.close()

export_funcs.get_commands(config_export.commands_list, config_export.command_fname)

print "TarURL:\n"
export_funcs.tar_objects(config_export.tar_name, " ".join(list(config_export.required_paths)))
print export_funcs.get_url(config_export.tar_name, config_export.info_value["info.tar"])


# Получаем список опций
options = sys.argv
for i in range(1, len(options)):
    if options[i] in config_export.options_functions: config_export.options_functions[options[i]]()

