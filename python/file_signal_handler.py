"""
Module to support signals to harnessed jobs sent via the file system.
"""
from __future__ import absolute_import, print_function, division
import os
import time

class FileSignalHandlerException(RuntimeError):
    pass

class FileSignalHandler(object):
    """
    File signal handler class.

    Attributes
    ----------
    signal_file : str
        Path of the signal file.  It must be of the form
        <dirname>/<filename>, and <dirname> must exist.
    """
    def __init__(self, signal_file=None):
        """
        Constructor.

        Parameters
        ----------
        signal_file : str, optional
            Path of the signal file.  It must be of the form
            <dirname>/<filename>, and <dirname> must exist.
            If None, then it is set to '/tmp/hj_signal_<job_id>.txt'

        Raises
        ------
        ValueError :
            Raised if the directory to contain the signal file does not
            exist.

        Notes
        -----
            Since signals are ideally supposed to be transient events,
            if the signal file already exists, this constructor will
            delete it and carry on.
        """
        if signal_file is None:
            signal_file \
                = os.path.join('/tmp',
                               'hj_signal_%s.txt' % os.environ['LCATR_JOB_ID'])
        # Ensure a reasonable path (i.e., not in system root) is given
        # and that the directory exists.
        dirname = os.path.dirname(signal_file)
        if not os.path.isdir(dirname):
            raise ValueError('Directory %s does not exist' % dirname)
        # Delete the signal file if it already exists.
        if os.path.isfile(signal_file):
            os.remove(signal_file)
        self.signal_file = signal_file

    def wait(self, wait_interval, poll_interval=30):
        """
        Wait for a specified time, polling for the signal file at
        regular intervals.

        Parameters
        ----------
        wait_interval : float
            Time to wait in seconds.
        poll_interval : float, optional
            Interval in seconds between successive polls for signal
            file.  Must be less than or equal to wait_interval.
            Default=30.

        Returns
        -------
        float
            Elapsed time in seconds.

        Raises
        ------
        FileSignalHandlerException
            If the signal file is detected while waiting.
        """
        num_loops = int(wait_interval/poll_interval)
        if num_loops < 1:
            raise ValueError("num_loops computed to be < 1 for int(%s/%s)"
                             % (wait_interval, poll_interval))
        slop = wait_interval - num_loops*poll_interval
        i = 0
        for i in range(num_loops):
            time.sleep(poll_interval)
            if os.path.isfile(self.signal_file):
                os.remove(self.signal_file)
                raise FileSignalHandlerException("signal file %s found"
                                                 % self.signal_file)
        time.sleep(slop)
        return (i+1)*poll_interval + slop

    def send_file_signal(self):
        "Send the file signal by touching self.signal_file"
        # See http://stackoverflow.com/questions/1158076/implement-touch-using-python
        with open(self.signal_file, 'a'):
            os.utime(self.signal_file, None)

if __name__ == '__main__':
    sighandler = FileSignalHandler('./foo.txt')
    print("elapsed time: %s s" % sighandler.wait(20.452, 10))
