from django import forms


from django import forms
from timezone_field import TimeZoneFormField


class CountryForm(forms.Form):
    tz1 = TimeZoneFormField()  # renders like "Asia/Dubai"
    tz2 = TimeZoneFormField(
        choices_display="WITH_GMT_OFFSET"
    )  # renders like "GMT+04:00 Asia/Dubai"
    tz3 = TimeZoneFormField(use_pytz=True)  # returns pytz timezone objects
    tz4 = TimeZoneFormField(use_pytz=False)
