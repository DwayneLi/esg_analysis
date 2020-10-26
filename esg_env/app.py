from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import sys
import config


app = Flask(__name__)

app.config.from_object(config)
#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://admin:esglidonghuai123@esgdb.cqvmsusqrmb3.us-east-2.rds.amazonaws.com:3306/esg_db"
#'sqlite:///' + os.path.join(app.root_path, 'data.db')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#C:\Program Files\MySQL\MySQL Workbench 8.0 CE
db = SQLAlchemy(app)


class esg_score(db.Model):
 __tablename__ = 'esg_company'
 id = db.Column(db.Integer, primary_key=True, autoincrement=True)
 Symbol = db.Column(db.String(10))
 Security_name = db.Column(db.String(30))
 GICS_Sector = db.Column(db.String(30), nullable=True)
 # GICS_Sector = db.Column('GICS Sector', db.String(30), nullable=True)
 GICS_Sub_Industry = db.Column(db.String(30), nullable=True)
 # GICS_Sub_Industry = db.Column('GICS Sub-Industry', db.String(30), nullable=True)
 ESG_Score = db.Column(db.Float, nullable=True)
 ESG_Risk = db.Column(db.String(30), nullable=True)
 ESG_Percentile = db.Column(db.String(30), nullable=True)
 Environment_Risk = db.Column(db.Float, nullable=True)
 Social_Risk = db.Column(db.Float, nullable=True)
 Governance_Risk = db.Column(db.Float, nullable=True)
 Controversy_comment = db.Column(db.String(30), nullable=True)
 Controversy_level = db.Column(db.String(30), nullable=True)
 Peer_Controversy_level = db.Column(db.Float, nullable=True)
 execution_date  = db.Column(db.Date, nullable=True)





@app.route('/')
def index():
 tenexample = esg_score.query.filter(esg_score.ESG_Score.isnot(None)).limit(5).all()

 return render_template('index.html', example=tenexample)

import click

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    #user = User.query.first()
    return render_template('404.html'), 404  # 返回模板和状态码

#def insert_esg():










import pandas as pd
#ten = pd.read_csv('tencomp.csv')
#esg10=ten.to_dict(orient='records')
esg10 =[{'Controversy_comment': 'Significant',
  'Controversy_level': 3.0,
  'ESG_Percentile': '72nd percentile',
  'ESG_Risk': 'High',
  'ESG_Score': '35',
  'Environment_Risk': '12.8',
  'GICS Sector': 'Industrials',
  'GICS Sub-Industry': 'Industrial Conglomerates',
  'Governance_Risk': '8.1',
  'Peer_Controversy_level': '2.2',
  'Security': '3M Company',
  'Social_Risk': '14.0',
  'Symbol': 'MMM',
  'date': '2020-10-22'},
 {'Controversy_comment': 'Significant',
  'Controversy_level': 3.0,
  'ESG_Percentile': '56th percentile',
  'ESG_Risk': 'Medium',
  'ESG_Score': '30',
  'Environment_Risk': '3.0',
  'GICS Sector': 'Health Care',
  'GICS Sub-Industry': 'Health Care Equipment',
  'Governance_Risk': '10.6',
  'Peer_Controversy_level': 'None',
  'Security': 'Abbott Laboratories',
  'Social_Risk': '16.2',
  'Symbol': 'ABT',
  'date': '2020-10-22'},
 {'Controversy_comment': 'Significant',
  'Controversy_level': 3.0,
  'ESG_Percentile': '60th percentile',
  'ESG_Risk': 'High',
  'ESG_Score': '31',
  'Environment_Risk': '1.0',
  'GICS Sector': 'Health Care',
  'GICS Sub-Industry': 'Pharmaceuticals',
  'Governance_Risk': '11.8',
  'Peer_Controversy_level': '1.9',
  'Security': 'AbbVie Inc.',
  'Social_Risk': '18.1',
  'Symbol': 'ABBV',
  'date': '2020-10-22'},
 {'Controversy_comment': 'None',
  'Controversy_level': 'None',
  'ESG_Percentile': 'None',
  'ESG_Risk': 'None',
  'ESG_Score': 'None',
  'Environment_Risk': 'None',
  'GICS Sector': 'Health Care',
  'GICS Sub-Industry': 'Health Care Equipment',
  'Governance_Risk': 'None',
  'Peer_Controversy_level': 'None',
  'Security': 'ABIOMED Inc',
  'Social_Risk': 'None',
  'Symbol': 'ABMD',
  'date': '2020-10-22'},
 {'Controversy_comment': 'Moderate',
  'Controversy_level': 2.0,
  'ESG_Percentile': '2nd percentile',
  'ESG_Risk': 'Low',
  'ESG_Score': '11',
  'Environment_Risk': '0.6',
  'GICS Sector': 'Information Technology',
  'GICS Sub-Industry': 'IT Consulting & Other Services',
  'Governance_Risk': '5.7',
  'Peer_Controversy_level': '1.5',
  'Security': 'Accenture plc',
  'Social_Risk': '5.0',
  'Symbol': 'ACN',
  'date': '2020-10-22'},
 {'Controversy_comment': 'Moderate',
  'Controversy_level': 2.0,
  'ESG_Percentile': '11th percentile',
  'ESG_Risk': 'Low',
  'ESG_Score': '17',
  'Environment_Risk': '0.2',
  'GICS Sector': 'Communication Services',
  'GICS Sub-Industry': 'Interactive Home Entertainment',
  'Governance_Risk': '6.2',
  'Peer_Controversy_level': '1.5',
  'Security': 'Activision Blizzard',
  'Social_Risk': '10.5',
  'Symbol': 'ATVI',
  'date': '2020-10-22'},
 {'Controversy_comment': 'Low',
  'Controversy_level': 1.0,
  'ESG_Percentile': '4th percentile',
  'ESG_Risk': 'Low',
  'ESG_Score': '13',
  'Environment_Risk': '0.4',
  'GICS Sector': 'Information Technology',
  'GICS Sub-Industry': 'Application Software',
  'Governance_Risk': '4.9',
  'Peer_Controversy_level': '1.5',
  'Security': 'Adobe Inc.',
  'Social_Risk': '7.9',
  'Symbol': 'ADBE',
  'date': '2020-10-22'},
 {'Controversy_comment': 'None',
  'Controversy_level': 'None',
  'ESG_Percentile': 'None',
  'ESG_Risk': 'None',
  'ESG_Score': 'None',
  'Environment_Risk': 'None',
  'GICS Sector': 'Information Technology',
  'GICS Sub-Industry': 'Semiconductors',
  'Governance_Risk': 'None',
  'Peer_Controversy_level': 'None',
  'Security': 'Advanced Micro Devices Inc',
  'Social_Risk': 'None',
  'Symbol': 'AMD',
  'date': '2020-10-22'},
 {'Controversy_comment': 'Moderate',
  'Controversy_level': 2.0,
  'ESG_Percentile': '3rd percentile',
  'ESG_Risk': 'Low',
  'ESG_Score': '12',
  'Environment_Risk': '0.1',
  'GICS Sector': 'Consumer Discretionary',
  'GICS Sub-Industry': 'Automotive Retail',
  'Governance_Risk': '3.6',
  'Peer_Controversy_level': '1.7',
  'Security': 'Advance Auto Parts',
  'Social_Risk': '8.7',
  'Symbol': 'AAP',
  'date': '2020-10-22'},
 {'Controversy_comment': 'Moderate',
  'Controversy_level': 2.0,
  'ESG_Percentile': '67th percentile',
  'ESG_Risk': 'High',
  'ESG_Score': '33',
  'Environment_Risk': '18.8',
  'GICS Sector': 'Utilities',
  'GICS Sub-Industry': 'Independent Power Producers & Energy Traders',
  'Governance_Risk': '5.8',
  'Peer_Controversy_level': '1.8',
  'Security': 'AES Corp',
  'Social_Risk': '8.6',
  'Symbol': 'AES',
  'date': '2020-10-22'}]

if __name__ == 'main':
 app.run(debug=True)