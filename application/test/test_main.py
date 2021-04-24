def test_ping(client):
    """
    WHEN GET ping
    THEN receive pong!
    :param client: app instance
    """
    res = client.get("/ping/")
    assert res.status_code == 200

    data = res.get_json()

    assert data == "pong!"


def test_calc_option_vanilla_years(client):
    """
    GIVEN param hull exercice + years
    WHEN ask for values
    THEN Have the right result
    :param client:
    """
    res = client.get("/api/calc/option/vanilla/50/50/0.1/0.3/0.25/years/-1/")
    assert res.status_code == 200

    data = res.get_json()

    # Call
    assert data[0]["name"] == "Call"
    assert data[0]["price"] == 3.610
    assert data[0]["delta"] == 0.595
    assert data[0]["theta"] == -8.428
    assert data[0]["gamma"] == 0.052
    assert data[0]["vega"] == 9.687
    assert data[0]["rho"] == 6.541

    # Put
    assert data[1]["name"] == "Put"
    assert data[1]["price"] == 2.376
    assert data[1]["delta"] == -0.595
    assert data[1]["theta"] == -3.552
    assert data[1]["gamma"] == 0.052
    assert data[1]["vega"] == 9.687
    assert data[1]["rho"] == -5.650


def test_calc_option_vanilla_days(client):
    """
    GIVEN param hull exercice + days
    WHEN ask for values
    THEN Have the right result
    :param client:
    """
    res = client.get("/api/calc/option/vanilla/50/50/0.1/0.3/91.25/days/-1/")
    assert res.status_code == 200

    data = res.get_json()

    # Call
    assert data[0]["name"] == "Call"
    assert data[0]["price"] == 3.610
    assert data[0]["delta"] == 0.595
    assert data[0]["theta"] == -8.428
    assert data[0]["gamma"] == 0.052
    assert data[0]["vega"] == 9.687
    assert data[0]["rho"] == 6.541

    # Put
    assert data[1]["name"] == "Put"
    assert data[1]["price"] == 2.376
    assert data[1]["delta"] == -0.595
    assert data[1]["theta"] == -3.552
    assert data[1]["gamma"] == 0.052
    assert data[1]["vega"] == 9.687
    assert data[1]["rho"] == -5.650


def test_calc_option_vanilla_months(client):
    """
    GIVEN param hull exercice + months
    WHEN ask for values
    THEN Have the right result
    :param client:
    """
    res = client.get("/api/calc/option/vanilla/50/50/0.1/0.3/3/months/-1/")
    assert res.status_code == 200

    data = res.get_json()

    # Call
    assert data[0]["name"] == "Call"
    assert data[0]["price"] == 3.610
    assert data[0]["delta"] == 0.595
    assert data[0]["theta"] == -8.428
    assert data[0]["gamma"] == 0.052
    assert data[0]["vega"] == 9.687
    assert data[0]["rho"] == 6.541

    # Put
    assert data[1]["name"] == "Put"
    assert data[1]["price"] == 2.376
    assert data[1]["delta"] == -0.595
    assert data[1]["theta"] == -3.552
    assert data[1]["gamma"] == 0.052
    assert data[1]["vega"] == 9.687
    assert data[1]["rho"] == -5.650


def test_calc_delta(client):
    """
    GIVEN param from partiel2017
    WHEN ask for deltas
    THEN Have the right result
    :param client:
    """
    begin_spot = 85
    res = client.get("/api/calc/delta/" + str(begin_spot) + "/114/100/0.1/0.15/60/")
    assert res.status_code == 200

    data = res.get_json()

    result = [0.009, 0.015,	0.023, 0.036, 0.053, 0.076,	0.106, 0.142, 0.186, 0.237, 0.294, 0.355, 0.421, 0.487,
              0.554, 0.618, 0.679, 0.734, 0.784, 0.828, 0.865, 0.896, 0.921, 0.941, 0.957, 0.969, 0.978,
              0.985, 0.99, 0.993]

    count = 0
    for cell in data["call"]:
        assert cell['x'] == begin_spot
        assert cell['y'] == result[count]
        count += 1
        begin_spot += 1


def test_calc_theta(client):
    """
    GIVEN param from partiel2017
    WHEN ask for deltas
    THEN Have the right result
    :param client:
    """
    begin_spot = 85
    res = client.get("/api/calc/delta/" + str(begin_spot) + "/114/100/0.1/0.15/60/")
    assert res.status_code == 200

    data = res.get_json()

    count = 0
    for cell in data["call"]:
        assert cell['x'] == begin_spot
        assert cell['y']
        count += 1
        begin_spot += 1


def test_calc_gamma(client):
    """
    GIVEN param from partiel2017
    WHEN ask for deltas
    THEN Have the right result
    :param client:
    """
    begin_spot = 85
    res = client.get("/api/calc/gamma/" + str(begin_spot) + "/114/100/0.1/0.15/60/")
    assert res.status_code == 200

    data = res.get_json()

    count = 0
    for cell in data["call"]:
        assert cell['x'] == begin_spot
        assert cell['y']
        count += 1
        begin_spot += 1


def test_calc_vega(client):
    """
    GIVEN param from partiel2017
    WHEN ask for deltas
    THEN Have the right result
    :param client:
    """
    begin_spot = 85
    res = client.get("/api/calc/vega/" + str(begin_spot) + "/114/100/0.1/0.15/60/")
    assert res.status_code == 200

    data = res.get_json()

    count = 0
    for cell in data["call"]:
        assert cell['x'] == begin_spot
        assert cell['y']
        count += 1
        begin_spot += 1


def test_calc_rho(client):
    """
    GIVEN param from partiel2017
    WHEN ask for deltas
    THEN Have the right result
    :param client:
    """
    begin_spot = 85
    res = client.get("/api/calc/rho/" + str(begin_spot) + "/114/100/0.1/0.15/60/")
    assert res.status_code == 200

    data = res.get_json()

    count = 0
    for cell in data["call"]:
        assert cell['x'] == begin_spot
        assert cell['y']
        count += 1
        begin_spot += 1
