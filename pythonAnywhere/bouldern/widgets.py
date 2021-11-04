from django.contrib.gis.forms import BaseGeometryWidget


class GymMapWidget(BaseGeometryWidget):
    template_name = 'bouldern/gym_map.html'

    class Media:
        extend = False
        js = ('https://cdnjs.cloudflare.com/ajax/libs/ol3/4.6.5/ol.js',
              'bouldern/js/map.js')
