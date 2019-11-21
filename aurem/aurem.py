import logging
#
import numpy as np
import plotting
#
from obspy import UTCDateTime
from obspy.core.trace import Trace
from obspy.core.stream import Stream

logger = logging.getLogger(__name__)


class REC(object):
    """ This class initialize the Reciprocal-Based Picker algorithm.
        The picker takes in inputs only the obspy.Stream objects.
        Being completely automatic, only the channel parameter to
        specify the working trace is accepted.
    """
    def __init__(self, stream, channel="*Z"):
        self.st = stream.copy()
        self.wt = self.st.select(channel=channel)[0]
        #
        self.recfn = np.array([])
        self.idx = None
        self.pick = None

    def _calculate_rec_cf(self):
        """ Create the
        This method will return the Reciprocal-Based carachteristic
        function, that will be analyzed in the `work` method.

        Inputs:
            arr must be a  `numpy.ndarray`

        """
        N = self.wt.data.size
        arr = self.wt.data
        for ii in range(1, N):
            with np.errstate(divide='raise'):
                try:
                    val1 = ii/(np.var(arr[0:ii]))
                except FloatingPointError:  # if var==0 --> log is -inf
                    val1 = 0.00  # orig
                try:
                    print(np.var(arr[ii:]))
                    val2 = (N-ii)/np.var(arr[ii:])
                except FloatingPointError:  # if var==0 --> log is -inf
                    val2 = 0.00  # orig
                self.recfn = np.append(self.recfn, (-val1-val2))

    def work(self):
        """ This method will create the CF and return the index
            responding to the minimum of the CF.

        """
        self._calculate_rec_cf()
        # (ascending order min->max) OK!
        self.idx = sorted(range(len(self.recfn)),
                          key=lambda k: self.recfn[k])[0] + 1
        self.pick = (self.wt.stats.starttime +
                     self.wt.stats.delta * self.idx)

    def set_working_trace(self, channel):
        if not isinstance(channel, str):
            raise TypeError
        #
        self.wt = self.st.select(channel=channel)[0]

    def get_rec_function(self):
        if self.recfn:
            return self.recfn
        else:
            logger.warning("Missing EVALUATION FUNCTION! " +
                           "Run the work method first!")

    def get_pick_index(self):
        if self.idx:
            return self.idx
        else:
            logger.warning("Missing INDEX! " +
                           "Run the work method first!")

    def get_pick(self):
        if self.pick:
            if isinstance(self.pick, UTCDateTime):
                return self.pick
            else:
                raise TypeError
        else:
            logger.warning("Missing PICK! " +
                           "Run the work method first!")

    def plot(self):
        """ Wrapper around the plot_rec function in plot method

        """
        plotting.plot_rec(self,
                          plot_ax=None,
                          plot_cf=True,
                          plot_pick=True,
                          plot_additional_picks={},
                          normalize=True,
                          axtitle="REC picks",
                          show=True)




class AIC(object):
    """ This class initialize the Akaike Information Criteria Picker
        algorithm. The picker takes in inputs only the obspy.Stream
        objects. Being completely automatic, only the channel parameter
        to specify the working trace is accepted.
    """
    def __init__(self, stream, channel="*Z"):
        self.st = stream.copy()
        self.wt = self.st.select(channel=channel)[0]
        #
        self.aicfn = np.array([])
        self.idx = None
        self.pick = None

    def _calculate_aic_cf(self):
        """ Create the
        This method will return the Akaike Information Criteria
        carachteristic function, that will be analyzed in the `work`
        method.

        Inputs:
            arr must be a  `numpy.ndarray`

        """
        N = self.wt.data.size
        arr = self.wt.data
        for ii in range(1, N):
            with np.errstate(divide='raise'):
                try:
                    var1 = np.log(np.var(arr[0:ii]))
                except FloatingPointError:  # if var==0 --> log is -inf
                    var1 = 0.00
                #
                try:
                    var2 = np.log(np.var(arr[ii:]))
                except FloatingPointError:  # if var==0 --> log is -inf
                    var2 = 0.00
            #
            val1 = ii*var1
            val2 = (N-ii-1)*var2
            self.aicfn = np.append(self.aicfn, (val1+val2))

    def work(self):
        """ This method will create the CF and return the index
            responding to the minimum of the CF.

        """
        self._calculate_rec_cf()
        # (ascending order min->max) OK!
        self.idx = sorted(range(len(self.aicfn)),
                          key=lambda k: self.aicfn[k])[0] + 1
        self.pick = (self.wt.stats.starttime +
                     self.wt.stats.delta * self.idx)

    def set_working_trace(self, channel):
        if not isinstance(channel, str):
            raise TypeError
        #
        self.wt = self.st.select(channel=channel)[0]

    def get_rec_function(self):
        if self.aicfn:
            return self.aicfn
        else:
            logger.warning("Missing EVALUATION FUNCTION! " +
                           "Run the work method first!")

    def get_pick_index(self):
        if self.idx:
            return self.idx
        else:
            logger.warning("Missing INDEX! " +
                           "Run the work method first!")

    def get_pick(self):
        if self.pick:
            if isinstance(self.pick, UTCDateTime):
                return self.pick
            else:
                raise TypeError
        else:
            logger.warning("Missing PICK! " +
                           "Run the work method first!")

    def plot(self):
        """ Wrapper around the plot_rec function in plot method

        """
        plotting.plot_rec(self,
                          plot_ax=None,
                          plot_cf=True,
                          plot_pick=True,
                          plot_additional_picks={},
                          normalize=True,
                          axtitle="REC picks",
                          show=True)
