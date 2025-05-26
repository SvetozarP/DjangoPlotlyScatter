from django.shortcuts import render
import plotly.express as px
from core.models import PersonSalary


# Create your views here.


def plot(request):
    person_salaries = PersonSalary.objects.all()
    ages = person_salaries.values_list('age', flat=True)
    salaries = person_salaries.values_list('salary', flat=True)

    fig = px.scatter(
        x=ages,
        y=salaries,
        title="Salary by age",
        labels={"x": "Age", "y": "Salary"},
        height=800,
        trendline="ols",
    )

    html = fig.to_html()

    context = {'chart': html}
    return render(request, 'scatter.html', context)