from grappelli.dashboard import modules, Dashboard

class CustomDashboard(Dashboard):
    def init_with_context(self, context):
        self.children.append(modules.ModelList(
            title='Gestión de Modelos',
            models=['clients.models.*'],
        ))
        self.children.append(modules.LinkList(
            title='Enlaces Útiles',
            children=[
                {'title': 'Google', 'url': 'https://www.google.com/'},
            ],
        ))
