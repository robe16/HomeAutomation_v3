import ast
from src.bundles.info_services.weather_metoffice.metoffice import info_metoffice


def compile_weather():
    #
    data = info_metoffice().createForecast()
    #
    try:
        return ast.literal_eval(data)
    except:
        return data
