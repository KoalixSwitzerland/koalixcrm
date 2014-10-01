# -*- coding: utf-8 -*-
import sys

from django.conf import settings


class PluginProcessor(object):
    @staticmethod
    def convert_to_relative_string(plugin_module, name_of_inline):
        output = []
        if len(name_of_inline) != 0:
            output.append(plugin_module.__name__ + "." + name_of_inline[0])
            return output
        else:
            return []

    @staticmethod
    def get_all_plugins():
        all_plugin_modules = []
        for plugin in settings.KOALIXCRM_PLUGINS:
            temp = __import__(plugin + ".admin")
            all_plugin_modules.append(sys.modules[plugin + ".admin"])
        return all_plugin_modules

    def get_plugin_additions(self, addition_name):
        list_of_additions = []
        all_plugin_modules = self.get_all_plugins()
        for plugin_module in all_plugin_modules:
            try:
                list_of_additions.extend(getattr(plugin_module.KoalixcrmPluginInterface, addition_name))
            except AttributeError:
                continue
        return list_of_additions

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

    def import_module(self, name, package=None):
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
            name = self.resolve_name(name[level:], package, level)
        __import__(name)
        return sys.modules[name]