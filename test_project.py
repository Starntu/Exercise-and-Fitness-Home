from project import valid_date
from project import metric
from project import imperial
from project import interpret_bmi
import pytest


def test_date():
    with pytest.raises(ValueError):
        valid_date("7/16/19999")
    with pytest.raises(ValueError):
        valid_date("hi/16/19999")


def test_metric():
    assert metric(1.75, 70) == 22.86
    assert metric(2, 90) == 22.5

    assert metric("height", 70) is None
    assert metric(1.75, "weight") is None
    assert metric(0, 70) is None


def test_imperial():
    assert imperial(5, 7, 150) == 23.49

    assert imperial("5'", 7, 150) is None
    assert imperial(5, '7"', 150) is None
    assert imperial(5, 7, "weight") is None
    assert imperial(0, 0, 150) is None


def test_bmi():
    assert interpret_bmi(17.5) == "Underweight"
    assert interpret_bmi(20.0) == "Normal weight"
    assert interpret_bmi(27.5) == "Overweight"
    assert interpret_bmi(35.0) == "Obese"
