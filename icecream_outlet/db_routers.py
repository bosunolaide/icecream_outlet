
class AnalyticsRouter:
    route_app_labels = {"analytics"}

    def db_for_read(self, model, **hints):
        return "analytics" if model._meta.app_label in self.route_app_labels else "default"

    def db_for_write(self, model, **hints):
        return "analytics" if model._meta.app_label in self.route_app_labels else "default"

    def allow_migrate(self, db, app_label=None, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == "analytics"
        return db == "default"
