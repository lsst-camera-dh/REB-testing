"""
Module to access CCS trending database via the RESTful interface.
"""
import xml.dom.minidom as minidom
import time
import datetime
import requests
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mds

__all__ = ['Channels', 'RestUrl', 'TimeAxis', 'TrendingPlotter',
           'TrendingHistory', 'TrendingPoint']


def date_time(msec):
    "Convert milliseconds since epoch to a datetime object."
    return datetime.datetime.fromtimestamp(msec/1e3)


class Channels(object):
    "Class to read the channels available from the CCS database"
    def __init__(self, host='tid-pc93482'):
        url = 'http://%s:8080/rest/data/dataserver/listchannels' % host
        doc = minidom.parseString(requests.get(url).text)
        self.channels = dict()
        for channel in doc.getElementsByTagName('datachannel'):
            path_elements = channel.getElementsByTagName('pathelement')
            subsystem = str(path_elements[0].childNodes[0].data)
            quantity = str(path_elements[1].childNodes[0].data)
            self.channels['/'.join((subsystem, quantity))] \
                = int(channel.getElementsByTagName('id')[0].childNodes[0].data)

    def __call__(self, subsystem, quantity):
        """
        Access to the channel id.

        Parameters
        ----------
        subsystem : str
            The CCS subsystem name, e.g., 'ccs-reb5-0'
        quantity : str
            The trending quantity name, e.g., 'REB0.Temp1'

        Returns
        -------
        int
            The channel id number.
        """
        return self.channels['/'.join((subsystem, quantity))]


class RestUrl(object):
    """
    The url of the RESTful interface server.
    """
    def __init__(self, subsystem, host='tid-pc93482', time_axis=None,
                 raw=False):
        self.subsystem = subsystem
        self.host = host
        self.channels = Channels(host=host)
        self.time_axis = time_axis
        self.raw = raw

    def __call__(self, quantity):
        id_ = self.channels(self.subsystem, quantity)
        url = 'http://%s:8080/rest/data/dataserver/data/%i' % (self.host, id_)
        if self.raw:
            url += '?flavor=raw'
        if self.time_axis is not None:
            url = self.time_axis.append_axis_info(url)
        return url

class TimeAxis(object):
    """
    Abstraction of the time axis information for CCS trending plots.
    """
    def __init__(self, dt=24., start=None, end=None, nbins=None):
        """
        Constructor for time intervals.

        Parameters
        ----------
        dt : float, optional
            Duration of time axis in hours.  Ignored if both start and
            end are given.  Default: 24.
        start : str, optional
            Start of time interval. ISO-8601 format, e.g., "2017-01-21T09:58:01"
        end : str, optional
            End of time interval. ISO-8601 format.
        nbins : int, optional
            Number of bins for time axis.  Automatically chosen by RESTful
            server if not given.
        """
        self.start = self._convert_iso_8601(start)
        self.end = self._convert_iso_8601(start)
        if self.start is None:
            if self.end is None:
                self.end = time.mktime(datetime.datetime.now().timetuple())
            self.start = self.end - dt*3600.
        elif self.end is None:
            self.end = self.start + dt*3600.
        self.nbins = nbins

    def append_axis_info(self, url):
        """Append time axis info to the REST url."""
        tokens = ['t1=%i' % (self.start*1e3), 't2=%i' % (self.end*1e3)]
        if self.nbins is not None:
            tokens.append('n=%i' % self.nbins)
        axis_info = '&'.join(tokens)
        if url.find('flavor') != -1:
            result = url + '&' + axis_info
        else:
            result = url + '?' + axis_info
        return result

    @staticmethod
    def _convert_iso_8601(iso_date):
        "Convert ISO-8601 formatted string to seconds since epoch"
        if iso_date is None:
            return None
        dt = datetime.datetime.strptime(iso_date, '%Y-%m-%dT%H:%M:%S')
        return time.mktime(dt.timetuple())


class TrendingPlotter(object):
    def __init__(self, subsystem, host, time_axis=None):
        self.subsystem = subsystem
        self.host = host
        self.rest_url = RestUrl(subsystem, host=host, time_axis=time_axis)

    def plot(self, quantities):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        for quantity in quantities:
            history = TrendingHistory(self.rest_url(quantity))
            ax.errorbar(mds.date2num(history.x_values), history.y_values,
                        yerr=history.y_errors, fmt='.', label=quantity)
        plt.legend()
        frame = plt.gca()
        frame.xaxis.set_major_formatter(mds.DateFormatter('%y-%m-%d\n%H:%M:%S'))
        return fig


class TrendingHistory(object):
    def __init__(self, url):
        doc = minidom.parseString(requests.get(url).text)
        self.history = [TrendingPoint(x) for x in
                        doc.getElementsByTagName('trendingdata')]
        try:
            self.x_axis_name = self.history[0].x_axis_name
        except IndexError:
            pass
        self._x_values = ()
        self._x_errors = ()
        self._y_values = ()
        self._y_errors = ()

    @property
    def x_values(self):
        if len(self._x_values) == 0:
            self._x_values = np.array([pt.x_value for pt in self.history])
        return self._x_values

    @property
    def x_errors(self):
        if len(self._x_errors) == 0:
            self._x_errors = np.array([pt.x_error for pt in self.history])
        return self._x_errors

    @property
    def y_values(self):
        if len(self._y_values) == 0:
            self._y_values = np.array([pt.value for pt in self.history])
        return self._y_values

    @property
    def y_errors(self):
        if len(self._y_errors) == 0:
            self._y_errors = np.array([pt.rms for pt in self.history])
        return self._y_errors


class TrendingPoint(object):
    def __init__(self, element):
        datavalues = element.getElementsByTagName('datavalue')
        self.__dict__.update(dict([(x.getAttribute('name'),
                                    float(x.getAttribute('value')))
                                   for x in datavalues]))
        axisvalue = element.getElementsByTagName('axisvalue')[0]
        self.x_axis_name = axisvalue.getAttribute('name')
        if self.x_axis_name == 'time':
            convert = date_time
        else:
            convert = lambda x: x
        self.x_value = convert(float(axisvalue.getAttribute('value')))
        self.x_error = (float(axisvalue.getAttribute('upperedge')) -
                        float(axisvalue.getAttribute('loweredge')))/2e3


if __name__ == '__main__':
    plt.ion()
    host = 'tid-pc93482'
    subsystem = 'ccs-reb5-0'
    time_axis = TimeAxis(dt=3, nbins=10)
    quantities = ('REB0.Temp1', 'REB0.Temp2', 'REB0.Temp3')

    rest_url = RestUrl(subsystem, host=host, time_axis=time_axis)
    for quantity in quantities:
        url = rest_url(quantity)

    foo = TrendingHistory(url)
    print foo.x_values, foo.y_values

#    plotter = TrendingPlotter(subsystem, host, time_axis=time_axis)
#    plotter.plot(quantities)
