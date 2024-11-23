# forms.py
from django import forms


class RouteForm(forms.Form):
    start_point = forms.CharField(label='Начална точка', max_length=100)
    end_point = forms.CharField(label='Крайна точка', max_length=100)


class WaypointForm(forms.Form):
    waypoint = forms.CharField(max_length=100, label="Спирка")
