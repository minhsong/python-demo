# -*- coding: utf-8 -*-

import json
import time
from datetime import date, datetime

from sqlalchemy.ext.declarative import DeclarativeMeta
from app import log
LOG = log.get_logger()

def new_alchemy_encoder():
    # http://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json
    _visited_objs = []

    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj):# pylint: disable=E0202
            if isinstance(obj.__class__, DeclarativeMeta):
                # don't re-visit self
                if obj in _visited_objs:
                    return None
                _visited_objs.append(obj)

                # an SQLAlchemy class
                fields = {}
                for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata' and x !='FIELDS']:
                    fields[field] = obj.__getattribute__(field)
                    if isinstance(fields[field], (datetime,date)):
                        fields[field] = int(time.mktime(fields[field].timetuple()))
                # a json-encodable dict
                LOG.debug(fields)
                return fields

            return json.JSONEncoder.default(self, obj)
    return AlchemyEncoder


def passby(data):
    return data


def datetime_to_timestamp(date):
    if isinstance(date, (datetime,date)):
        return int(time.mktime(date.timetuple()))
    else:
        return None
