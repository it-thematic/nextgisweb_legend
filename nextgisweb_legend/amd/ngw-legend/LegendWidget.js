define([
    "dojo/_base/declare",
    "dojo/_base/lang",
    "dojo/Deferred",
    "dojo/when",
    "dijit/_TemplatedMixin",
    "dijit/_WidgetsInTemplateMixin",
    "dijit/layout/ContentPane",
    "@nextgisweb/pyramid/i18n!",
    "ngw-resource/serialize",
    // resource
    "dojo/text!./template/LegendWidget.hbs",
    // template
    "dojox/layout/TableContainer",
    "ngw-file-upload/Uploader"
], function (
    declare,
    lang,
    Deferred,
    when,
    _TemplatedMixin,
    _WidgetsInTemplateMixin,
    ContentPane,
    i18n,
    serialize,
    template
) {
    return declare([ContentPane, serialize.Mixin, _TemplatedMixin, _WidgetsInTemplateMixin], {
        templateString: i18n.renderTemplate(template),

        title: i18n.gettext("Legend"),
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