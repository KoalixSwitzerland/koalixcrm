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
            temp = __import__(plugin + ".admin")
            allpluginmodules.append(sys.modules[plugin + ".admin"]);
        return allpluginmodules

    @staticmethod
    def resolve_name(name, package, level):
        """Return the absolute name of the module to be imported."""
        if not hasattr(package, 'rindex'):
            raise ValueError("'package' not set to a string")
        dot = len(package)
        for x in xrange(level, 1, -1):
            try:
                dot = package.rindex('.', 0, dot)
            except ValueError:
                raise ValueError("attempted relative import beyond top-level "
                                 "package")
        return "%s.%s" % (package[:dot], name)

    @staticmethod
    def import_module(name, package=None):
        """Import a module.

        The 'package' argument is required when performing a relative import. It
        specifies the package to use as the anchor point from which to resolve the
        relative import to an absolute import.

        """
        if name.startswith('.'):
            if not package:
                raise TypeError("relative imports require the 'package' argument")
            level = 0
            for character in name:
                if character != '.':
                    break
                    level += 1
            name = resolve_name(name[level:], package, level)
        __import__(name)
        return sys.modules[name]

    def getPluginAdditions(self, additionname):
        listofAdditions = []
        allpluginmodules = self.getAllPlugins()
        for pluginmodule in allpluginmodules:
            try:
                listofAdditions.extend(getattr(pluginmodule.KoalixcrmPluginInterface, additionname))
            except AttributeError:
                continue
        return listofAdditions