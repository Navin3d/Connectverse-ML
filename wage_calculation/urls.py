from django.urls import path
from . import views

urlpatterns = [
        path("wage/<str:age_input>/<str:gender_input>/<str:WorkingHrsMoreThan40PerWeek_input>/<str:workType_input>",
         views.get_wage_amount),
    path("working_hours/<str:age_input>/<str:gender_input>/<str:wage_input>/<str:workType_input>/<str:physicalHealthPoints>",
         views.get_work_hours),
    path("can-apply/<str:payPerHour_input>/<str:workHoursPerWeekGreatethan21Hours_input>/<str:hasDrivingLicense_input>/<str:hasvehicle_input>/<str:waitingTime_input>/<str:blokSameAsJob_input>/<str:districtSameAsJob_input>/<str:stateSameAsJob_input>/<str:readyToRelocate_input>/",
         views.can_apply_for_job),
]
