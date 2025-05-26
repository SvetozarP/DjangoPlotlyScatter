from django.shortcuts import render
import plotly.express as px
from core.models import PersonSalary


# Create your views here.


def plot(request):
    person_salaries = PersonSalary.objects.all()
    # person_salaries = PersonSalary.objects.filter(education__in=['1. < HS Grad', '5. Advanced Degree'])
    ages = person_salaries.values_list('age', flat=True)
    salaries = person_salaries.values_list('salary', flat=True)
    color = person_salaries.values_list('education', flat=True)

    fig = px.scatter(
        x=ages,
        y=salaries,
        title="Salary by age",
        labels={"x": "Age", "y": "Salary"},
        height=800,
        trendline="ols",
        color=color,
    )

    fig1 = px.box(
        x=ages,
        y=salaries,
        title="Salary by age",
        labels={"x": "Age", "y": "Salary"},
        height=800,
    )

    html = fig.to_html()
    html_box = fig1.to_html()

    context = {
        'chart': html,
        'chart_box': html_box,
    }
    return render(request, 'scatter.html', context)