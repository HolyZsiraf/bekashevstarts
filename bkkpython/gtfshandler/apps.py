from importlib import import_module
from django.apps import AppConfig


class GtfshandlerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gtfshandler'
    initializedAlready = False
    def ready(self):
        print("started!!!!")
        return
        if not self.initializedAlready:
            hevDep = import_module('gtfshandler.models', 'HevDeparture')
            parser = import_module('gtfshandler.gtfsparser')
            parser.downloadAndUnzipGtfsPackage()
            hevDep.HevDeparture.objects.all().delete()
            parser.loadDeparturesToDatabase()
            self.initializedAlready = True