from nextgisweb.env import Component


class LegendComponent(Component):

    def configure(self):
        super(LegendComponent, self).configure()

    def initialize_db(self):
        super(LegendComponent, self).configure()

    def setup_pyramid(self, config):
        from . import view, api
        view.setup_pyramid(self, config)
        api.setup_pyramid(self, config)
