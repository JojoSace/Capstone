import pandas as pd
import streamlit as st
from PIL import Image
import plotly.express as px

from plotly.offline import init_notebook_mode, iplot, plot
import plotly as py
init_notebook_mode(connected=True)
import plotly.graph_objs as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Filipino Income and Expenditure", page_icon="🇵🇭", layout="wide")

# Load csv file into pandas dataframe
data = pd.read_csv('Capstone_DW.csv')

# Sort the DataFrame
data.sort_values(by=['Total Household Income'], ascending = True, inplace=True)

# remove unnecessary columns
data.drop(['Unnamed: 0', 'Bread and Cereals Expenditure', 'Total Rice Expenditure', 
                                'Meat Expenditure','Total Fish and  marine products Expenditure', 
                                'Fruit Expenditure', 'Vegetables Expenditure', 
                                'Restaurant and hotels Expenditure', 'Alcoholic Beverages Expenditure', 
                                'Tobacco Expenditure', 'Clothing, Footwear and Other Wear Expenditure', 
                                'Housing and water Expenditure', 'Medical Care Expenditure', 
                                'Transportation Expenditure', 'Communication Expenditure', 
                                'Education Expenditure', 'Miscellaneous Goods and Services Expenditure', 
                                'Special Occasions Expenditure', 'Crop Farming and Gardening expenses', 
                                'Imputed House Rental Value','House Floor Area', 'Electricity', 'Has Electricity',
                                'Main Source of Water Supply'], axis=1, inplace = True)

# Get Columns for each Income Class
employment_poor = data[data['Income Class'] == 'Poor']
employment_middle = data[data['Income Class'] == 'Middle Class']
employment_rich = data[data['Income Class'] == 'Rich']

# Import geomapping images
annual_income = Image.open(".\Plots\Income_by_Region.png")
annual_expenditure = Image.open(".\Plots\Expenditure_by_Region.png")
monthly_income = Image.open(".\Plots\Monthly_Income_by_Region.png")
monthly_expenditure = Image.open(".\Plots\Monthly_Expenditure_by_Region.png")

# ---- MAINPAGE ----
st.title("💸 FILIPINO INCOME AND EXPENDITURE: MULTIVARIATE ANALYSIS")
st.subheader("The Philippines has a high poverty rate, with about 16.6% of the population living below the poverty line. There is a need to understand the factors that contribute to poverty in the Philippines, in order to develop effective policies to alleviate it.")
st.subheader("This dashboard will help you understand the factors that contribute to poverty in the Philippines, in order to develop effective policies to alleviate it.")

st.subheader("The dataset is from a 2018 nationwide Family Income and Expenditure Survey (FIES) conducted every three (3) years by the Philippine Statistics Authority. (https://www.kaggle.com/datasets/grosvenpaul/family-income-and-expenditure)")
st.write(data)
left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Total Instances:")
    st.subheader(f"{data.shape[0]} Household Head")
with right_column:
    st.subheader("Total Features:")
    st.subheader(f"{data.shape[1]} Variables")
st.markdown("""---""")

# ---- SIDEBAR ----
with st.sidebar:
    st.subheader('EXPLOTATORY DATA ANALYSIS')
    st.subheader('Plot Style')
    sidebar_plot = st.selectbox('Select a plot style:',('Histogram (by Income Class)', 'Pie Chart (by Income Class)', 'Geomapping (by Region)'))
    if(sidebar_plot == 'Histogram (by Income Class)'):
        st.subheader('Features')
        sidebar_features = st.selectbox('Select a feature:',('Highest Educational Degree Completed by Household Head', 'Household Head Job or Business Indicator', 'Household Head Class of Worker'))
    elif(sidebar_plot == 'Pie Chart (by Income Class)'):
        st.subheader('Features')
        sidebar_features = st.selectbox('Select a feature:',('Highest Educational Degree Completed by Household Head', 'Household Head Job or Business Indicator', 'Household Head Class of Worker'))  
    elif(sidebar_plot == 'Geomapping (by Region)'):
        st.subheader('Features')
        sidebar_features = st.selectbox('Select a feature:',('Annual Income', 'Annual Expenditure', 'Monthly Income per Capita', 'Monthly Expenditure per Capita'))

# ---- HISTOGRAM ----
if (sidebar_features == 'Highest Educational Degree Completed by Household Head') and (sidebar_plot == 'Histogram (by Income Class)'):
    fig_hist = px.histogram(data, y ='Household Head Highest Grade Completed', 
                   color = 'Income Class', color_discrete_sequence=px.colors.qualitative.Antique)
    fig_hist.update_layout(
        title='Highest Educational Degree Completed by Household Head',
        xaxis_title='Household Head',
        yaxis_title='Highest Educational Degree Completed', 
        font=dict(
            size=20
            )
    )
    fig_hist.update_layout(barmode='group', yaxis={'categoryorder':'total descending'}, height=1000)
    st.plotly_chart(fig_hist, use_container_width=True)
elif (sidebar_features == 'Household Head Job or Business Indicator') and (sidebar_plot == 'Histogram (by Income Class)'):
    fig_hist = px.histogram(data, x ='Household Head Job or Business Indicator', 
                   color = 'Income Class', color_discrete_sequence=px.colors.qualitative.Antique)
    fig_hist.update_layout(
        title='Household Head Job or Business Indicator',
        xaxis_title='Job or Business',
        yaxis_title='Household Head',
        font=dict(
            size=20
            )
    )
    fig_hist.update_layout(barmode='group', yaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig_hist, use_container_width=True)
elif (sidebar_features == 'Household Head Class of Worker') and (sidebar_plot == 'Histogram (by Income Class)'):
    fig_hist = px.histogram(data, y ='Household Head Class of Worker', 
                   color = 'Income Class', color_discrete_sequence=px.colors.qualitative.Antique)
    fig_hist.update_layout(
        title='Household Head Class of Worker',
        xaxis_title='Class of Worker',
        yaxis_title='Household Head',
        font=dict(
            size=20
            )
    )
    fig_hist.update_layout(barmode='group', yaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig_hist, use_container_width=True)

# ---- PIE CHART ----
if (sidebar_features == 'Highest Educational Degree Completed by Household Head') and (sidebar_plot == 'Pie Chart (by Income Class)'):

    # pie chart of grade completed
    values = data['Household Head Highest Grade Completed'].value_counts()
    color = data['Household Head Highest Grade Completed'].value_counts().index
    fig_pie = px.pie(data, values=values, color=color, names=color,
             hole=.3,
             color_discrete_sequence=px.colors.qualitative.Antique)
    fig_pie.update_traces(textposition='inside')
    fig_pie.update_layout(title_text='Highest Educational Degree Completed by Household Head',uniformtext_minsize=15, uniformtext_mode='hide',
                  height=1000, title={'font': {'size': 30}}, font={'size': 20})
    fig_pie.update_layout(barmode='group', yaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig_pie, use_container_width=True)  
    
    #pie chart grade completed by income class
    # Pie Chart Labels
    plabel = employment_poor['Household Head Highest Grade Completed'].value_counts().index
    mlabel = employment_middle['Household Head Highest Grade Completed'].value_counts().index
    rlabel = employment_rich['Household Head Highest Grade Completed'].value_counts().index

    poor = employment_poor['Household Head Highest Grade Completed'].value_counts()
    middle = employment_middle['Household Head Highest Grade Completed'].value_counts()
    rich = employment_rich['Household Head Highest Grade Completed'].value_counts()
    
    specs = [[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]]
    fig_pie_income = make_subplots(rows=1, cols=3, specs=specs, subplot_titles=['Poor', 'Middle Class', 'Rich'])

    fig_pie_income.add_trace(go.Pie(labels=plabel, values = poor,
                     name="Poor"), 
              1, 1)
    fig_pie_income.add_trace(go.Pie(labels=mlabel, values = middle,
                     name="Middle Class"), 
              1, 2)
    fig_pie_income.add_trace(go.Pie(labels=rlabel,  values = rich,
                     name="Rich"), 
              1, 3)

    fig_pie_income.update_traces(textposition='inside', hole=.3)
    fig_pie_income.update_layout(title_text='Household Head Highest Grade Completed by Income Class' ,uniformtext_minsize=10, uniformtext_mode='hide', 
                  height=500)
    fig_pie_income.update_layout(barmode='group', yaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig_pie_income, use_container_width=True)
    
elif (sidebar_features == 'Household Head Job or Business Indicator') and (sidebar_plot == 'Pie Chart (by Income Class)'):

    # pie chart of grade completed
    values = data['Household Head Job or Business Indicator'].value_counts()
    color = data['Household Head Job or Business Indicator'].value_counts().index
    fig_pie = px.pie(data, values=values, color=color, names=color,
             hole=.3,
             color_discrete_sequence=px.colors.qualitative.Antique)
    fig_pie.update_traces(textposition='inside')
    fig_pie.update_layout(title_text='Household Head Job or Business Indicator by Household Head',uniformtext_minsize=15, uniformtext_mode='hide',
                  height=1000, title={'font': {'size': 30}}, font={'size': 20})
    fig_pie.update_layout(barmode='group', yaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig_pie, use_container_width=True)  
    
    #pie chart with job by income class
    # Pie Chart Labels
    plabel = employment_poor['Household Head Job or Business Indicator'].value_counts().index
    mlabel = employment_middle['Household Head Job or Business Indicator'].value_counts().index
    rlabel = employment_rich['Household Head Job or Business Indicator'].value_counts().index

    poor = employment_poor['Household Head Job or Business Indicator'].value_counts()
    middle = employment_middle['Household Head Job or Business Indicator'].value_counts()
    rich = employment_rich['Household Head Job or Business Indicator'].value_counts()

    specs = [[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]]
    fig_pie_income = make_subplots(rows=1, cols=3, specs=specs, subplot_titles=['Poor', 'Middle Class', 'Rich'])

    fig_pie_income.add_trace(go.Pie(labels=plabel, values = poor,
                     name="Poor"), 
              1, 1)
    fig_pie_income.add_trace(go.Pie(labels=mlabel, values = middle,
                     name="Middle Class"), 
              1, 2)
    fig_pie_income.add_trace(go.Pie(labels=rlabel,  values = rich,
                     name="Rich"), 
              1, 3)

    fig_pie_income.update_traces(textposition='inside', hole=.3)
    fig_pie_income.update_layout(title_text='Household Head Job or Business Indicator by Income Class' ,uniformtext_minsize=10, uniformtext_mode='hide', 
                  height=500)
    fig_pie_income.update_layout(barmode='group', yaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig_pie_income, use_container_width=True)
    
elif (sidebar_features == 'Household Head Class of Worker') and (sidebar_plot == 'Pie Chart (by Income Class)'):
    
    # pie chart of grade completed
    values = data['Household Head Class of Worker'].value_counts()
    color = data['Household Head Class of Worker'].value_counts().index
    fig_pie = px.pie(data, values=values, color=color, names=color,
             hole=.3,
             color_discrete_sequence=px.colors.qualitative.Antique)
    fig_pie.update_traces(textposition='inside')
    fig_pie.update_layout(title_text='Household Head Class of Worker by Household Head',uniformtext_minsize=15, uniformtext_mode='hide',
                  height=1000, title={'font': {'size': 30}}, font={'size': 20})
    fig_pie.update_layout(barmode='group', yaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig_pie, use_container_width=True)  
    
    #pie chart with job by income class
    # Pie Chart Labels
    plabel = employment_poor['Household Head Class of Worker'].value_counts().index
    mlabel = employment_middle['Household Head Class of Worker'].value_counts().index
    rlabel = employment_rich['Household Head Class of Worker'].value_counts().index

    poor = employment_poor['Household Head Class of Worker'].value_counts()
    middle = employment_middle['Household Head Class of Worker'].value_counts()
    rich = employment_rich['Household Head Class of Worker'].value_counts()

    specs = [[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]]
    fig_pie_income = make_subplots(rows=1, cols=3, specs=specs, subplot_titles=['Poor', 'Middle Class', 'Rich'])

    fig_pie_income.add_trace(go.Pie(labels=plabel, values = poor,
                     name="Poor"), 
              1, 1)
    fig_pie_income.add_trace(go.Pie(labels=mlabel, values = middle,
                     name="Middle Class"), 
              1, 2)
    fig_pie_income.add_trace(go.Pie(labels=rlabel,  values = rich,
                     name="Rich"), 
              1, 3)

    fig_pie_income.update_traces(textposition='inside', hole=.3)
    fig_pie_income.update_layout(title_text='Household Head Job or Business Indicator by Income Class' ,uniformtext_minsize=10, uniformtext_mode='hide', 
                  height=500)
    fig_pie_income.update_layout(barmode='group', yaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig_pie_income, use_container_width=True)     

# ---- GEOMAPPING ----
if (sidebar_features == 'Annual Income') and (sidebar_plot == 'Geomapping (by Region)'):
    st.image(annual_income, output_format="auto")
elif (sidebar_features == 'Annual Expenditure') and (sidebar_plot == 'Geomapping (by Region)'):
    st.image(annual_expenditure, output_format="auto")
elif (sidebar_features == 'Monthly Income per Capita') and (sidebar_plot == 'Geomapping (by Region)'):
    st.image(monthly_income, output_format="auto")
elif (sidebar_features == 'Monthly Expenditure per Capita') and (sidebar_plot == 'Geomapping (by Region)'):
    st.image(monthly_expenditure, output_format="auto")
    
