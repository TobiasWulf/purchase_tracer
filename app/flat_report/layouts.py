import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
# from flask import redirect, url_for


navbar = dbc.NavbarSimple(
    children=[
        # dbc.NavItem(dbc.NavLink(current_user.username, href=url_for('main.user', username=current_user.username))),
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Menu",
            children=[
                dbc.DropdownMenuItem("Overall Summary"),
                dbc.DropdownMenuItem("Monthly Summary"),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("User Summary"),
            ],
        ),
    ],
    brand="Purchase Tracer",
    brand_href='#',
    sticky="top",
)

body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("Flat Report"),
                        dcc.Dropdown(
                            id='my-dropdown',
                            options=[
                                {'label': 'Coke', 'value': 'COKE'},
                                {'label': 'Tesla', 'value': 'TSLA'},
                                {'label': 'Apple', 'value': 'AAPL'}
                            ],
                            value='COKE'
                        ),
                        dcc.Graph(id='my-graph')
                    ]
                )
            ]
        )
    ],
    className='mt-4'
)

layout = html.Div([navbar, body])
