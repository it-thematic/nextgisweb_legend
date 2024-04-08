define([
    "dojo/_base/declare",
    "dojo/_base/lang",
    "dojo/Deferred",
    "dojo/when",
    "dijit/_WidgetBase",
    "dijit/_TemplatedMixin",
    "dijit/_WidgetsInTemplateMixin",
    // resource
    "@nextgisweb/pyramid/i18n!",
    "ngw-resource/serialize",
    "dojo/text!./template/LegendWidget.hbs",
    // template
    "dijit/layout/ContentPane",
    "dojox/layout/TableContainer"
], function (
    declare,
    lang,
    Deferred,
    when,
    _WidgetBase,
    _TemplatedMixin,
    _WidgetsInTemplateMixin,
    i18n,
    serialize,
    template,
    ContentPane
) {
    return declare(
        [
            ContentPane,
            _WidgetBase, 
            _TemplatedMixin, 
            _WidgetsInTemplateMixin,
            serialize.Mixin, 
        ], {
        title: i18n.gettext("Legend"),
        templateString: i18n.renderTemplate(template),
        prefix: "legend_sprite",

        serializeInMixin: function (data) {
            var prefix = this.prefix,
                setObject = function (key, value) {
                    lang.setObject(prefix + "." + key, value, data);
                };

            setObject("description_file", this.dFileUpload.get("value"));
            setObject("image_file", this.iFileUpload.get("value"));
        },

        validateDataInMixin: function (errback) {
            var description = this.composite.operation === "create" ?
                this.dFileUpload.upload_promise !== undefined &&
                this.dFileUpload.upload_promise.isResolved() : true;

            var image = this.composite.operation === "create" ?
                this.iFileUpload.upload_promise !== undefined &&
                this.iFileUpload.upload_promise.isResolved() : true;

            return description && image;
        }

    });
});