from inspector.cpu import get_cpu_info


def test_get_cpu_info_returns_dict():
    result = get_cpu_info()
    assert isinstance(result, dict)


def test_cpu_required_keys_present():
    result = get_cpu_info()
    expected_keys = [
        "model",
        "cores_physical",
        "cores_logical",
        "usage_percent_overall",
        "usage_percent_per_core",
        "freq_current_mhz",
        "freq_min_mhz",
        "freq_max_mhz",
    ]
    for key in expected_keys:
        assert key in result, f"Missing key: {key}"


def test_cpu_core_counts_are_positive_integers():
    result = get_cpu_info()
    assert isinstance(result["cores_physical"], int)
    assert isinstance(result["cores_logical"], int)
    assert result["cores_physical"] > 0
    assert result["cores_logical"] > 0


def test_logical_cores_gte_physical_cores():
    result = get_cpu_info()
    assert result["cores_logical"] >= result["cores_physical"]


def test_cpu_usage_overall_is_valid_percentage():
    result = get_cpu_info()
    assert isinstance(result["usage_percent_overall"], float)
    assert 0.0 <= result["usage_percent_overall"] <= 100.0


def test_cpu_usage_per_core_is_list():
    result = get_cpu_info()
    assert isinstance(result["usage_percent_per_core"], list)
    assert len(result["usage_percent_per_core"]) > 0


def test_cpu_usage_per_core_valid_percentages():
    result = get_cpu_info()
    for pct in result["usage_percent_per_core"]:
        assert 0.0 <= pct <= 100.0, f"Invalid per-core percentage: {pct}"