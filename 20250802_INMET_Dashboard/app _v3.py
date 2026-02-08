import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, dash_table, Input, Output

FILE_PATH = "A318_2025.csv"
MESES = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro"
}

# Read file
df = pd.read_csv(FILE_PATH, sep=";")
df.columns = df.columns.str.strip()

# Create a datetime column
df["Hora (UTC)"] = df["Hora (UTC)"].astype(str).str.zfill(4)
df["Datetime"] = pd.to_datetime(
    df["Data"] + " " + df["Hora (UTC)"],
    format="%d/%m/%Y %H%M"
)

# Correct all numeric column types and account for decimal separator
colunas = [
    "Temp. Ins. (C)", "Temp. Max. (C)", "Temp. Min. (C)",
    "Umi. Ins. (%)", "Umi. Max. (%)", "Umi. Min. (%)",
    "Pressao Ins. (hPa)", "Pressao Max. (hPa)", "Pressao Min. (hPa)",
    "Vel. Vento (m/s)", "Dir. Vento (m/s)", "Raj. Vento (m/s)",
    "Radiacao (KJ/m²)", "Chuva (mm)"
]

for c in colunas:
    df[c] = df[c].astype(str).str.replace(",", ".").astype(float)

# Create a column 'month' for monthly average calculations
df["Mes"] = df["Datetime"].dt.month
df["Mes_nome"] = df["Mes"].map(MESES)

# Drop NaN values
df = df.dropna(subset=["Vel. Vento (m/s)", "Dir. Vento (m/s)"])

# Calculate monthly averages
df_mensal = df.groupby("Mes")[["Vel. Vento (m/s)", "Temp. Ins. (C)", "Umi. Ins. (%)"]].mean().reset_index()
df_mensal["Mes_nome"] = df_mensal["Mes"].map(MESES)

######## Start of Dash #########
app = Dash(__name__)

# Define standard structure for cards
def card(children):

    return html.Div(
        children,
        style={
            "backgroundColor": "white",
            "borderRadius": "12px",
            "padding": "20px",
            "boxShadow": "0 2px 6px rgba(0,0,0,0.08)",
            "marginBottom": "25px"
        }
    )

def kpi_card(titulo, kpi_id):

    return html.Div(

        style={
            "backgroundColor": "white",
            "borderRadius": "12px",
            "padding": "20px",
            "boxShadow": "0 2px 6px rgba(0,0,0,0.08)",
            "textAlign": "center"
        },

        children=[

            html.P(
                titulo,
                style={
                    "color": "#64748B",
                    "marginBottom": "8px",
                    "fontSize": "14px"
                }
            ),

            html.H2(
                "--",
                id=kpi_id,
                style={
                    "margin": "0",
                    "color": "#1E293B"
                }
            )

        ]
    )


# start of layout
app.layout = html.Div(

    style={
        "backgroundColor": "#F5F7FA",
        "minHeight": "100vh",
        "padding": "30px"
    },
    children=[
        html.Div(
            # To keep everything in the same page width
            style={
                "maxWidth": "1300px",
                "margin": "auto",
                "fontFamily": "Inter, Arial, sans-serif"
            },
            children=[
                card([

                    html.H1("Dashboard Meteorológico",
                            style={"color": "#1E293B"}),

                    html.P("Dados INMET • Ano 2025",
                           style={"color": "#64748B"})

                ]),
                card([
                    html.Label(
                        "Selecione o mês",
                        style={
                            "fontWeight": "600",
                            "marginBottom": "8px",
                            "display": "block"
                        }
                    ),
                    dcc.Dropdown(
                        id="filtro-mes",

                        options=[{"label": "Todos", "value": "Todos"}] + [
                            {"label": MESES[m], "value": MESES[m]}
                            for m in sorted(df["Mes"].unique())
                        ],

                        value="Todos",
                        clearable=False,

                        style={"width": "250px"}
                    )
                ]),

                # Start of KPIs
                html.Div(
                    style={
                        "display": "grid",
                        "gridTemplateColumns": "repeat(5, 1fr)",
                        "gap": "20px",
                        "marginBottom": "25px"
                    },
                    children=[

                        kpi_card("Velocidade Média", "kpi-vento"),
                        kpi_card("Temperatura Média", "kpi-temp"),
                        kpi_card("Umidade Média", "kpi-umi"),
                        kpi_card("Pressão Média", "kpi-press"),
                        kpi_card("Direção Média", "kpi-dir")

                    ]
                ),
                # Graphs
                html.Div(
                    style={
                        "display": "grid",
                        "gridTemplateColumns": "1fr 1fr",
                        "gap": "25px"
                    },
                    children=[

                        card(dcc.Graph(id="serie-vento")),
                        card(dcc.Graph(id="serie-temp")),
                        card(dcc.Graph(id="serie-umi")),
                        card(dcc.Graph(id="serie-pressao"))

                    ]
                ),
                html.Div(
                    style={
                        "display": "grid",
                        "gridTemplateColumns": "1fr 1fr",
                        "gap": "25px"
                    },
                    children=[
                        card(dcc.Graph(id="media-vento")),
                        card(dcc.Graph(id="media-temp-umi"))
                    ]
                ),
                # Histogram + windrose
                html.Div(

                    style={
                        "display": "grid",
                        "gridTemplateColumns": "1fr 1fr",
                        "gap": "25px"
                    },

                    children=[

                        card(dcc.Graph(id="hist")),
                        card(dcc.Graph(id="rosa"))

                    ]
                ),
                # Table
                card([
                    html.H3("Base de Dados"),
                    dash_table.DataTable(
                        id="tabela",
                        columns=[
                            {"name": c, "id": c}
                            for c in df.columns
                        ],
                        page_size=15,
                        filter_action="native",
                        sort_action="native",
                        style_table={"overflowX": "auto"},
                        style_header={
                            "backgroundColor": "#F1F5F9",
                            "fontWeight": "600"
                        },
                        style_cell={
                            "textAlign": "center",
                            "fontSize": "13px",
                            "padding": "6px"
                        }
                    )
                ])
            ]
        )
    ]
)

def serie_com_box(dados, x, y, titulo, unidade):
    """Plot the scatter + box plots"""
    fig = make_subplots(
        rows=1,
        cols=2,
        column_widths=[0.25, 0.75],
        shared_yaxes=True
    )
    fig.add_trace(
        go.Box(
            y=dados[y],
            boxmean=True,
            name="",
            showlegend=False
        ),
        row=1,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=dados[x],
            y=dados[y],
            mode="lines"
        ),
        row=1,
        col=2
    )

    fig.update_layout(
        title=titulo,
        height=380,
        showlegend=False,
        margin=dict(l=40, r=20, t=50, b=40),
        font=dict(size=12)
    )

    fig.update_yaxes(title_text=unidade, row=1, col=2)
    fig.update_xaxes(showticklabels=False, row=1, col=1)
    return fig

@app.callback(

    Output("serie-vento", "figure"),
    Output("serie-temp", "figure"),
    Output("serie-umi", "figure"),
    Output("serie-pressao", "figure"),

    Output("media-vento", "figure"),
    Output("media-temp-umi", "figure"),

    Output("hist", "figure"),
    Output("rosa", "figure"),

    Output("tabela", "data"),

    Output("kpi-vento", "children"),
    Output("kpi-temp", "children"),
    Output("kpi-umi", "children"),
    Output("kpi-press", "children"),
    Output("kpi-dir", "children"),

    Input("filtro-mes", "value")

)
def atualizar(mes):
    if mes == "Todos":
        dados = df.copy()
    else:
        dados = df[df["Mes_nome"] == mes]

    # Means for KPIs
    vento = round(dados["Vel. Vento (m/s)"].mean(), 2)
    temp = round(dados["Temp. Ins. (C)"].mean(), 1)
    umi = round(dados["Umi. Ins. (%)"].mean(), 1)
    press = round(dados["Pressao Ins. (hPa)"].mean(), 1)
    dir_vento =  round(dados["Dir. Vento (m/s)"].mean(), 1)

    # Scatters and boxplot
    fig_vento = serie_com_box(
        dados, "Datetime", "Vel. Vento (m/s)",
        "Velocidade do Vento", "m/s"
    )

    fig_temp = serie_com_box(
        dados, "Datetime", "Temp. Ins. (C)",
        "Temperatura", "°C"
    )

    fig_umi = serie_com_box(
        dados, "Datetime", "Umi. Ins. (%)",
        "Umidade", "%"
    )

    fig_press = serie_com_box(
        dados, "Datetime", "Pressao Ins. (hPa)",
        "Pressão", "hPa"
    )

    # Mean bargraphs
    fig_media_vento = px.bar(
        df_mensal,
        x="Mes_nome",
        y="Vel. Vento (m/s)",
        title="Velocidade Média Mensal"
    )
    fig_media_vento.update_xaxes(title="")

    fig_temp_umi = make_subplots(specs=[[{"secondary_y": True}]])
    fig_temp_umi.add_bar(
        x=df_mensal["Mes_nome"],
        y=df_mensal["Temp. Ins. (C)"],
        name="Temperatura",
        secondary_y=False
    )

    fig_temp_umi.add_bar(
        x=df_mensal["Mes_nome"],
        y=df_mensal["Umi. Ins. (%)"],
        name="Umidade",
        secondary_y=True
    )

    fig_temp_umi.update_layout(
        title="Temperatura e Umidade Médias",
        barmode="group"
    )

    fig_temp_umi.update_xaxes(title="")

    # Histogram
    fig_hist = px.histogram(
        dados,
        x="Vel. Vento (m/s)",
        nbins=25,
        title="Distribuição do Vento"
    )

    # windrose
    fig_rosa = px.bar_polar(
        dados,
        # r="Vel. Vento (m/s)",
        theta="Dir. Vento (m/s)",
        direction="clockwise",
        start_angle=90,
        title="Rosa dos Ventos"
    )

    tabela = dados.to_dict("records")

    return (
        fig_vento,
        fig_temp,
        fig_umi,
        fig_press,
        fig_media_vento,
        fig_temp_umi,
        fig_hist,
        fig_rosa,
        tabela,
        f"{vento} m/s",
        f"{temp} °C",
        f"{umi} %",
        f"{press} hPa",
        f"{dir_vento} °"
    )

if __name__ == "__main__":

    app.run(debug=True)
