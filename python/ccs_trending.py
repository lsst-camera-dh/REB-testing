import xml.dom.minidom as minidom
import datetime
import requests
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
plt.ion()

def date_time(msec):
    "Convert milliseconds since epoch to a datetime object."
    return datetime.datetime.fromtimestamp(msec/1e3)


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


class Channels(object):
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
        return self.channels['/'.join((subsystem, quantity))]


class RestUrl(object):
    def __init__(self, subsystem, host='tid-pc93482'):
        self.subsystem = subsystem
        self.host = host
        self.channels = Channels(host=host)

    def __call__(self, quantity):
        channel_id = self.channels(self.subsystem, quantity)
        return 'http://%s:8080/rest/data/dataserver/data/%i' \
            % (self.host, channel_id)


if __name__ == '__main__':
    host = 'tid-pc93482'
    subsystem = 'ccs-reb5-0'
    rest_url = RestUrl(subsystem, host=host)
    quantities = ('REB0.Temp1', 'REB0.Temp2', 'REB0.Temp3')
    my_channels = Channels()

    for quantity in quantities:
        history = TrendingHistory(rest_url(quantity))
        print history.x_values, history.y_values


#    foo = TrendingHistory(url)
#
#    fig = plt.figure()
#    ax = fig.add_subplot(1, 1, 1)
#    ax.errorbar(mdates.date2num(foo.x_values), foo.y_values,
#                yerr=foo.y_errors, fmt='.')
##    axis_range = list(plt.axis())
##    axis_range[2] = 0
##    plt.axis(axis_range)
#    frame = plt.gca()
#    frame.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d\n%H:%M:%S'))
