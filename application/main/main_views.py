import os
import json
from flask import Blueprint, jsonify, make_response, current_app, send_file
from math import log, sqrt, exp
from scipy import stats

main_bp = Blueprint('main_bp', __name__,
                    url_prefix='',
                    static_folder='./dist/static/',
                    template_folder='./dist/',
                    )


# For turning list into set before a serialisation
def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


@main_bp.route('/')
def index_client():
    """Landing page / Home page"""
    dist_dir = current_app.config['DIST_DIR']
    entry = os.path.join(dist_dir, 'index.html')

    return send_file(entry)


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

    time_exp = expiration / time_u

    # D1 and D2
    d_1 = (log(spot / strike) + (rate + pow(drift, 2) / 2) * time_exp) / (drift * sqrt(time_exp))
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

    theta_call = -1 * ((spot * np_d_1 * drift) / (2 * sqrt(time_exp))) - rate * strike * exp(-rate * time_exp) * n_d_2
    theta_put = -1 * ((spot * np_d_1 * drift) / (2 * sqrt(time_exp))) + rate * strike * exp(-rate * time_exp) * n_d_n_2

    gamma_call = np_d_1 * (spot * drift * sqrt(time_exp))
    gamma_put = np_d_n_1 * (spot * drift * sqrt(time_exp))

    vega_call = spot * sqrt(time_exp) * np_d_1
    vega_put = spot * sqrt(time_exp) * np_d_n_1

    rho_call = strike * time_exp * exp(-rate * time_exp) * n_d_2
    rho_put = -strike * time_exp * exp(-rate * time_exp) * n_d_n_2

    return jsonify({
        "call": {
            "price": round(price_call, 3),
            "delta": round(delta_call, 3),
            "theta": round(theta_call, 3),
            "gamma": round(gamma_call, 3),
            "rho": round(rho_call, 3),
            "vega": round(vega_call, 3),
        },
        "put": {
            "price": round(price_put, 3),
            "delta": round(delta_put, 3),
            "theta": round(theta_put, 3),
            "gamma": round(gamma_put, 3),
            "rho": round(rho_put, 3),
            "vega": round(vega_put, 3),
        },
        "dataTab": [
            {
                "name": "Call",
                "price": round(price_call, 3),
                "delta": round(delta_call, 3),
                "theta": round(theta_call, 3),
                "gamma": round(gamma_call, 3),
                "rho": round(rho_call, 3),
                "vega": round(vega_call, 3),
            },
            {
                "name": "Put",
                "price": round(price_put, 3),
                "delta": round(delta_put, 3),
                "theta": round(theta_put, 3),
                "gamma": round(gamma_put, 3),
                "rho": round(rho_put, 3),
                "vega": round(vega_put, 3),
            }
        ]

    })


@main_bp.route('/api/calc/delta/<spot_b>/<spot_e>/<strike>/<rate>/<drift>/<expiration>/')
def calc_delta(spot_b, spot_e, strike, rate, drift, expiration):
    """Routing to calculate all value of delta"""
    strike = float(strike)
    spot_b = float(spot_b)
    spot_e = float(spot_e)
    rate = float(rate)
    drift = float(drift)
    expiration = float(expiration)

    count = 0
    result_tot = {
        "call": [{'x': 0.0, 'y': 0.0} for i in range(int(spot_e - spot_b))],
        "put": [{'x': 0.0, 'y': 0.0} for i in range(int(spot_e - spot_b))],
    }
    time_exp = expiration / 365
    for i in range(int(spot_b), int(spot_e), 1):
        result_tot["put"][count]['x'] = i
        result_tot["call"][count]['x'] = i
        result_tot["call"][count]['y'] = round(stats.norm.cdf(
            (log(i / strike) + (rate * 0.5 * pow(drift, 2) * time_exp)) / (drift * sqrt(time_exp))), 3)
        result_tot["put"][count]['y'] = -1 * result_tot["call"][count]['y']
        count += 1

    return jsonify(result_tot)


@main_bp.route('/api/calc/theta/<spot_b>/<spot_e>/<strike>/<rate>/<drift>/<expiration>/')
def calc_theta(spot_b, spot_e, strike, rate, drift, expiration):
    """Routing to calculate all value of theta"""
    strike = float(strike)
    spot_b = float(spot_b)
    spot_e = float(spot_e)
    rate = float(rate)
    drift = float(drift)
    expiration = float(expiration)

    count = 0
    result_tot = {
        "call": [{'x': 0.0, 'y': 0.0} for i in range(int(spot_e - spot_b))],
        "put": [{'x': 0.0, 'y': 0.0} for i in range(int(spot_e - spot_b))],
    }
    time_exp = expiration / 365
    for i in range(int(spot_b), int(spot_e), 1):
        d_1 = (log(i / strike) + (rate + pow(drift, 2) / 2) * time_exp) / (drift * sqrt(time_exp))
        d_2 = d_1 - (drift * sqrt(time_exp))
        np_d_1 = stats.norm.pdf(d_1)
        n_d_2 = stats.norm.cdf(d_2)
        n_d_n_2 = stats.norm.cdf(-d_2)

        result_tot["put"][count]['x'] = i
        result_tot["call"][count]['x'] = i

        result_tot["call"][count]['y'] = round(-1 * ((i * np_d_1 * drift) / (2 * sqrt(time_exp))) - rate * strike * exp(
            -rate * time_exp) * n_d_2, 3)
        result_tot["put"][count]['y'] = round(-1 * ((i * np_d_1 * drift) / (2 * sqrt(time_exp))) + rate * strike * exp(
            -rate * time_exp) * n_d_n_2, 3)
        count += 1

    return jsonify(result_tot)


@main_bp.route('/api/calc/gamma/<spot_b>/<spot_e>/<strike>/<rate>/<drift>/<expiration>/')
def calc_gamma(spot_b, spot_e, strike, rate, drift, expiration):
    """Routing to calculate all value of gamma"""
    strike = float(strike)
    spot_b = float(spot_b)
    spot_e = float(spot_e)
    rate = float(rate)
    drift = float(drift)
    expiration = float(expiration)

    count = 0
    result_tot = {
        "call": [{'x': 0.0, 'y': 0.0} for i in range(int(spot_e - spot_b))],
        "put": [{'x': 0.0, 'y': 0.0} for i in range(int(spot_e - spot_b))],
    }
    time_exp = expiration / 365
    for i in range(int(spot_b), int(spot_e), 1):
        d_1 = (log(i / strike) + (rate + pow(drift, 2) / 2) * time_exp) / (drift * sqrt(time_exp))
        np_d_1 = stats.norm.pdf(d_1)
        np_d_n_1 = stats.norm.pdf(-d_1)

        result_tot["put"][count]['x'] = i
        result_tot["call"][count]['x'] = i

        result_tot["call"][count]['y'] = round(np_d_1 * (i * drift * sqrt(time_exp)), 3)
        result_tot["put"][count]['y'] = round(np_d_n_1 * (i * drift * sqrt(time_exp)), 3)
        count += 1

    return jsonify(result_tot)


@main_bp.route('/api/calc/vega/<spot_b>/<spot_e>/<strike>/<rate>/<drift>/<expiration>/')
def calc_vega(spot_b, spot_e, strike, rate, drift, expiration):
    """Routing to calculate all value of vega"""
    strike = float(strike)
    spot_b = float(spot_b)
    spot_e = float(spot_e)
    rate = float(rate)
    drift = float(drift)
    expiration = float(expiration)

    count = 0
    result_tot = {
        "call": [{'x': 0.0, 'y': 0.0} for i in range(int(spot_e - spot_b))],
        "put": [{'x': 0.0, 'y': 0.0} for i in range(int(spot_e - spot_b))],
    }
    time_exp = expiration / 365
    for i in range(int(spot_b), int(spot_e), 1):
        d_1 = (log(i / strike) + (rate + pow(drift, 2) / 2) * time_exp) / (drift * sqrt(time_exp))
        np_d_1 = stats.norm.pdf(d_1)
        np_d_n_1 = stats.norm.pdf(-d_1)

        result_tot["put"][count]['x'] = i
        result_tot["call"][count]['x'] = i

        result_tot["call"][count]['y'] = round(i * sqrt(time_exp) * np_d_1, 3)
        result_tot["put"][count]['y'] = round(i * sqrt(time_exp) * np_d_n_1, 3)
        count += 1

    return jsonify(result_tot)


@main_bp.route('/api/calc/rho/<spot_b>/<spot_e>/<strike>/<rate>/<drift>/<expiration>/')
def calc_rho(spot_b, spot_e, strike, rate, drift, expiration):
    """Routing to calculate all value of vega"""
    strike = float(strike)
    spot_b = float(spot_b)
    spot_e = float(spot_e)
    rate = float(rate)
    drift = float(drift)
    expiration = float(expiration)

    count = 0
    result_tot = {
        "call": [{'x': 0.0, 'y': 0.0} for i in range(int(spot_e - spot_b))],
        "put": [{'x': 0.0, 'y': 0.0} for i in range(int(spot_e - spot_b))],
    }
    time_exp = expiration / 365
    for i in range(int(spot_b), int(spot_e), 1):
        d_1 = (log(i / strike) + (rate + pow(drift, 2) / 2) * time_exp) / (drift * sqrt(time_exp))
        d_2 = d_1 - (drift * sqrt(time_exp))
        n_d_2 = stats.norm.cdf(d_2)
        n_d_n_2 = stats.norm.cdf(-d_2)

        result_tot["put"][count]['x'] = i
        result_tot["call"][count]['x'] = i

        result_tot["call"][count]['y'] = round(strike * time_exp * exp(-rate * time_exp) * n_d_2, 3)
        result_tot["put"][count]['y'] = round(-strike * time_exp * exp(-rate * time_exp) * n_d_n_2, 3)
        count += 1

    return jsonify(result_tot)


@main_bp.route('/ping/')
def ping():
    """Testing route ping...pong"""
    return jsonify('pong!')


@main_bp.route('/about/')
def about():
    """About page"""
    print("about")
