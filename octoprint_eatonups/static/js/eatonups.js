/*
 * View model for OctoPrint-EatonUPS
 *
 * Author: Kamel Makhloufi
 * License: AGPLv3
 */
$(function() {
    function EatonUPSViewModel(parameters) {
        var self = this;

        // assign the injected parameters, e.g.:
        // self.connectionViewModel = parameters[0];
        // self.settingsViewModel = parameters[1];

        self.upsPower = function(data) {
            console.log("yo");
            $.ajax({
                url: "/api/plugin/eatonups",
                type: "POST",
                dataType: "json",
                data: JSON.stringify({ 
                command: "power",
                    state: data
                }),
                contentType: "application/json"
            });
        }
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: EatonUPSViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: [ "connectionViewModel" ],
        // Elements to bind to, e.g. #settings_plugin_eatonups, #tab_plugin_eatonups, ...
        elements: [ "#connection_plugin_eatonups" ]
    });
});
