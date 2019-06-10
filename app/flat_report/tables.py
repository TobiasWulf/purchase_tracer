import pandas as pd
import dash
import dash_table
from dash.dependencies import Input, Output
from app.models import Purchase
from app import db


_page_size = 5
_purchase_df =

purchases_table = dash_table.DataTable(
    id='purchases_table',
    columns=[
        {'name': i, 'id': i, 'deletable': True} for i in sorted(df.columns)
    ],
    pagination_settings={
        'current_page': 0,
        'page_size': PAGE_SIZE
    },
    pagination_mode='be',

    filtering='be',
    filter='',

    sorting='be',
    sorting_type='multi',
    sort_by=[]
)


operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]