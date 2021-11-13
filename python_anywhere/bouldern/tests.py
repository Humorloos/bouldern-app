# from django.core.files import File
#
# from bouldern.gyms import gyms
# from bouldern.models import *
#
#
# def populate_db():
#     for gym_name, gym_dict in gyms.items():
#         sections = gym_dict.pop('sections')
#         gym = Gym(name=gym_name, **gym_dict)
#         with open(Path(__file__).parent.joinpath('pythonAnywhere').joinpath('bouldern').joinpath('resources').joinpath('figures').joinpath(
#                       gym_name).joinpath('hallenplan.png').absolute(), 'rb') as gym_plan:
#             gym.gym_plan = File(gym_plan)
#             gym.save()
#         for section_name, section_dict in sections.items():
#             section_boundaries = SectionBoundaries(None, *section_dict.pop('boundaries').T.ravel())
#             section_boundaries.save()
#             section = Section(name=section_name, gym=gym, boundaries=section_boundaries)
#             section.save()
#             print(f'saving section {section_name}')
#             for wall_coords in section_dict['walls']:
#                 wall = Wall(None, *wall_coords, section=section)
#                 wall.save()
#
# populate_db()