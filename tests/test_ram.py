from inspector.ram import get_ram_info


def test_get_ram_info_returns_dict():
    result = get_ram_info()
    assert isinstance(result, dict)


def test_ram_required_keys_present():
    result = get_ram_info()
    expected_keys = [
        "total_gb",
        "used_gb",
        "free_gb",
        "available_gb",
        "usage_percent",
        "swap_total_gb",
        "swap_used_gb",
        "swap_free_gb",
        "swap_usage_percent",
    ]
    for key in expected_keys:
        assert key in result, f"Missing key: {key}"


def test_ram_values_are_positive():
    result = get_ram_info()
    assert result["total_gb"] > 0
    assert result["used_gb"] >= 0
    assert result["free_gb"] >= 0
    assert result["available_gb"] >= 0


def test_ram_usage_percent_is_valid():
    result = get_ram_info()
    assert 0.0 <= result["usage_percent"] <= 100.0


def test_ram_available_lte_total():
    result = get_ram_info()
    assert result["available_gb"] <= result["total_gb"]


def test_ram_used_lte_total():
    result = get_ram_info()
    assert result["used_gb"] <= result["total_gb"]


def test_swap_values_are_non_negative():
    result = get_ram_info()
    assert result["swap_total_gb"] >= 0
    assert result["swap_used_gb"] >= 0
    assert result["swap_free_gb"] >= 0


def test_swap_usage_percent_is_valid():
    result = get_ram_info()
    assert 0.0 <= result["swap_usage_percent"] <= 100.0