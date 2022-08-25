from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# Create your views here.
# https://navin3d.github.io/Connectverse-Staticfiles/staticfiles/Money_Calculation.csv
# https://navin3d.github.io/Connectverse-Staticfiles/staticfiles/Work_Time_Calculation.csv
# https://navin3d.github.io/Connectverse-Staticfiles/staticfiles/Job_Assign.csv

wage_data = pd.read_csv('https://navin3d.github.io/Connectverse-Staticfiles/staticfiles/Money_Calculation.csv')
wage_X = wage_data.drop(columns=['wagePerHr'])
wage_Y = wage_data['wagePerHr']
wage_model = DecisionTreeClassifier()
wage_model.fit(wage_X, wage_Y)


working_hrs_data = pd.read_csv('https://navin3d.github.io/Connectverse-Staticfiles/staticfiles/Work_Time_Calculation.csv')
working_hrs_X = working_hrs_data.drop(columns=['WorkingHrsMoreThan40PerWeek'])
working_hrs_Y = working_hrs_data['WorkingHrsMoreThan40PerWeek']
working_hrs_model = DecisionTreeClassifier()
working_hrs_model.fit(working_hrs_X, working_hrs_Y)


job_assign_data = pd.read_csv('https://navin3d.github.io/Connectverse-Staticfiles/staticfiles/Job_Assign.csv')
job_assign_X = job_assign_data.drop(columns=['canApplyToJob'])
job_assign_Y = job_assign_data['canApplyToJob']
print(job_assign_X, job_assign_Y)
job_assign_model = DecisionTreeClassifier()
job_assign_model.fit(job_assign_X, job_assign_Y)


def decode_gender(gender):
    if gender == "MALE":
        return 0
    elif gender == "FEMALE":
        return 1
    else:
        return 2


def decode_work_type(work_type):
    if work_type == "HOUSEHOLD":
        return 1
    elif work_type == "CONSTRUCTION":
        return 2
    elif work_type == "FARMING":
        return 3
    elif work_type == "ANY":
        return 4
    else:
        return 5


def decode_work_hrs(working_hrs):
    if working_hrs == "YES":
        return 0
    else:
        return 1


def predict_wage(age, gender_encoded, WorkingHrsMoreThan40PerWeek_encoded, workType_encoded):
    gender = decode_gender(gender_encoded)
    WorkingHrsMoreThan40PerWeek = decode_work_hrs(WorkingHrsMoreThan40PerWeek_encoded)
    workType = decode_work_type(workType_encoded)
    wage = wage_model.predict([[age, gender, WorkingHrsMoreThan40PerWeek, workType], [20, 1, 1, 0]])
    return wage[0]


def predict_work_hrs(age, gender_encoded, wage, workType_encoded, physicalHealthPoints):
    gender = decode_gender(gender_encoded)
    workType = decode_work_type(workType_encoded)
    working_hrs = working_hrs_model.predict([[age, gender, wage, workType, physicalHealthPoints], [20, 1, 1, 0, 7]])
    return working_hrs[0]


def predict_can_apply(payPerHour, workHoursPerWeekGreatethan21Hours, hasDrivingLicense, hasvehicle, waitingTime, blokSameAsJob, districtSameAsJob, stateSameAsJob, readyToRelocate):
    can_apply_job = job_assign_model.predict([[payPerHour, workHoursPerWeekGreatethan21Hours, hasDrivingLicense, hasvehicle, waitingTime, blokSameAsJob, districtSameAsJob, stateSameAsJob, readyToRelocate], [20, 1, 1, 0, 7, 0, 0, 0, 0]])
    return can_apply_job[0]


@api_view(["GET"])
def get_wage_amount(request, age_input, gender_input, WorkingHrsMoreThan40PerWeek_input, workType_input):
    if request.method == "GET":
        wage = predict_wage(age_input, gender_input, WorkingHrsMoreThan40PerWeek_input, workType_input)
        return Response(wage, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_work_hours(request, age_input, gender_input, wage_input, workType_input, physicalHealthPoints):
    if request.method == "GET":
        working_hrs = predict_work_hrs(age_input, gender_input, wage_input, workType_input, physicalHealthPoints)
        return Response(working_hrs, status=status.HTTP_200_OK)


@api_view(["GET"])
def can_apply_for_job(request, payPerHour_input, workHoursPerWeekGreatethan21Hours_input, hasDrivingLicense_input, hasvehicle_input, waitingTime_input, blokSameAsJob_input, districtSameAsJob_input, stateSameAsJob_input, readyToRelocate_input):
    if request.method == "GET":
        can_apply = predict_can_apply(payPerHour_input, workHoursPerWeekGreatethan21Hours_input, hasDrivingLicense_input, hasvehicle_input, waitingTime_input, blokSameAsJob_input, districtSameAsJob_input, stateSameAsJob_input, readyToRelocate_input)
        return Response(can_apply, status=status.HTTP_200_OK)
