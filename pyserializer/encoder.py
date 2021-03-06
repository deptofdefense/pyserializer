# =================================================================
#
# Work of the U.S. Department of Defense, Defense Digital Service.
# Released as open source under the MIT License.  See LICENSE file.
#
# =================================================================

import datetime
import decimal
import json
import ipaddress

import pandas as pd
import numpy as np


class Encoder(json.JSONEncoder):
    """
    Encoder extends the default JSON encoder to add support for new functions.
    """

    def __init__(self, **kwargs):
        formats = kwargs.pop("formats", {})
        self.decimal_format = formats.pop("decimal", "float")
        self.date_format = formats.pop("date", "%Y-%m-%d")
        self.datetime_format = formats.pop("datetime", "%Y-%m-%dT%H:%M:%S.%f%z")
        self.timestamp_format = formats.pop("timestamp", "%Y-%m-%dT%H:%M:%S.%f%z")
        return super(Encoder, self).__init__(**kwargs)

    def default(self, obj):

        if isinstance(obj, Exception):
            return str(obj)

        if isinstance(obj, decimal.Decimal):
            return str(obj) if self.decimal_format == "string" else float(obj)

        # timestamp comes before datetime, because a timestamp object is a subclass of datetime
        if isinstance(obj, pd.Timestamp):
            return obj.strftime(self.timestamp_format)

        # datetime comes before date, because a datetime object is a subclass of date
        if isinstance(obj, datetime.datetime):
            return obj.strftime(self.datetime_format)

        if isinstance(obj, datetime.date):
            return obj.strftime(self.date_format)

        if isinstance(obj, pd.DataFrame):
            return obj.to_dict('records')

        if isinstance(obj, np.integer):
            return int(obj)

        if isinstance(obj, np.floating):
            return float(obj)

        if isinstance(obj, np.ndarray):
            return obj.tolist()

        if isinstance(obj, (ipaddress.IPv4Network, ipaddress.IPv6Network)):
            return str(obj)

        return super(Encoder, self).default(obj)
