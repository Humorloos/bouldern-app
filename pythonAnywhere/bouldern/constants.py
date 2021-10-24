from pathlib import Path

TARGET_DIR = Path(__file__).parent.parent.joinpath('target')

BOULDERN_URI = 'bouldern'
BOULDER_ISLAND_URI = 'boulder_island'
STUDIO_BLOC_URI = 'studio_bloc'

RESOURCES_PATH = Path(__file__).parent.joinpath('resources')
GOOGLE_API_PATH = RESOURCES_PATH.joinpath('google_api')
FIGURES_DIR = RESOURCES_PATH.joinpath('figures')
