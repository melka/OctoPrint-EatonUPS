# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
import flask
import os

class EatonUPSPlugin(octoprint.plugin.SettingsPlugin,
                     octoprint.plugin.AssetPlugin,
                     octoprint.plugin.TemplatePlugin,
					 octoprint.plugin.SimpleApiPlugin):

	##~~ SettingsPlugin mixin

	def get_settings_defaults(self):
		return dict(
			ups_name="eaton@localhost",
			ups_user="admin",
			ups_pass="password",
			ups_outlet="1"
		)

	def on_after_startup(self):
		self._logger.info("Eaton UPS plugin started")

	##~~ ApiPlugin mixin

	def get_api_commands(self):
		return dict(
			power=["state"]
        )
	
	def on_api_command(self, command, data):
		if command == "power":
			upsName = self._settings.get(["ups_name"])
			upsUser = self._settings.get(["ups_user"])
			upsPass = self._settings.get(["ups_pass"])
			upsOutlet = self._settings.get_int(["ups_outlet"])
			state = data["state"]
			if state == "off" or state == "on":
				shellCommand = "upscmd -u {upsUser} -p {upsPass} {upsName} outlet.{upsOutlet}.load.{state}".format(**locals())
				self._logger.info(shellCommand)
				os.system(shellCommand)
			else :
				self._logger.info("invalid state, ignoring")

	def on_api_get(self, request):
		return flask.jsonify(state="api started")

	##~~ AssetPlugin mixin

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/eatonups.js"]
		)

	def get_template_configs(self):
		return [
			dict(type="sidebar", custom_bindings=False),
			dict(type="settings", custom_bindings=False)
		]

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
		# for details.
		return dict(
			eatonups=dict(
				displayName="Eatonups Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="melka",
				repo="OctoPrint-EatonUPS",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/melka/OctoPrint-EatonUPS/archive/{target_version}.zip"
			)
		)


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Eaton UPS Plugin"
__plugin_description__ = "Controlling an Eaton UPS via nut inside octoprint"

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
#__plugin_pythoncompat__ = ">=2.7,<3" # only python 2
#__plugin_pythoncompat__ = ">=3,<4" # only python 3
#__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = EatonUPSPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

