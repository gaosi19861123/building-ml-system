from datetime import date, datetime
from typing import Optional

from pandera import Check, Column, DataFrameSchema, Index
from pydantic import BaseModel
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


STORES = [
    "nagoya",
    "shinjuku",
    "osaka",
    "kobe",
    "sendai",
    "chiba",
    "morioka",
    "ginza",
    "yokohama",
    "ueno",
]

ITEMS = [
    "fruit_juice",
    "apple_juice",
    "orange_juice",
    "sports_drink",
    "coffee",
    "milk",
    "mineral_water",
    "sparkling_water",
    "soy_milk",
    "beer",
]

WEEKS = [i for i in range(1, 54, 1)]

MONTHS = [i for i in range(1, 13, 1)]

YEARS = [i for i in range(2017, 2031, 1)]

DAYS_OF_WEEK = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]

_BASE_SCHEMA = {
    "date": Column(datetime),
    "day_of_week": Column(str, checks=Check.isin(DAYS_OF_WEEK)),
    "store": Column(str, checks=Check.isin(STORES)),
    "item": Column(str, checks=Check.isin(ITEMS)),
    "item_price": Column(int, checks=Check.greater_than_or_equal_to(0)),
    "sales": Column(int, checks=Check.greater_than_or_equal_to(0)),
    "total_sales_amount": Column(int, checks=Check.greater_than_or_equal_to(0)),
}

BASE_SCHEMA = DataFrameSchema(
    _BASE_SCHEMA,
    index=Index(int),
    strict=True,
    coerce=True,
)

_WEEKLY_SCHEMA = {
    "year": Column(int),
    "week_of_year": Column(int, checks=Check.isin(WEEKS)),
    "month": Column(int, checks=Check.isin(MONTHS)),
    "store": Column(str, checks=Check.isin(STORES)),
    "item": Column(str, checks=Check.isin(ITEMS)),
    "item_price": Column(int, checks=Check.greater_than_or_equal_to(0)),
    "sales": Column(int, checks=Check.greater_than_or_equal_to(0)),
    "total_sales_amount": Column(int, checks=Check.greater_than_or_equal_to(0)),
    "sales_lag_.*": Column(float, checks=Check.greater_than_or_equal_to(0), nullable=True, regex=True),
}

WEEKLY_SCHEMA = DataFrameSchema(
    _WEEKLY_SCHEMA,
    index=Index(int),
    strict=True,
    coerce=True,
)

_PREPROCESSED_SCHEMA = {
    "store": Column(str, checks=Check.isin(STORES)),
    "item": Column(str, checks=Check.isin(ITEMS)),
    "year": Column(int, checks=Check.isin(YEARS)),
    "week_of_year": Column(int, checks=Check.isin(WEEKS)),
    "sales.*": Column(
        float,
        checks=Check(lambda x: x >= 0.0 and x <= 5000.0, element_wise=True),
        nullable=True,
        regex=True,
    ),
    "item_price": Column(float, checks=Check(lambda x: x >= 0.0 and x <= 1.0, element_wise=True)),
    "store_.*": Column(float, checks=Check.isin((0, 1)), regex=True),
    "item_.*[^price]": Column(float, checks=Check.isin((0, 1)), regex=True),
    "week_of_year_.*": Column(float, checks=Check.isin((0, 1)), regex=True),
    "month_.*": Column(float, checks=Check.isin((0, 1)), regex=True),
    "year_.*": Column(float, checks=Check.isin((0, 1)), regex=True),
}

PREPROCESSED_SCHEMA = DataFrameSchema(
    _PREPROCESSED_SCHEMA,
    index=Index(int),
    strict=True,
    coerce=True,
)

_WEEK_BASED_SPLIT_SCHEMA = {
    "year": Column(int),
    "week_of_year": Column(int, checks=Check.isin(WEEKS)),
}

WEEK_BASED_SPLIT_SCHEMA = DataFrameSchema(
    _WEEK_BASED_SPLIT_SCHEMA,
    index=Index(int),
)


_PREDICTION_SCHEMA = {
    "date": Column(datetime),
    "store": Column(str, checks=Check.isin(STORES)),
    "item": Column(str, checks=Check.isin(ITEMS)),
    "item_price": Column(int, checks=Check.greater_than_or_equal_to(0)),
}

PREDICTION_SCHEMA = DataFrameSchema(
    _PREDICTION_SCHEMA,
    index=Index(int),
    strict=True,
    coerce=True,
)

_UPDATED_BASE_SCHEMA = {
    "day_of_month": Column(int, checks=Check(lambda x: x >= 1 and x <= 31, element_wise=True)),
    "day_of_year": Column(int, checks=Check(lambda x: x >= 1 and x <= 366, element_wise=True)),
    "month": Column(int, checks=Check(lambda x: x >= 1 and x <= 12, element_wise=True)),
    "year": Column(int, checks=Check(lambda x: x >= 2000 and x <= 2030, element_wise=True)),
    "week_of_year": Column(int, checks=Check(lambda x: x >= 1 and x <= 53, element_wise=True)),
    "is_month_start": Column(int, checks=Check.isin((0, 1))),
    "is_month_end": Column(int, checks=Check.isin((0, 1))),
}

_UPDATED_SCHEMA = {**_BASE_SCHEMA, **_UPDATED_BASE_SCHEMA}

UPDATED_SCHEMA = DataFrameSchema(
    _UPDATED_SCHEMA,
    index=Index(int),
    strict=True,
    coerce=True,
)

_UPDATED_PREDICTION_SCHEMA = {**_PREDICTION_SCHEMA, **_UPDATED_BASE_SCHEMA}

UPDATED_PREDICTION_SCHEMA = DataFrameSchema(
    _UPDATED_PREDICTION_SCHEMA,
    index=Index(int),
    strict=True,
    coerce=True,
)
