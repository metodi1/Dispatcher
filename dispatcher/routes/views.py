from django.forms import formset_factory
from django.conf import settings
from django.shortcuts import render
from django.views.generic import ListView
from googlemaps.geocoding import geocode

from dispatcher.routes.forms import RouteForm, WaypointForm
from dispatcher.routes.models import RoundDetails
from dispatcher.core_function.functions import get_info
from django.views.generic.detail import DetailView
import googlemaps


def home_page(request):
    api_key = settings.GOOGLE_MAPS_API_KEY
    context = {
        'api_key': api_key,
    }

    return render(request, 'home/home page.html', context)


def route_view(request):
    api_key = settings.GOOGLE_MAPS_API_KEY
    gmaps = googlemaps.Client(key=api_key)
    # Create the waypoint formset (with 3 extra empty forms)
    WaypointFormSet = formset_factory(WaypointForm, extra=1)

    total_distance = 0

    if request.method == 'POST':

        # Handle route form (start and end points)
        route_form = RouteForm(request.POST)

        # Handle the waypoint formset
        waypoint_formset = WaypointFormSet(request.POST)

        if route_form.is_valid() and waypoint_formset.is_valid():
            # Extract data from the start and end points form
            start_location = route_form.cleaned_data['start_point']
            end_location = route_form.cleaned_data['end_point']

            geocode_start_location = gmaps.geocode(start_location)
            start_location_en = geocode_start_location[0]['formatted_address']

            geocode_end_location = gmaps.geocode(end_location)
            end_location_en = geocode_end_location[0]['formatted_address']

            # Process each waypoint in the formset
            waypoints = []
            for form in waypoint_formset:
                waypoint = form.cleaned_data.get('waypoint')
                if waypoint:
                    geocode_waypoint = gmaps.geocode(waypoint)
                    waypoint_en = geocode_waypoint[0]['formatted_address']
                    waypoints.append(waypoint_en)

            # Process or save the data (start, end, waypoints)

            route_legs = get_info(start_location, end_location, waypoints)

            for route in route_legs:
                total_distance = total_distance + (int(route['distance_value']) / 1000)

            for route in route_legs:
                total_distance = total_distance + (int(route['distance_value']) / 1000)

            round_number = RoundDetails(start_point=start_location_en, end_point=end_location_en, waypoints=waypoints,
                                        total_distance=total_distance)
            round_number.save()

            context = {
                'start_point': start_location,
                'end_point': end_location,
                'waypoints': waypoints,
                'google_maps_api_key': api_key,
                'route_legs': route_legs,
                'status': 'true'
            }
            return render(request, 'maps/map.html', context)

    else:
        # Display empty forms for GET requests
        route_form = RouteForm()
        waypoint_formset = WaypointFormSet()

    return render(request, 'forms/formForInput.html',
                  {'route_form': route_form, 'waypoint_formset': waypoint_formset})


class RouteDetailView(DetailView):
    model = RoundDetails
    template_name = 'maps/details_map.html'
    context_object_name = 'route'

    api_key = settings.GOOGLE_MAPS_API_KEY

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY
        return context


class ProductListView(ListView):
    model = RoundDetails
    template_name = 'home/routes_list.html'
    context_object_name = 'routes'
