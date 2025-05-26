from django.shortcuts import render
import plotly.express as px
from core.models import PersonSalary
from django.db.models import Case, When, Value, CharField, Avg


# Create your views here.


def plot(request):
    person_salaries = PersonSalary.objects.all()

    # 15-19, 20-24, 25-29...
    YEARS_PER_AGG = 5

    age_bins = [(i, i+YEARS_PER_AGG-1) for i in range(15, 85, YEARS_PER_AGG)]
    conditionals = [When(age__range=a_bin, then=Value(f'{a_bin}')) for a_bin in age_bins]

    case = Case(*conditionals, output_field=CharField())

    age_groupings = person_salaries.annotate(age_group=case).values('age_group').order_by('age_group')

    age_groupings_avg = (person_salaries.annotate(age_group=case)
                         .values('age_group')
                         .order_by('age_group')
                         .annotate(avg=Avg('salary')))

    # person_salaries = PersonSalary.objects.filter(education__in=['1. < HS Grad', '5. Advanced Degree'])
    ages = person_salaries.values_list('age', flat=True)
    salaries = person_salaries.values_list('salary', flat=True)

    ages_g = age_groupings.values_list('age_group', flat=True)
    salaries_g = age_groupings.values_list('salary', flat=True)
    color = person_salaries.values_list('education', flat=True)

    ages_avg = age_groupings_avg.values_list('age_group', flat=True)
    salaries_avg = age_groupings_avg.values_list('avg', flat=True)

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
        x=ages_g,
        y=salaries_g,
        title="Salary by age",
        labels={"x": "Age", "y": "Salary"},
        height=800,
    )

    fig2 = px.line(
        x=ages_avg,
        y=salaries_avg,
        title="Salary by age",
        labels={"x": "Age", "y": "Salary"},
        height=800,
    )

    html = fig.to_html()
    html_box = fig1.to_html()
    html_line = fig2.to_html()

    context = {
        'chart': html,
        'chart_box': html_box,
        'chart_line': html_line,
    }
    return render(request, 'scatter.html', context)