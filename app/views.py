import calendar
import logging

from flask_appbuilder.charts.views import (
    DirectByChartView, DirectChartView, GroupByChartView
)
from flask_appbuilder.models.group import aggregate_avg, aggregate_sum
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.views import ModelView

from . import appbuilder
from .models import Country, CountryStats, PoliticalType, Cisla

log = logging.getLogger(__name__)


class CountryStatsModelView(ModelView):
    datamodel = SQLAInterface(CountryStats)
    list_columns = ["country", "stat_date", "population", "unemployed", "college"]


class CountryModelView(ModelView):
    datamodel = SQLAInterface(Country)


class PoliticalTypeModelView(ModelView):
    datamodel = SQLAInterface(PoliticalType)

class CislaModelView(ModelView):
    datamodel = SQLAInterface(Cisla)
    list_columns = ["cislojedna", "cislodva"]

class CountryStatsDirectChart(DirectChartView):
    datamodel = SQLAInterface(CountryStats)
    chart_title = "Statistics"
    chart_type = "LineChart"
    direct_columns = {
        "General Stats": ("stat_date", "population", "unemployed", "college")
    }
    base_order = ("stat_date", "asc")


def pretty_month_year(value):
    return calendar.month_name[value.month] + " " + str(value.year)


class CountryDirectChartView(DirectByChartView):
    datamodel = SQLAInterface(CountryStats)
    chart_title = "Direct Data"

    definitions = [
        {
            "group": "stat_date",
            "series": ["unemployed", "college"],
        }
    ]


class CountryGroupByChartView(GroupByChartView):
    datamodel = SQLAInterface(CountryStats)
    chart_title = "Statistics"

    definitions = [
        {
            "label": "Country Stat",
            "group": "country",
            "series": [
                (aggregate_avg, "unemployed"),
                (aggregate_avg, "population"),
                (aggregate_avg, "college"),
            ],
        },
        {
            "group": "month_year",
            "formatter": pretty_month_year,
            "series": [
                (aggregate_sum, "unemployed"),
                (aggregate_avg, "population"),
                (aggregate_avg, "college"),
            ],
        },
    ]

class CislaDirectChartView(DirectByChartView):
    datamodel = SQLAInterface(Cisla)
    chart_title = "Cisla LOL"

    definitions = [
        {
            "group": "id",
            "series": ["cislojedna", "cislodva"],
        }
    ]

appbuilder.add_view(
    CislaModelView,
    "List of Cisla",
    icon="fa-folder-open-o",
    category="Statistics",
)
appbuilder.add_separator("Statistics")
appbuilder.add_view(
    CislaDirectChartView,
    "Show Cisla Chart",
    icon="fa-dashboard",
    category="Statistics",
)
