import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_bar_chart(data_dict, title, x_label, y_label):
    # crée un graphique en barres 
    df = pd.DataFrame(list(data_dict.items()), columns=[x_label, y_label])
    fig = df.sort_values(y_label, ascending=False)
    
    fig = px.bar(fig, x=x_label, y=y_label, title=title, color=y_label, color_continuous_scale='Viridis')
    fig.update_layout(showlegend=False, height=400)
    return fig

def create_pie_chart(data_dict, title):
    # Crée un graphique circulaire 
    fig = go.Figure(data=[go.Pie(labels=list(data_dict.keys()), values=list(data_dict.values()), hole=0.3)])
    fig.update_layout(title=title, height=400)
    return fig

def create_histogram(df, column, title, x_label):
    # crée un histogramme
    fig = px.histogram(df, x=column, title=title, labels={column: x_label}, color_discrete_sequence=['#636EFA'])
    fig.update_layout(height=400)
    return fig

def validate_email(email):
    # Valide le format de l'email
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_github(url):
    # Valide le format de l'URL GitHub
  if not url:
      return True
  return url.startswith('https://github.com/') or url == ''