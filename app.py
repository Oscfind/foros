from dash import Dash, html, dcc, Input, Output, State  
import dash_bootstrap_components as dbc  
from src.api.workflows.FAQs.extract_FAQs import obtener_faqs, obtener_faqs_unir  
from src.api.common.dependency_container import DependencyContainer  
faqs = obtener_faqs(); faqs_unir = obtener_faqs_unir()
DC = DependencyContainer(); DC.initialize()  
  

app = Dash(__name__, external_stylesheets=[dbc.themes.MATERIA])  
server = app.server

app.layout = dbc.Container(  
    [  
        dbc.Row(dbc.Col(html.H1("FAQ's Becat - Pregunta Respuesta", className="text-center mb-4", style={'font-size': '2.5em'}))),  
        dbc.Row(  
            dbc.Col(  
                [  
                    dcc.Loading(id="loading", type="default", children=html.Div(id='chat_area', style={'height': '520px', 'overflow': 'auto', 'padding': '10px', 'border': '1px solid #ccc', 'border-radius': '5px'})),  
                    dcc.Input(id='user_input', type='text', placeholder='Escribe tu pregunta...', style={'width': '100%', 'height': '50px', 'font-size': '1.2em', 'margin-top': '20px', 'border-radius': '5px'}),  
                    dbc.Button('Enviar', id='send_button', n_clicks=0, className="btn btn-primary mt-2", style={'width': '100%'})  
                ],  
                width=12  
            )  
        )  
    ],  
    fluid=True,  
    style={'max-width': '1200px', 'padding': '20px', 'font-family': 'Comic Sans MS', 'color': '#333'}  
)  
  
@app.callback(  
    Output('chat_area', 'children'),  
    Input('send_button', 'n_clicks'),  
    State('user_input', 'value'),  
    prevent_initial_call=True  
)  

def update_chat(n_clicks, user_input):  
    if user_input is None: return ""  
    request = {'Pregunta': user_input, 'FAQs': faqs + faqs_unir}  
    response = DependencyContainer.get_faqs_workflow().execute(request)
    faq = max(response['FAQs'], key=lambda x: float(x['Score']))
    if float(faq['Score']) >= 7: content = f"<h2>{faq['FAQ']}</h2>{faq['Contenido']}" 
    if 4 < float(faq['Score']) < 7: 
        content = f"""
                    <h2>{faq['FAQ']}</h2>{faq['Contenido']}
                    <h2>Si esta FAQ no se ajusta a tu pregunta, puedes dirigirte al siguiente número de Whatsapp: <a href="https://web.whatsapp.com/send?phone=34689909323">Contacta con un asesor.</a></h2>
        """
    if float(faq['Score']) <= 4: content = f'<h2>No encontramos ninguna FAQ relacionada a la pregunta. Dirígete al siguiente número de Whatsapp: <a href="https://web.whatsapp.com/send?phone=34689909323">contacta con un asesor.</a></h2>'
    return html.Div(html.Iframe(srcDoc=content, style={'width': '100%', 'height': '500px', 'border': 'none'}))  
  
if __name__ == '__main__':  
    app.run_server(debug=False)  