import sys
from pathlib import Path

if __package__ in (None, ''):
    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

from fasthtml import FastHTML
from fasthtml.common import *
import matplotlib.pyplot as plt

from employee_events import Employee, Team
from report.utils import load_model

from report.base_components import (
    Dropdown,
    BaseComponent,
    Radio,
    MatplotlibViz,
    DataTable,
)

from report.combined_components import FormGroup, CombinedComponent


class ReportDropdown(Dropdown):
    def build_component(self, entity_id, model):
        self.label = model.name.title()
        return super().build_component(entity_id, model)

    def component_data(self, entity_id, model):
        return model.names()


class Header(BaseComponent):
    def build_component(self, entity_id, model):
        return H1(f'{model.name.title()} Performance')


class LineChart(MatplotlibViz):
    def visualization(self, entity_id, model):
        counts = model.event_counts(entity_id).fillna(0).set_index('event_date').sort_index()
        counts = counts.cumsum()
        counts.columns = ['Positive', 'Negative']
        fig, ax = plt.subplots(figsize=(8, 3))
        counts.plot(ax=ax)
        self.set_axis_styling(ax, bordercolor='black', fontcolor='black')
        ax.set_title(f'{model.name.title()} Event Trend')
        ax.set_xlabel('Date')
        ax.set_ylabel('Cumulative Events')


class BarChart(MatplotlibViz):
    predictor = load_model()

    def visualization(self, entity_id, model):
        data = model.model_data(entity_id)
        probabilities = self.predictor.predict_proba(data)
        probability = probabilities[:, 1]
        pred = probability.mean() if model.name == 'team' else probability[0]
        fig, ax = plt.subplots(figsize=(4, 2))
        ax.barh([''], [pred])
        ax.set_xlim(0, 1)
        ax.set_title('Predicted Recruitment Risk', fontsize=20)
        self.set_axis_styling(ax, bordercolor='black', fontcolor='black')


class Visualizations(CombinedComponent):
    children = [LineChart(), BarChart()]
    outer_div_type = Div(cls='grid')


class NotesTable(DataTable):
    def component_data(self, entity_id, model):
        return model.notes(entity_id)


class DashboardFilters(FormGroup):
    id = 'top-filters'
    action = '/update_data'
    method = 'POST'

    children = [
        Radio(
            values=['Employee', 'Team'],
            name='profile_type',
            hx_get='/update_dropdown',
            hx_target='#selector',
        ),
        ReportDropdown(id='selector', name='user-selection'),
    ]


class Report(CombinedComponent):
    children = [Header(), DashboardFilters(), Visualizations(), NotesTable()]


app = FastHTML()
report = Report()


@app.get('/')
def home():
    return report(1, Employee())


@app.get('/employee/{id:str}')
def employee(id: str):
    return report(int(id), Employee())


@app.get('/team/{id:str}')
def team(id: str):
    return report(int(id), Team())


@app.get('/update_dropdown{r}')
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    profile_type = r.query_params.get('profile_type', 'Employee')
    if profile_type == 'Team':
        return dropdown(None, Team())
    return dropdown(None, Employee())


@app.post('/update_data')
async def update_data(r):
    from fasthtml.common import RedirectResponse
    data = await r.form()
    profile_type = data._dict['profile_type']
    entity_id = data._dict['user-selection']
    if profile_type == 'Employee':
        return RedirectResponse(f'/employee/{entity_id}', status_code=303)
    return RedirectResponse(f'/team/{entity_id}', status_code=303)


if __name__ == '__main__':
    serve()
