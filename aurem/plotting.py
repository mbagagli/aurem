import copy
import numpy as np
import logging
import matplotlib.pyplot as plt
plt.style.context('fivethirtyeight')


logger = logging.getLogger(__name__)


# =======================  Common

def _normalize_trace(workList, rangeVal=[-1, 1]):
    """Normalize array between 2 values

    This function normalize the trace between 2 numbers defined in input

    Inputs:
        workList (np.ndarray, list, tuple): input array to normalize
        rangeVal (list, tuple): min and max range of normalization

    Returns:
        worklist (np.ndarray, list, tuple): normalized input array.

    """
    minVal = min(workList)
    maxVal = max(workList)
    workList[:] = [((x - minVal) / (maxVal - minVal)) *
                   (rangeVal[1] - rangeVal[0]) for x in workList]
    workList = workList + rangeVal[0]
    return workList


# =======================  Main

def plot_rec(rec_obj,
             plot_ax=None,
             plot_cf=False,
             plot_pick=True,
             plot_additional_picks={},
             normalize=True,
             axtitle="AUREM picker: REC",
             show=False):
    """Plotting function for REC auto-regressive method.

    Args:
        rec_obj (aurem.picker.REC): REC picker object

    Optionals:
        plot_ax (matplotlib.pyplot.axes): handle of the axes where plot
        plot_cf (bool): either plot or not the CF of REC
        plot_pick (bool): either plot or not the final REC-pick
        plot_additional_picks (dict): key-args dict with
            'name': UTCDateTime scheme.
        normalize (bool): if True normalize between -1,1 the trace and
            from 0 to 1 the (optional) REC-CF.
        axtitle (str): axis title
        show (bool): if True plot on screen the resulting figure

    Returns:
        inax (matplotlib.pyplot.axes): handle of the active axis

    """
    if not plot_ax:
        inax = plt.axes()
    else:
        inax = plot_ax

    # Creating time vector and trace data
    newTrace = rec_obj.wt.copy()
    tv = newTrace.times()
    td = newTrace.data

    if normalize:
        td = _normalize_trace(td, rangeVal=[-1, 1])

    # -------------------------- Carachteristic function
    if plot_cf:
        if rec_obj.recfn.any():
            _wa = copy.deepcopy(rec_obj.recfn)
            # GoingToC: replace INF at the start and end with adiacent
            #           values for plotting reasons
            _wa[0] = _wa[1]
            _wa[-1] = _wa[-2]

            if normalize:
                _tmp = _normalize_trace(_wa, rangeVal=[0, 1])
            #
            zeropad = len(td) - len(_tmp)
            #
            inax.plot(tv, np.pad(_tmp, (0, zeropad), mode='constant',
                                 constant_values=(np.nan,)),
                      color="teal",
                      linewidth=1,
                      linestyle=':',
                      label="CF")
        else:
            logger.warning("Missing REC CF, skipping ...")

    # -------------------------- Additional Picks
    my_color_list_add = ['lime',
                         'forestgreen',
                         'limegreen',
                         'darkgreen']
    col_idx = 0
    if plot_additional_picks and isinstance(plot_additional_picks, dict):
        for _kk, _pp in plot_additional_picks.items():
            inax.axvline(_pp - rec_obj.wt.stats.starttime,
                         color=my_color_list_add[col_idx],
                         linewidth=1.5,
                         label=_kk)
            col_idx += 1

    # -------------------------- Final Pick
    if plot_pick:
        if rec_obj.pick:
            inax.axvline(rec_obj.pick - rec_obj.wt.stats.starttime,
                         color="teal",
                         linestyle="-",
                         linewidth=2,
                         label="PICK")
        else:
            logger.warning("Missing REC PICK, skipping ...")

    # -------------------------- Plot trace
    inax.plot(tv, td, "k", label="trace")
    inax.set_xlabel("time (s)")
    inax.set_ylabel("counts")
    inax.legend(loc='lower left')
    inax.set_title(axtitle, {'fontsize': 16, 'fontweight': 'bold'})

    if show:
        plt.tight_layout()
        plt.show()
    #
    return inax


def plot_aic(aic_obj,
             plot_ax=None,
             plot_cf=False,
             plot_pick=True,
             plot_additional_picks={},
             normalize=True,
             axtitle="AUREM picker: AIC",
             show=False):
    """Plotting function for AIC auto-regressive method.

    Args:
        aic_obj (aurem.picker.AIC): AIC picker object

    Optionals:
        plot_ax (matplotlib.pyplot.axes): handle of the axes where plot
        plot_cf (bool): either plot or not the CF of AIC
        plot_pick (bool): either plot or not the final AIC-pick
        plot_additional_picks (dict): key-args dict with
            'name': UTCDateTime scheme.
        normalize (bool): if True normalize between -1,1 the trace and
            from 0 to 1 the (optional) AIC-CF.
        axtitle (str): axis title
        show (bool): if True plot on screen the resulting figure

    Returns:
        inax (matplotlib.pyplot.axes): handle of the active axis

    """

    if not plot_ax:
        inax = plt.axes()
    else:
        inax = plot_ax

    # Creating time vector and trace data
    newTrace = aic_obj.wt.copy()
    tv = newTrace.times()
    td = newTrace.data

    if normalize:
        td = _normalize_trace(td, rangeVal=[-1, 1])

    # -------------------------- Carachteristic function
    if plot_cf:
        if aic_obj.aicfn.any():
            _wa = copy.deepcopy(aic_obj.aicfn)
            # GoingToC: replace INF at the start and end with adiacent
            #           values for plotting reasons
            _wa[0] = _wa[1]
            _wa[-1] = _wa[-2]

            if normalize:
                _tmp = _normalize_trace(_wa, rangeVal=[0, 1])
            #
            zeropad = len(td) - len(_tmp)
            #
            inax.plot(tv, np.pad(_tmp, (0, zeropad), mode='constant',
                                 constant_values=(np.nan,)),
                      color="teal",
                      linewidth=1,
                      linestyle=':',
                      label="CF")
        else:
            logger.warning("Missing AIC CF, skipping ...")

    # -------------------------- Additional Picks
    my_color_list_add = ['lime',
                         'forestgreen',
                         'limegreen',
                         'darkgreen']
    col_idx = 0
    if plot_additional_picks and isinstance(plot_additional_picks, dict):
        for _kk, _pp in plot_additional_picks.items():
            inax.axvline(_pp - aic_obj.wt.stats.starttime,
                         color=my_color_list_add[col_idx],
                         linewidth=1.5,
                         label=_kk)
            col_idx += 1

    # -------------------------- Final Pick
    if plot_pick:
        if aic_obj.pick:
            inax.axvline(aic_obj.pick - aic_obj.wt.stats.starttime,
                         color="teal",
                         linestyle="-",
                         linewidth=2,
                         label="PICK")
        else:
            logger.warning("Missing AIC PICK, skipping ...")

    # -------------------------- Plot trace
    inax.plot(tv, td, "k", label="trace")
    inax.set_xlabel("time (s)")
    inax.set_ylabel("counts")
    inax.legend(loc='lower left')
    inax.set_title(axtitle, {'fontsize': 16, 'fontweight': 'bold'})

    if show:
        plt.tight_layout()
        plt.show()
    #
    return inax


# ================== TIPS
# To create a continuos discrete list of colors with matplotlib

# import matplotlib.cm as mplcm
# import matplotlib.colors as colors
#    NUM_COLORS = len(pickTime_UTC.keys()) - 2  # MB: - mean and  -median
#    cm = plt.get_cmap('gist_rainbow')
#    cNorm = colors.Normalize(vmin=0, vmax=NUM_COLORS-1)
#    scalarMap = mplcm.ScalarMappable(norm=cNorm, cmap=cm)
#    inax.set_prop_cycle(color=[scalarMap.to_rgba(i)
#                               for i in range(NUM_COLORS)])
