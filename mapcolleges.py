import json
import plotly.graph_objects as go

with open('univ.json', 'r') as infile:
    univ_data = json.load(infile)

with open('schools.geojson', 'r') as infile:
    schools_geojson = json.load(infile)


big_12_schools = [school for school in univ_data if school['NCAA'].get('NAIA conference number football (IC2020)') == 108]

univ_dict = {school['instnm']: school for school in big_12_schools}

plot_data = []
for feature in schools_geojson['features']:
    school_name = feature['properties']['NAME']
    if school_name in univ_dict:
        university = univ_dict[school_name]
        plot_data.append({
            'name': school_name,
            'street': feature['properties'].get('STREET'),
            'city': feature['properties'].get('CITY'),
            'state': feature['properties'].get('STATE'),
            'zip': feature['properties'].get('ZIP'),
            'total_enrollment': university['Total  enrollment (DRVEF2020)'],
            'female_enrollment': int((university['Percent of total enrollment that are women (DRVEF2020)']) * (university['Total  enrollment (DRVEF2020)']) / 100),
            'male_enrollment': int((university['Total  enrollment (DRVEF2020)'] - ((university['Percent of total enrollment that are women (DRVEF2020)'] * university['Total  enrollment (DRVEF2020)']) / 100))),
            'latitude': feature['geometry']['coordinates'][1],
            'longitude': feature['geometry']['coordinates'][0]
        })

fig = go.Figure()


for school in plot_data:
    fig.add_trace(go.Scattergeo(
        text=f"{school['name']}<br>{school['street']},{school['city']},{school['state']},{school['zip']}<br>Total Enrollment: {school['total_enrollment']}<br>Female Enrollment: {school['female_enrollment']}<br>Male Enrollment: {school['male_enrollment']}",
        marker=dict(size=15,color='darkblue', line_color='white'),
        lon=[school['longitude']],
        lat=[school['latitude']],
        name=school['name']
    ))

fig.update_layout(
    title_text='Big 12 Schools Information',
    geo=dict(
        scope='usa',
        projection_type='albers usa',
        landcolor ="lightgray"
    )
)

fig.show()
