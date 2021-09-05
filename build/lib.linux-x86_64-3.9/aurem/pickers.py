import logging
import numpy as np
import pathlib
import ctypes as C
import copy
from obspy import UTCDateTime
#
from aurem import plotting as AUPL

logger = logging.getLogger(__name__)


# -------------------------------------------  Load and Setup C library
MODULEPATH = pathlib.Path(__file__).parent.absolute()

libname = tuple(MODULEPATH.glob("src/aurem_clib.*.so"))[0]
myclib = C.CDLL(libname)

# AIC
myclib.aicp.restype = C.c_int
myclib.aicp.argtypes = [np.ctypeslib.ndpointer(
                                        dtype=np.float32, ndim=1,
                                        flags='C_CONTIGUOUS'), C.c_int,
                        # OUT
                        np.ctypeslib.ndpointer(
                                        dtype=np.float32, ndim=1,
                                        flags='C_CONTIGUOUS'),
                        C.POINTER(C.c_int)]

# REC
myclib.recp.restype = C.c_int
myclib.recp.argtypes = [np.ctypeslib.ndpointer(
                                        dtype=np.float32, ndim=1,
                                        flags='C_CONTIGUOUS'), C.c_int,
                        # OUT
                        np.ctypeslib.ndpointer(
                                        dtype=np.float32, ndim=1,
                                        flags='C_CONTIGUOUS'),
                        C.POINTER(C.c_int)]
# ---------------------------------------------------------------------


class REC(object):
    """ Initialize the Reciprocal-Based picker class.

    The picker takes in inputs only the obspy.Stream objects.
    Being completely automatic, only the channel parameter to
    specify the working trace is accepted.

    For an exhaustive description of the picker's parameters the
    reader is referred to the reference paper.

    Args:
        stream (obspy.Stream): working Stream containing the working
            traces

    Optional:
        querykey (str): the following key-value parameters will be
            used to query the Stream at class initialization. Use the
            class method `set_working_trace` before running the work
            method.

    Note:
        If no query key-args given, the class will set the
        working trace as the 1st stream-trace !!!

    References:
        Ramin Madarshahian, Paul Ziehl, and Michael D. Todd (2020),
            Bayesian Estimation of Acoustic Emission Arrival Times for
            Source Localization.
            DOI: https://doi.org/10.1007/978-3-030-12075-7_13

    """
    def __init__(self, stream, **streamselect):
        self.wt = None  # just to define variable --> set_working_trace
        self.st = stream.copy()
        self.set_working_trace(**streamselect)
        #
        self.recfn = None
        self.idx = None
        self.pick = None

    def work(self):
        """ Core method ruling the picking workflow

        This method will create the CF and store pick index and UTC time

        Note:
            Now the CF's calcultation of CF and index extraction are
            contained in a faster C routine

        """
        if self.wt:
            pminidx = C.c_int()
            tmparr = np.ascontiguousarray(self.wt.data, np.float32)
            self.recfn = np.zeros(self.wt.data.size - 1,
                                  dtype=np.float32, order="C")
            ret = myclib.recp(tmparr, self.wt.data.size,
                              self.recfn, C.byref(pminidx))
            if ret != 0:
                raise MemoryError("Something wrong with REC picker C-routine")
            #
            self.idx = pminidx.value
            if self.idx != 0 and isinstance(self.idx, int):
                # pick found
                logger.debug("REC found pick")
                self.pick = (self.wt.stats.starttime +
                             self.wt.stats.delta * self.idx)
            else:
                # if idx == 0, it means inside C routine it didn't pick
                logger.debug("REC didn't found pick")
                self.pick = None
        else:
            raise AttributeError("Missing working trace. Use the class "
                                 "`set_working_trace` mothod first!")

    def set_working_trace(self, **streamselect):
        """ Select the trace from the class obspy.Stream

        The optional query parameters are the same supported by the
        obspy.Stream.selection() method

        Note:
            If no query key-args given, the class will set the
            working trace as the 1st stream-trace !!!

        """
        if streamselect and not isinstance(streamselect, dict):
            raise TypeError("Please specify stream select key-args query!")
        #
        self.wt = self.st.select(**streamselect)[0]

    def get_rec_function(self, mode="real"):
        """ Return the REC charachteristic function.

        Utility function to return aic function for either

        Optional:
            mode (str): either "real" or "plot". If "real", the original
                CF is returned. If plot option, the method return a
                deepcopy of the original CF. The "plot" method is
                indicated for custom plots.

        """
        if isinstance(self.recfn, np.ndarray) and self.recfn.size > 0:
            if mode.lower() == 'real':
                return self.recfn
            elif mode.lower() == 'plot':
                _wa = copy.deepcopy(self.recfn)
                # GoingToC: replace INF at the start and end with
                #           adiacent values for plotting reasons
                _wa[0] = _wa[1]
                _wa[-1] = _wa[-2]
                return _wa
        else:
            logger.warning("Missing CF FUNCTION! " +
                           "Run the work method first!")

    def get_pick_index(self):
        """ Return the pick-sample index

        Returns:
            idx (int): index of the pick

        """
        if self.idx:
            return self.idx
        else:
            logger.warning("Missing INDEX! " +
                           "Run the work method first!")

    def get_pick(self):
        """ Return the pick-UTC time

        Returns:
            pick (obspy.UTCDateTime): UTC time of the pick

        """
        if self.pick:
            if isinstance(self.pick, UTCDateTime):
                return self.pick
            else:
                raise TypeError
        else:
            logger.warning("Missing PICK! " +
                           "Run the work method first!")

    def plot(self):
        """ Wrapper around the plot_rec function.

        This method will quickly produce a plot with CF and picks
        For different type of plots, please use the plotting.plot_rec
        module instead.

        Returns:
            ax (matplotlib.pyplot.axes): axis object of the plot

        """
        ax = AUPL.plot_rec(self,
                           plot_ax=None,
                           plot_cf=True,
                           plot_pick=True,
                           plot_additional_picks={},
                           normalize=True,
                           axtitle="REC picks",
                           show=True)
        return ax


class AIC(object):
    """ Initialize the Akaike-Information-Criteria picker class.

    The picker takes in inputs only the obspy.Stream objects.
    Being completely automatic, only the channel parameter to
    specify the working trace is accepted.

    For an exhaustive description of the picker's parameters the
    reader is referred to the reference paper.

    Args:
        stream (obspy.Stream): working Stream containing the working
            traces

    Optional:
        querykey (str): the following key-value parameters will be
            used to query the Stream at class initialization. Use the
            class method `set_working_trace` before running the work
            method.

    Note:
        If no query key-args given, the class will set the
        working trace as the 1st stream-trace !!!

    References:
        Maeda, Naoki. 1985. “A Method for Reading and Checking Phase
            Time in Auto-Processing System of Seismic Wave Data.”
            Zisin (Journal of the Seismological Society of Japan.
            2nd Ser.) 38 (3): 365–79.
            DOI: https://doi.org/10.4294/zisin1948.38.3_365

    """
    def __init__(self, stream, **streamselect):
        self.wt = None  # just to define variable --> set_working_trace
        self.st = stream.copy()
        self.set_working_trace(**streamselect)
        #
        self.aicfn = None
        self.idx = None
        self.pick = None

    def work(self):
        """ Core method ruling the picking workflow

        This method will create the CF and store pick index and UTC time

        Note:
            Now the CF's calcultation of CF and index extraction are
            contained in a faster C routine

        """
        if self.wt:
            pminidx = C.c_int()
            tmparr = np.ascontiguousarray(self.wt.data, np.float32)
            self.aicfn = np.zeros(self.wt.data.size - 1,
                                  dtype=np.float32, order="C")
            ret = myclib.aicp(tmparr, self.wt.data.size,
                              self.aicfn, C.byref(pminidx))
            if ret != 0:
                raise MemoryError("Something wrong with AIC picker C-routine")
            #
            self.idx = pminidx.value
            if self.idx != 0 and isinstance(self.idx, int):
                # pick found
                logger.debug("AIC found pick")
                self.pick = (self.wt.stats.starttime +
                             self.wt.stats.delta * self.idx)
            else:
                # if idx == 0, it means inside C routine it didn't pick
                logger.debug("AIC didn't found pick")
                self.pick = None
        else:
            raise AttributeError("Missing working trace. Use the class "
                                 "`set_working_trace` mothod first!")

    def set_working_trace(self, **streamselect):
        """ Select the trace from the class obspy.Stream

        The optional query parameters are the same supported by the
        obspy.Stream.selection() method

        Note:
            After the selection-query stace of class stream. It will
            select the first trace of filtered stream

        """
        if streamselect and not isinstance(streamselect, dict):
            raise TypeError("Please specify stream select key-args query!")
        #
        self.wt = self.st.select(**streamselect)[0]

    def get_aic_function(self, mode="real"):
        """ Return the AIC charachteristic function.

        Utility function to return aic function for either

        Optional:
            mode (str): either "real" or "plot". If "real", the original
                CF is returned. If plot option, the method return a
                deepcopy of the original CF. The "plot" method is
                indicated for custom plots.

        Note:
            If no query key-args given, the class will set the
            working trace as the 1st stream-trace !!!

        """
        if isinstance(self.aicfn, np.ndarray) and self.aicfn.size > 0:
            if mode.lower() == 'real':
                return self.aicfn
            elif mode.lower() == 'plot':
                _wa = copy.deepcopy(self.aicfn)
                # GoingToC: replace INF at the start and end with
                #           adiacent values for plotting reasons
                _wa[0] = _wa[1]
                _wa[-1] = _wa[-2]
                return _wa
            raise ValueError("Mode must be either 'real' or 'plot'")
        else:
            raise AttributeError("Missing CF FUNCTION! " +
                                 "Run the work method first!")

    def get_pick_index(self):
        """ Return the pick-sample index

        Returns:
            idx (int): index of the pick

        """
        if self.idx is None:
            raise AttributeError("Missing INDEX! " +
                                 "Run the work method first!")
        #
        if isinstance(self.idx, int):
            return self.idx
        else:
            raise TypeError("INDEX is not an integer: %s" %
                            str(type(self.idx)))

    def get_pick(self):
        """ Return the pick-UTC time

        Returns:
            pick (obspy.UTCDateTime): UTC time of the pick

        """
        if self.idx is None:
            raise AttributeError("Missing PICK! " +
                                 "Run the work method first!")
        else:
            # At this stage, it can be already UTCDateTime or None.
            return self.pick

    def plot(self):
        """ Wrapper around the plot_aic function.

        This method will quickly produce a plot with CF and picks
        For different type of plots, please use the plotting.plot_rec
        module instead.

        Returns:
            ax (matplotlib.pyplot.axes): axis object of the plot

        """
        ax = AUPL.plot_aic(self,
                           plot_ax=None,
                           plot_cf=True,
                           plot_pick=True,
                           plot_additional_picks={},
                           normalize=True,
                           axtitle="AIC picks",
                           show=True)
        return ax
