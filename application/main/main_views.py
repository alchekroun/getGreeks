from flask import Blueprint, jsonify, make_response
from math import log, sqrt, exp

from scipy import stats

main_bp = Blueprint('main_bp', __name__, template_folder='templates/vue_template')


@main_bp.route('/')
def index():
    """Landing page / Home page"""
    return jsonify('pong!')


@main_bp.route('/api/calc/option/<spot>/<strike>/<rate>/<drift>/<expiration>/<time>/')
def calc_option(spot, strike, rate, drift, expiration, time):
    """Routing for calculate all variable from an option """

    strike = float(strike)
    spot = float(spot)
    rate = float(rate)
    drift = float(drift)
    expiration = float(expiration)

    if not strike or not spot or not rate or not drift or not expiration or not time:
        message = jsonify(message='invalid arguments')
        return make_response(message, 400)

    if time == "days":
        time_u = 365
    elif time == "months":
        time_u = 12
    elif time == "years":
        time_u = 1
    else:
        message = jsonify(message='invalid arguments')
        return make_response(message, 400)

    time_exp = expiration/time_u

    # D1 and D2
    d_1 = (log(strike / spot) + (rate + pow(drift, 2) / 2) * time_exp) / (drift * sqrt(time_exp))
    d_2 = d_1 - (drift * sqrt(time_exp))

    # CDF
    n_d_1 = stats.norm.cdf(d_1)
    n_d_2 = stats.norm.cdf(d_2)
    n_d_n_1 = stats.norm.cdf(-d_1)
    n_d_n_2 = stats.norm.cdf(-d_2)

    # PDF
    np_d_1 = stats.norm.pdf(d_1)
    np_d_2 = stats.norm.pdf(d_2)
    np_d_n_1 = stats.norm.pdf(-d_1)
    np_d_n_2 = stats.norm.pdf(-d_2)

    # Price
    price_call = spot * n_d_1 - strike * exp(-1 * rate * time_exp) * n_d_2
    price_put = strike * exp(-1 * rate * time_exp) * n_d_n_2 - spot * n_d_n_1

    # Greeks
    delta_call = n_d_1
    delta_put = -1 * delta_call

    theta_call = -1 * ((spot * np_d_1 * drift)/(2*sqrt(time_exp))) - rate * strike * exp(-rate * time_exp) * n_d_2
    theta_put = -1 * ((spot * np_d_1 * drift)/(2*sqrt(time_exp))) + rate * strike * exp(-rate * time_exp) * n_d_n_2

    gamma_call = np_d_1 * (spot * drift * sqrt(time_exp))
    gamma_put = np_d_n_1 * (spot * drift * sqrt(time_exp))

    vega_call = spot * sqrt(time_exp) * np_d_1
    vega_put = spot * sqrt(time_exp) * np_d_n_1

    rho_call = strike * time_exp * exp(-rate * time_exp)*n_d_2
    rho_put = -strike * time_exp * exp(-rate * time_exp)*n_d_n_2

    return jsonify({
        "call": {
            "price": price_call,
            "delta": delta_call,
            "theta": theta_call,
            "gamma": gamma_call,
            "rho": rho_call,
            "vega": vega_call,
        },
        "put": {
            "price": price_put,
            "delta": delta_put,
            "theta": theta_put,
            "gamma": gamma_put,
            "rho": rho_put,
            "vega": vega_put,
        }
    })


@main_bp.route('/ping/')
def ping():
    """Testing route ping...pong"""
    return jsonify('pong!')


@main_bp.route('/about/')
def about():
    """About page"""
    print("about")
