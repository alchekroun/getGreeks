from flask import Blueprint, jsonify, make_response, request
from math import log, sqrt, exp
from scipy import stats

calc_bp = Blueprint('calc_bp', __name__,
                    url_prefix='/calc',
                    )


@calc_bp.route('/option/<type_option>/', methods=['POST'])
def calc_option(type_option):
    """Route for calculate all greek values plus the price.
    ---
    tags:
        - Calculate Option
    description: Route for calculate all greek values plus the price.
    consumes :
        -   "application/json"
    produces :
        -   "application/json"
    parameters:
        -   name: type_option
            in: path
            type: string
            enum: ['Vanilla', 'Dividend']
            required: true
        -   in : body
            name : body
            description:
                Input
            required: true
            schema:
                required:
                    - spot
                    - strike
                    - rate
                    - drift
                    - expiration
                    - time
                    - dividend
                properties:
                    spot:
                        description: Underlying spot of the option
                        type: number
                        min: 1
                        example: 50
                    strike:
                        description: Strike of the option
                        type: number
                        min: 1
                        example: 51
                    rate:
                        description: Rate risk free of the option
                        type: number
                        min: 0.05
                        max: 1
                        example: 0.1
                    drift:
                        description: Drift of the option
                        type: number
                        min: 0.05
                        max: 1
                        example: 0.3
                    expiration:
                        description: Expiration time of the option
                        type: number
                        min: 1
                        example: 15
                    time:
                        description: Time unity for the Expiration
                        type: string
                        enum: ['days', 'months', 'years']
                        example: 'days'
                    dividend:
                        description: Dividend of the option if it is an option with dividend. If it's not you can put
                            value but void.
                        type: number
                        min: 1
                        max: 25
                        example: 3
    responses:
        200:
            description: List of values associated to the input
        308:
            description: Redirection
        400:
            description: Invalid arguments
    """
    input_json = request.get_json()
    strike = float(input_json["strike"])
    spot = float(input_json["spot"])
    rate = float(input_json["rate"])
    drift = float(input_json["drift"])
    expiration = float(input_json["expiration"])
    dividend = float(input_json["dividend"])
    time = str(input_json["time"])

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
    if type_option == "Vanilla":
        d_1 = (log(spot / strike) + (rate + pow(drift, 2) * 0.5) * time_exp) / (drift * sqrt(time_exp))
    else:
        d_1 = (log(spot / strike) + (rate - dividend + pow(drift, 2) * 0.5) * time_exp) / (drift * sqrt(time_exp))

    d_2 = d_1 - (drift * sqrt(time_exp))

    # CDF
    n_d_1 = stats.norm.cdf(d_1)
    n_d_2 = stats.norm.cdf(d_2)
    n_d_n_1 = stats.norm.cdf(-d_1)
    n_d_n_2 = stats.norm.cdf(-d_2)

    # PDF
    np_d_1 = stats.norm.pdf(d_1)
    np_d_n_1 = stats.norm.pdf(-d_1)

    if type_option == "Vanilla":
        # Price
        price_call = spot * n_d_1 - strike * exp(-1 * rate * time_exp) * n_d_2
        price_put = strike * exp(-1 * rate * time_exp) * n_d_n_2 - spot * n_d_n_1

        # Greeks
        delta_call = n_d_1
        delta_put = -delta_call

        theta_call = -1 * ((spot * np_d_1 * drift) / (2 * sqrt(time_exp))) - rate * strike * exp(
            -rate * time_exp) * n_d_2
        theta_put = -1 * ((spot * np_d_1 * drift) / (2 * sqrt(time_exp))) + rate * strike * exp(
            -rate * time_exp) * n_d_n_2

        gamma_call = np_d_1 / (spot * drift * sqrt(time_exp))
        gamma_put = np_d_n_1 / (spot * drift * sqrt(time_exp))

        vega_call = spot * sqrt(time_exp) * np_d_1
        vega_put = spot * sqrt(time_exp) * np_d_n_1

        rho_call = strike * time_exp * exp(-rate * time_exp) * n_d_2
        rho_put = -strike * time_exp * exp(-rate * time_exp) * n_d_n_2
    elif type_option == 'Dividend':
        # Price
        price_call = spot * exp(-dividend * time_exp) * n_d_1 - strike * exp(-rate * time_exp) * n_d_2
        price_put = strike * exp(-rate * time_exp) * n_d_n_2 - spot * exp(-dividend * time_exp) * n_d_n_1

        # Greeks
        delta_call = exp(-1 * dividend * time_exp) * n_d_1
        delta_put = exp(-1 * dividend * time_exp) * (delta_call - 1)

        theta_call = -1 * ((spot * np_d_1 * drift * exp(-1 * dividend * time_exp)) / (
                2 * sqrt(time_exp))) + dividend * spot * n_d_1 * exp(
            -1 * dividend * time_exp) - rate * strike * exp(-rate * time_exp) * n_d_2
        theta_put = -1 * ((spot * np_d_1 * drift * exp(-1 * dividend * time_exp)) /
                          (2 * sqrt(time_exp))) - dividend * spot * n_d_1 * exp(
            -1 * dividend * time_exp) + rate * strike * exp(-rate * time_exp) * n_d_n_2

        gamma_call = (np_d_1 * exp(-1 * dividend * time_exp)) / (spot * drift * sqrt(time_exp))
        gamma_put = (np_d_n_1 * exp(-1 * dividend * time_exp)) / (spot * drift * sqrt(time_exp))

        vega_call = spot * sqrt(time_exp) * np_d_1 * exp(-1 * dividend * time_exp)
        vega_put = spot * sqrt(time_exp) * np_d_n_1 * exp(-1 * dividend * time_exp)

        rho_call = strike * time_exp * exp(-rate * time_exp) * n_d_2
        rho_put = -strike * time_exp * exp(-rate * time_exp) * n_d_n_2

    return jsonify([
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
    ])


@calc_bp.route('/<type_option>/delta/', methods=['POST'])
def calc_delta(type_option):
    """Route for calculate the variation of delta.
    ---
    tags:
        - Calculate Greek for Graph
    description: Route for calculate the variation of delta.
    consumes :
        -   "application/json"
    produces :
        -   "application/json"
    parameters:
        -   name: type_option
            in: path
            type: string
            enum: ['Vanilla', 'Dividend']
            required: true
        -   in : body
            name : body
            description:
                Input
            required: true
            schema:
                required:
                    - spot_b
                    - spot_e
                    - strike
                    - rate
                    - drift
                    - expiration
                    - time
                    - dividend
                properties:
                    spot_b:
                        description: First value of the spot interval
                        type: number
                        min: 1
                        max: 99
                        example: 40
                    spot_e:
                        description: Last value of the spot interval
                        type: number
                        min: 2
                        max: 100
                        example: 60
                    strike:
                        description: Strike of the option
                        type: number
                        min: 1
                        example: 50
                    rate:
                        description: Rate risk free of the option
                        type: number
                        min: 0.05
                        max: 1
                        example: 0.1
                    drift:
                        description: Drift of the option
                        type: number
                        min: 0.05
                        max: 1
                        example: 0.3
                    expiration:
                        description: Expiration time of the option
                        type: number
                        min: 1
                        example: 15
                    dividend:
                        description: Dividend of the option if it is an option with dividend. If it's not you can put
                            value but void.
                        type: number
                        min: 1
                        max: 25
                        example: 3
    responses:
        200:
            description: List of values associated to the input
        308:
            description: Redirection
        400:
            description: Invalid arguments
    """
    input_json = request.get_json()
    strike = float(input_json["strike"])
    spot_b = float(input_json["spot_b"])
    spot_e = float(input_json["spot_e"])
    rate = float(input_json["rate"])
    drift = float(input_json["drift"])
    expiration = float(input_json["expiration"])
    dividend = float(input_json["dividend"])

    count = 0
    result_tot = {
        "call": [{'x': 0.0, 'y': 0.0} for i in range(int(spot_e - spot_b))],
        "put": [{'x': 0.0, 'y': 0.0} for i in range(int(spot_e - spot_b))],
    }
    time_exp = expiration / 365
    if type_option == "Vanilla":
        for i in range(int(spot_b), int(spot_e), 1):
            result_tot["put"][count]['x'] = i
            result_tot["call"][count]['x'] = i
            result_tot["call"][count]['y'] = round(stats.norm.cdf(
                (log(i / strike) + (rate + pow(drift, 2) * 0.5) * time_exp) / (drift * sqrt(time_exp))), 3)
            result_tot["put"][count]['y'] = -1 * result_tot["call"][count]['y']
            count += 1
    elif type_option == 'Dividend':
        for i in range(int(spot_b), int(spot_e), 1):
            result_tot["put"][count]['x'] = i
            result_tot["call"][count]['x'] = i
            result_tot["call"][count]['y'] = round(exp(-1 * dividend * time_exp) * stats.norm.cdf(
                (log(i / strike) + (rate - dividend + pow(drift, 2) * 0.5) * time_exp) / (drift * sqrt(time_exp))), 3)
            result_tot["put"][count]['y'] = round(exp(-1 * dividend * time_exp) * (result_tot["call"][count]['y'] - 1),
                                                  3)
            count += 1

    return jsonify(result_tot)


@calc_bp.route('/<type_option>/theta/', methods=['POST'])
def calc_theta(type_option):
    """Route for calculate the variation of theta.
    ---
    tags:
        - Calculate Greek for Graph
    description: Route for calculate the variation of theta.
    consumes :
        -   "application/json"
    produces :
        -   "application/json"
    parameters:
        -   name: type_option
            in: path
            type: string
            enum: ['Vanilla', 'Dividend']
            required: true
        -   in : body
            name : body
            description:
                Input
            required: true
            schema:
                required:
                    - spot_b
                    - spot_e
                    - strike
                    - rate
                    - drift
                    - expiration
                    - time
                    - dividend
                properties:
                    spot_b:
                        description: First value of the spot interval
                        type: number
                        min: 1
                        max: 99
                        example: 40
                    spot_e:
                        description: Last value of the spot interval
                        type: number
                        min: 2
                        max: 100
                        example: 60
                    strike:
                        description: Strike of the option
                        type: number
                        min: 1
                        example: 50
                    rate:
                        description: Rate risk free of the option
                        type: number
                        min: 0.05
                        max: 1
                        example: 0.1
                    drift:
                        description: Drift of the option
                        type: number
                        min: 0.05
                        max: 1
                        example: 0.3
                    expiration:
                        description: Expiration time of the option
                        type: number
                        min: 1
                        example: 15
                    dividend:
                        description: Dividend of the option if it is an option with dividend. If it's not you can put
                            value but void.
                        type: number
                        min: 1
                        max: 25
                        example: 3
    responses:
        200:
            description: List of values associated to the input
        308:
            description: Redirection
        400:
            description: Invalid arguments
    """
    input_json = request.get_json()
    strike = float(input_json["strike"])
    spot_b = float(input_json["spot_b"])
    spot_e = float(input_json["spot_e"])
    rate = float(input_json["rate"])
    drift = float(input_json["drift"])
    expiration = float(input_json["expiration"])
    dividend = float(input_json["dividend"])

    count = 0
    result_tot = {
        "call": [{'x': 0.0, 'y': 0.0} for i in range(int(spot_e - spot_b))],
        "put": [{'x': 0.0, 'y': 0.0} for i in range(int(spot_e - spot_b))],
    }
    time_exp = expiration / 365
    if type_option == 'Vanilla':
        for i in range(int(spot_b), int(spot_e), 1):
            d_1 = (log(i / strike) + (rate - dividend + pow(drift, 2) / 2) * time_exp) / (drift * sqrt(time_exp))
            d_2 = d_1 - (drift * sqrt(time_exp))
            np_d_1 = stats.norm.pdf(d_1)
            n_d_2 = stats.norm.cdf(d_2)
            n_d_n_2 = stats.norm.cdf(-d_2)

            result_tot["put"][count]['x'] = i
            result_tot["call"][count]['x'] = i

            result_tot["call"][count]['y'] = round(
                -1 * ((i * np_d_1 * drift) / (2 * sqrt(time_exp))) - rate * strike * exp(
                    -rate * time_exp) * n_d_2, 3)
            result_tot["put"][count]['y'] = round(
                -1 * ((i * np_d_1 * drift) / (2 * sqrt(time_exp))) + rate * strike * exp(
                    -rate * time_exp) * n_d_n_2, 3)
            count += 1
    elif type_option == 'Dividend':
        for i in range(int(spot_b), int(spot_e), 1):
            d_1 = (log(i / strike) + (rate - dividend + pow(drift, 2) / 2) * time_exp) / (drift * sqrt(time_exp))
            d_2 = d_1 - (drift * sqrt(time_exp))
            n_d_1 = stats.norm.cdf(d_1)
            np_d_1 = stats.norm.pdf(d_1)
            n_d_2 = stats.norm.cdf(d_2)
            n_d_n_2 = stats.norm.cdf(-d_2)

            result_tot["put"][count]['x'] = i
            result_tot["call"][count]['x'] = i

            result_tot["call"][count]['y'] = round(-1 * ((i * np_d_1 * drift * exp(-1 * dividend * time_exp)) /
                                                         (2 * sqrt(time_exp))) - dividend * i * n_d_1 *
                                                   exp(-1 * dividend * time_exp) - rate * strike * exp(
                -rate * time_exp) * n_d_2, 3)
            result_tot["put"][count]['y'] = round(-1 * ((i * np_d_1 * drift * exp(-1 * dividend * time_exp)) /
                                                        (2 * sqrt(time_exp))) - dividend * i * n_d_1 * exp(
                -1 * dividend * time_exp) + rate * strike * exp(-rate * time_exp) * n_d_n_2, 3)
            count += 1

    return jsonify(result_tot)


@calc_bp.route('/<type_option>/gamma/', methods=['POST'])
def calc_gamma(type_option):
    """Route for calculate the variation of gamma.
    ---
    tags:
        - Calculate Greek for Graph
    description: Route for calculate the variation of gamma.
    consumes :
        -   "application/json"
    produces :
        -   "application/json"
    parameters:
        -   name: type_option
            in: path
            type: string
            enum: ['Vanilla', 'Dividend']
            required: true
        -   in : body
            name : body
            description:
                Input
            required: true
            schema:
                required:
                    - spot_b
                    - spot_e
                    - strike
                    - rate
                    - drift
                    - expiration
                    - time
                    - dividend
                properties:
                    spot_b:
                        description: First value of the spot interval
                        type: number
                        min: 1
                        max: 99
                        example: 40
                    spot_e:
                        description: Last value of the spot interval
                        type: number
                        min: 2
                        max: 100
                        example: 60
                    strike:
                        description: Strike of the option
                        type: number
                        min: 1
                        example: 50
                    rate:
                        description: Rate risk free of the option
                        type: number
                        min: 0.05
                        max: 1
                        example: 0.1
                    drift:
                        description: Drift of the option
                        type: number
                        min: 0.05
                        max: 1
                        example: 0.3
                    expiration:
                        description: Expiration time of the option
                        type: number
                        min: 1
                        example: 15
                    dividend:
                        description: Dividend of the option if it is an option with dividend. If it's not you can put
                            value but void.
                        type: number
                        min: 1
                        max: 25
                        example: 3
    responses:
        200:
            description: List of values associated to the input
        308:
            description: Redirection
        400:
            description: Invalid arguments
    """
    input_json = request.get_json()
    strike = float(input_json["strike"])
    spot_b = float(input_json["spot_b"])
    spot_e = float(input_json["spot_e"])
    rate = float(input_json["rate"])
    drift = float(input_json["drift"])
    expiration = float(input_json["expiration"])
    dividend = float(input_json["dividend"])

    count = 0
    result_tot = {
        "call": [{'x': 0.0, 'y': 0.0} for i in range(int(spot_e - spot_b))],
        "put": [{'x': 0.0, 'y': 0.0} for i in range(int(spot_e - spot_b))],
    }
    time_exp = expiration / 365
    if type_option == 'Vanilla':
        for i in range(int(spot_b), int(spot_e), 1):
            d_1 = (log(i / strike) + (rate - dividend + pow(drift, 2) / 2) * time_exp) / (drift * sqrt(time_exp))
            np_d_1 = stats.norm.pdf(d_1)
            np_d_n_1 = stats.norm.pdf(-d_1)

            result_tot["put"][count]['x'] = i
            result_tot["call"][count]['x'] = i

            result_tot["call"][count]['y'] = round(np_d_1 / (i * drift * sqrt(time_exp)), 3)
            result_tot["put"][count]['y'] = round(np_d_n_1 / (i * drift * sqrt(time_exp)), 3)
            count += 1
    elif type_option == 'Dividend':
        for i in range(int(spot_b), int(spot_e), 1):
            d_1 = (log(i / strike) + (rate - dividend + pow(drift, 2) / 2) * time_exp) / (drift * sqrt(time_exp))
            np_d_1 = stats.norm.pdf(d_1)
            np_d_n_1 = stats.norm.pdf(-d_1)

            result_tot["put"][count]['x'] = i
            result_tot["call"][count]['x'] = i

            result_tot["call"][count]['y'] = round(
                (np_d_1 * exp(-1 * dividend * time_exp)) / (i * drift * sqrt(time_exp)), 3)
            result_tot["put"][count]['y'] = round(
                (np_d_n_1 * exp(-1 * dividend * time_exp)) / (i * drift * sqrt(time_exp)), 3)
            count += 1

    return jsonify(result_tot)


@calc_bp.route('/<type_option>/vega/', methods=['POST'])
def calc_vega(type_option):
    """Route for calculate the variation of vega.
    ---
    tags:
        - Calculate Greek for Graph
    description: Route for calculate the variation of vega.
    consumes :
        -   "application/json"
    produces :
        -   "application/json"
    parameters:
        -   name: type_option
            in: path
            type: string
            enum: ['Vanilla', 'Dividend']
            required: true
        -   in : body
            name : body
            description:
                Input
            required: true
            schema:
                required:
                    - spot_b
                    - spot_e
                    - strike
                    - rate
                    - drift
                    - expiration
                    - time
                    - dividend
                properties:
                    spot_b:
                        description: First value of the spot interval
                        type: number
                        min: 1
                        max: 99
                        example: 40
                    spot_e:
                        description: Last value of the spot interval
                        type: number
                        min: 2
                        max: 100
                        example: 60
                    strike:
                        description: Strike of the option
                        type: number
                        min: 1
                        example: 50
                    rate:
                        description: Rate risk free of the option
                        type: number
                        min: 0.05
                        max: 1
                        example: 0.1
                    drift:
                        description: Drift of the option
                        type: number
                        min: 0.05
                        max: 1
                        example: 0.3
                    expiration:
                        description: Expiration time of the option
                        type: number
                        min: 1
                        example: 15
                    dividend:
                        description: Dividend of the option if it is an option with dividend. If it's not you can put
                            value but void.
                        type: number
                        min: 1
                        max: 25
                        example: 3
    responses:
        200:
            description: List of values associated to the input
        308:
            description: Redirection
        400:
            description: Invalid arguments
    """
    input_json = request.get_json()
    strike = float(input_json["strike"])
    spot_b = float(input_json["spot_b"])
    spot_e = float(input_json["spot_e"])
    rate = float(input_json["rate"])
    drift = float(input_json["drift"])
    expiration = float(input_json["expiration"])
    dividend = float(input_json["dividend"])

    count = 0
    result_tot = {
        "call": [{'x': 0.0, 'y': 0.0} for i in range(int(spot_e - spot_b))],
        "put": [{'x': 0.0, 'y': 0.0} for i in range(int(spot_e - spot_b))],
    }
    time_exp = expiration / 365
    if type_option == 'Vanilla':
        for i in range(int(spot_b), int(spot_e), 1):
            d_1 = (log(i / strike) + (rate - dividend + pow(drift, 2) / 2) * time_exp) / (drift * sqrt(time_exp))
            np_d_1 = stats.norm.pdf(d_1)
            np_d_n_1 = stats.norm.pdf(-d_1)

            result_tot["put"][count]['x'] = i
            result_tot["call"][count]['x'] = i

            result_tot["call"][count]['y'] = round(i * sqrt(time_exp) * np_d_1, 3)
            result_tot["put"][count]['y'] = round(i * sqrt(time_exp) * np_d_n_1, 3)
            count += 1
    elif type_option == 'Dividend':
        for i in range(int(spot_b), int(spot_e), 1):
            d_1 = (log(i / strike) + (rate - dividend + pow(drift, 2) / 2) * time_exp) / (drift * sqrt(time_exp))
            np_d_1 = stats.norm.pdf(d_1)

            result_tot["put"][count]['x'] = i
            result_tot["call"][count]['x'] = i

            result_tot["call"][count]['y'] = round(i * sqrt(time_exp) * np_d_1 * exp(-1 * dividend * time_exp), 3)
            result_tot["put"][count]['y'] = round(i * sqrt(time_exp) * np_d_1 * exp(-1 * dividend * time_exp), 3)
            count += 1

    return jsonify(result_tot)


@calc_bp.route('/<type_option>/rho/', methods=['POST'])
def calc_rho(type_option):
    """Route for calculate the variation of vega.
    ---
    tags:
        - Calculate Greek for Graph
    description: Route for calculate the variation of vega.
    consumes :
        -   "application/json"
    produces :
        -   "application/json"
    parameters:
        -   name: type_option
            in: path
            type: string
            enum: ['Vanilla', 'Dividend']
            required: true
        -   in : body
            name : body
            description:
                Input
            required: true
            schema:
                required:
                    - spot_b
                    - spot_e
                    - strike
                    - rate
                    - drift
                    - expiration
                    - time
                    - dividend
                properties:
                    spot_b:
                        description: First value of the spot interval
                        type: number
                        min: 1
                        max: 99
                        example: 40
                    spot_e:
                        description: Last value of the spot interval
                        type: number
                        min: 2
                        max: 100
                        example: 60
                    strike:
                        description: Strike of the option
                        type: number
                        min: 1
                        example: 50
                    rate:
                        description: Rate risk free of the option
                        type: number
                        min: 0.05
                        max: 1
                        example: 0.1
                    drift:
                        description: Drift of the option
                        type: number
                        min: 0.05
                        max: 1
                        example: 0.3
                    expiration:
                        description: Expiration time of the option
                        type: number
                        min: 1
                        example: 15
                    dividend:
                        description: Dividend of the option if it is an option with dividend. If it's not you can put
                            value but void.
                        type: number
                        min: 1
                        max: 25
                        example: 3
    responses:
        200:
            description: List of values associated to the input
        308:
            description: Redirection
        400:
            description: Invalid arguments
    """
    input_json = request.get_json()
    strike = float(input_json["strike"])
    spot_b = float(input_json["spot_b"])
    spot_e = float(input_json["spot_e"])
    rate = float(input_json["rate"])
    drift = float(input_json["drift"])
    expiration = float(input_json["expiration"])
    dividend = float(input_json["dividend"])

    count = 0
    result_tot = {
        "call": [{'x': 0.0, 'y': 0.0} for i in range(int(spot_e - spot_b))],
        "put": [{'x': 0.0, 'y': 0.0} for i in range(int(spot_e - spot_b))],
    }
    time_exp = expiration / 365
    if type_option == "Vanilla":
        for i in range(int(spot_b), int(spot_e), 1):
            d_1 = (log(i / strike) + (rate - dividend + pow(drift, 2) / 2) * time_exp) / (drift * sqrt(time_exp))
            d_2 = d_1 - (drift * sqrt(time_exp))
            n_d_2 = stats.norm.cdf(d_2)
            n_d_n_2 = stats.norm.cdf(-d_2)

            result_tot["put"][count]['x'] = i
            result_tot["call"][count]['x'] = i

            result_tot["call"][count]['y'] = round(strike * time_exp * exp(-rate * time_exp) * n_d_2, 3)
            result_tot["put"][count]['y'] = round(-strike * time_exp * exp(-rate * time_exp) * n_d_n_2, 3)
            count += 1
    elif type_option == "Dividend":
        for i in range(int(spot_b), int(spot_e), 1):
            d_1 = (log(i / strike) + (rate - dividend + pow(drift, 2) / 2) * time_exp) / (drift * sqrt(time_exp))
            n_d_1 = stats.norm.cdf(d_1)
            n_d_n_1 = stats.norm.cdf(-d_1)

            result_tot["put"][count]['x'] = i
            result_tot["call"][count]['x'] = i

            result_tot["call"][count]['y'] = round(-time_exp * exp(-rate * time_exp) * i * n_d_1, 3)
            result_tot["put"][count]['y'] = round(-time_exp * exp(-rate * time_exp) * i * n_d_n_1, 3)
            count += 1

    return jsonify(result_tot)
