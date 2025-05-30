# app/views.py

from django.shortcuts import render, redirect
from .Blockchain_module import create_health_id, search_patient_by_id
from . import final_diet_system_

def index(request):
    return render(request, 'index.html')

def health_id(request):
    return render(request, 'health-id.html')

def create_plan(request):
    return render(request, 'plan.html')

def diet(request):
    if request.method == 'POST':
        # Get all form fields
        hospital = request.POST.get('hospital')
        doctor = request.POST.get('doctor')
        patient_name = request.POST.get('patient_name')
        age = request.POST.get('age')
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        issues = request.POST.get('issues')
        suggestions = request.POST.get('suggestions')

        data = {
            "Hospital": hospital,
            "Doctor": doctor,
            "Patient Name": patient_name,
            "Age": int(age),
            "Weight": float(weight),
            "Height": float(height),
            "Issues": issues,
            "Suggestions": suggestions
        }

        patient_id, previous_hash, current_hash = create_health_id(data)
        
        
        return render(request, 'success.html', {"patient_id": patient_id, "current_hash":current_hash, "previous_hash":previous_hash, "hospital": hospital, "doctor": doctor, "patient_name": patient_name, "age": age, "weight": weight, "height": height, "issues": issues, "suggestions": suggestions})

    return render(request, 'diet.html')

def retrieve_patient(request):
    if request.method == "POST":
        patient_id = request.POST.get('patient_id')
        patient = search_patient_by_id(patient_id)

        if patient:
            return render(request, "retrieve.html", {"patient": patient})
        else:
            return render(request, "retrieve.html", {"not_found": True})

    return render(request, "retrieve.html")


def generate_plan(request):
    if request.method == "POST":
        age = int(request.POST.get('age'))
        weight = float(request.POST.get('weight'))
        height = float(request.POST.get('height'))
        goal = request.POST.get('goal')
        diabetes = request.POST.get('diabetes')
        diet_preference = "veg" if request.POST.get('diet_preference') == "veg" else "nonveg"

        # Now pass the parameters to final_diet_system_
        diet_plan = final_diet_system_.generate_diet_plan_from_input(
            age, diet_preference, weight, height, goal, diabetes
        )

        # Send diet_plan to HTML
        return render(request, 'diet_result.html', {'diet_plan': diet_plan})

    return render(request, 'plan.html')