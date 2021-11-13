from django.contrib.gis.forms import BaseGeometryWidget


class GymMapWidget(BaseGeometryWidget):
    template_name = 'bouldern/gym_map_wrapper.html'

    class Media:
        js = ('https://cdnjs.cloudflare.com/ajax/libs/ol3/4.6.5/ol.js',
              'bouldern/js/map.js')
