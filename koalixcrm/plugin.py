# -*- coding: utf-8 -*-
import sys

from django.conf import settings


class PluginProcessor(object):
    @staticmethod
    def converttorelativestring(pluginmodule, nameofinline):
        output = []
        if len(nameofinline) != 0:
            output.append(pluginmodule.__name__ + "." + nameofinline[0])
            return output
        else:
            return []

    @staticmethod
    def getAllPlugins():
        allpluginmodules = []
        for plugin in settings.KOALIXCRM_PLUGINS:
            __import__(plugin + ".admin")
            allpluginmodules.append(sys.modules[plugin + ".admin"])
        return allpluginmodules

    def getPluginAdditions(self, additionname):
        listofAdditions = []
        allpluginmodules = self.getAllPlugins()
        for pluginmodule in allpluginmodules:
            try:
                listofAdditions.extend(getattr(pluginmodule.KoalixcrmPluginInterface, additionname))
            except AttributeError:
                continue
        return listofAdditions