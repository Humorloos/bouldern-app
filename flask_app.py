from flask import Flask
from flask_restful import Api

from bouldernFormsApp.boulder_island_handler import BoulderIslandHandler
from bouldernFormsApp.constants import STUDIO_BLOC_HOOK_URL, BOULDER_ISLAND_HOOK_URL
from bouldernFormsApp.studio_bloc_handler import StudioBlocHandler
from googleCalendarApp.calendar_handler import CalendarHandler
from googleCalendarApp.constants import HOOK_URL as CALENDAR_HOOK_URL

app = Flask(__name__)
api = Api(app)

api.add_resource(CalendarHandler, f'/{CALENDAR_HOOK_URL}/')
api.add_resource(StudioBlocHandler, f'/{STUDIO_BLOC_HOOK_URL}/')
api.add_resource(BoulderIslandHandler, f'/{BOULDER_ISLAND_HOOK_URL}/')

if __name__ == '__main__':
    app.run(debug=True)
