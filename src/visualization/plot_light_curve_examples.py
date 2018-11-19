from functools import partial
from plotnine import *
from scipy.optimize import leastsq

import math
import os
import os.path

import numpy as np
import pandas as pd

def main():
    i_input_dir = "../../data/interim/lmc/curves/I"
    v_input_dir = "../../data/interim/lmc/curves/V"

    output_dir = "../../reports/figures/light_curve_examples"
    os.makedirs(output_dir, exist_ok=True)

    data_id_number = "00001"
    data_id = "OGLE-LMC-RRLYR-{}".format(data_id_number)

    bands = [
        ("i", i_input_dir),
        ("v", v_input_dir)
    ]

    # Get the period to use for the period folded light curves
    rrab_data_file = "../../data/interim/lmc/RRab.csv"
    rrab = pd.read_csv(rrab_data_file)

    period = rrab[rrab["id"] == data_id]["period"].iloc[0]

    for band, band_dir in bands:
        data_file = os.path.join(band_dir, data_id + ".csv")

        data = pd.read_csv(data_file)

        # Regular light curve
        plot_raw = ggplot(data, aes("time", "mag")) +\
                geom_point() +\
                scale_y_reverse() +\
                xlab("Time (MJD)") +\
                ylab("Magnitude (mag)") +\
                ggtitle("Light Curve - {} - {} band".format(data_id, band.upper())) +\
                theme(
                    figure_size=(9, 9),
                    text=element_text(size=16)
                )

        plot_filename = "light_curve_raw_{}.png".format(band)
        plot_file = os.path.join(output_dir, plot_filename)

        ggsave(plot_raw, plot_file)

        # Period folded light curve
        data["phase"] = data["time"] % period

        plot_folded = ggplot(data, aes("phase", "mag")) +\
                geom_point() +\
                scale_y_reverse() +\
                xlab("Phase") +\
                ylab("Magnitude (mag)") +\
                ggtitle("Folded Light Curve - {} - {} band".format(data_id, band.upper())) +\
                theme(
                    figure_size=(9, 9),
                    text=element_text(size=16)
                )

        plot_folded_filename = "light_curve_folded_{}.png".format(band)
        plot_folded_file = os.path.join(output_dir, plot_folded_filename)

        ggsave(plot_folded, plot_folded_file)

        # Fourier series fitted light curve
        fourier_order = 3
        fourier_coef = fourier_decomposition(data["phase"], data["mag"], fourier_order)

        data["fourier_fit"] = fourier_series(data["phase"], fourier_coef, fourier_order)

        plot_fourier = ggplot(data, aes("phase", "mag")) +\
                geom_point() +\
                geom_line(aes("phase", "fourier_fit"), color="blue", size=3) +\
                scale_y_reverse() +\
                xlab("Phase") +\
                ylab("Magnitude (mag)") +\
                ggtitle("Fourier Fitted Light Curve - {} - {} band".format(data_id, band.upper())) +\
                theme(
                    figure_size=(9, 9),
                    text=element_text(size=16)
                )

        plot_fourier_filename = "light_curve_fourier_{}.png".format(band)
        plot_fourier_file = os.path.join(output_dir, plot_fourier_filename)

        ggsave(plot_fourier, plot_fourier_file)

def fourier_decomposition(times, magnitudes, order):
    """
    Fits the given light curve to a cosine fourier series of the given order
    and returns the fit amplitude and phi weights. The coefficents are
    calculated using a least squares fit.

    The fourier series that is fit is the following:

    n = order
    f(time) = A_0 + sum([A_k * cos(2pi * k * time + phi_k) for k in range(1, n + 1)])

    The fourier coeeficients are returned in a list of the following form:

    [A_0, A_1, phi_1, A_2, phi_2, ...]

    Each of the A coefficients will be positive.

    The number of (time, magnitude) values provided must be greater than or
    equal to the order * 2 + 1. This is a requirement of the least squares
    function used for calculating the coefficients.

    Parameters
    ----------
    times : numpy.ndarray
        The light curve times.
    magnitudes : numpy.ndarray
        The light curve magnitudes.
    order : int
        The order of the fourier series to fit.

    Returns
    -------
    fourier_coef : numpy.ndarray
        The fit fourier coefficients.
    """
    num_examples = times.shape[0]
    num_coef = order * 2 + 1

    if num_coef > num_examples:
        raise Exception("Too few examples for the specified order. Number of examples must be at least order * 2 + 1. Required: %d, Actual: %d" % (num_coef, num_examples))

    initial_coef = np.ones(num_coef)

    cost_function = partial(fourier_series_cost, times, magnitudes, order)

    fitted_coef, success = leastsq(cost_function, initial_coef)

    final_coef = correct_coef(fitted_coef, order)

    return final_coef

def correct_coef(coef, order):
    """
    Corrects the amplitudes in the given fourier coefficients so that all of
    them are positive.

    This is done by taking the absolute value of all the negative amplitude
    coefficients and incrementing the corresponding phi weights by pi.

    Parameters
    ----------
    fourier_coef : numpy.ndarray
        The fit fourier coefficients.
    order : int
        The order of the fourier series to fit.

    Returns
    -------
    cor_fourier_coef : numpy.ndarray
        The corrected fit fourier coefficients.
    """
    coef = coef[:]
    for k in range(order):
        i = 2 * k + 1
        if coef[i] < 0.0:
            coef[i] = abs(coef[i])
            coef[i + 1] += math.pi

    return coef

def fourier_series_cost(times, magnitudes, order, coef):
    """
    Returns the error of the fourier series of the given order and coefficients
    in modeling the given light curve.

    Parameters
    ----------
    times : numpy.ndarray
        The light curve times.
    magnitudes : numpy.ndarray
        The light curve magnitudes.
    order : int
        The order of the fourier series to fit.
    fourier_coef : numpy.ndarray
        The fit fourier coefficients.

    Returns
    -------
    error : numpy.float64
        The error of the fourier series in modeling the curve.
    """
    return magnitudes - fourier_series(times, coef, order)

def fourier_series(times, coef, order):
    """
    Returns the magnitude values given by applying the fourier series described
    by the given order and coefficients to the given time values.

    Parameters
    ----------
    times : numpy.ndarray
        The light curve times.
    fourier_coef : numpy.ndarray
        The fit fourier coefficients.
    order : int
        The order of the fourier series to fit.

    Returns
    -------
    magnitudes : numpy.ndarray
        The calculated light curve magnitudes.
    """
    cos_vals = [coef[2 * k + 1] * np.cos(2 * np.pi * (k + 1) * times + coef[2 * k + 2])
            for k in range(order)]
    cos_sum = np.sum(cos_vals, axis=0)

    return coef[0] + cos_sum

if __name__ == "__main__":
    main()
