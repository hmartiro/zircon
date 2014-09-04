from django.conf import settings
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required

from zircon.datastores.influx import InfluxDatastore
# TODO get rid of this datastore, use client-side request

import json

try:
    zircon_config = settings.ZIRCON_CONFIG
    db_info = zircon_config.get('db_info', None)
    db_name = zircon_config.get('db_name', None)
    db = InfluxDatastore(db_info=db_info, db_name=db_name)
except AttributeError:
    print('[WARNING] No ZIRCON_CONFIG found in Django settings!')
    db = InfluxDatastore()


#@login_required
def home(request):

    signal_ids = db.list_signals()

    d = {
        'signal_ids': json.dumps(signal_ids)
    }

    return TemplateResponse(request, 'dashboard/index.html', context=d)
