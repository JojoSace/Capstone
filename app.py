import pandas as pd
import streamlit as st
from PIL import Image
import plotly.express as px


import plotly as py
import plotly.graph_objs as go
from plotly.subplots import make_subplots

#---- PREPARE DATA --

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
                                'Main Source of Water Supply', 'Has Formal Education','Household Head Occupation',
                                'Total Income from Entrepreneurial Acitivites'], axis=1, inplace = True)

# Get Columns for each Income Class
employment_poor = data[data['Income Class'] == 'Poor']
employment_middle = data[data['Income Class'] == 'Middle Class']
employment_rich = data[data['Income Class'] == 'Rich']

# Import geomapping images
annual_income = Image.open(".\Income_by_Region.png")
annual_expenditure = Image.open(".\Expenditure_by_Region.png")
monthly_income = Image.open(".\Monthly_Income_by_Region.png")
monthly_expenditure = Image.open(".\Monthly_Expenditure_by_Region.png")

# ---- FUNCTIONS ----

# Dataset Function
def dataset():
    st.title("DATASET OVERVIEW")
    st.write(data)
    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader("Total Instances:")
        st.subheader(f"{data.shape[0]} Families")
    with right_column:
        st.subheader("Total Features:")
        st.subheader(f"{data.shape[1]} Variables")
    st.markdown("""---""") 

# Histogram Function
def histogram_x(value):
    st.title(value)
    fig_hist = px.histogram(data, x =value, 
                   color = 'Income Class', color_discrete_sequence=px.colors.qualitative.Antique)
    fig_hist.update_layout(
        xaxis_title=value.replace('Household Head', ''),
        yaxis_title='Household Head',
        font=dict(
            size=20
            )
    )
    fig_hist.update_layout(barmode='group', height=800, yaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig_hist, use_container_width=True)
def histogram_y(value):
    st.title(value)
    fig_hist = px.histogram(data, y = value, 
                    color = 'Income Class', color_discrete_sequence=px.colors.qualitative.Antique)
    fig_hist.update_layout(
        yaxis_title=value.replace('Household Head', ''),
        xaxis_title='Household Head',
        font=dict(
            size=20
            )
    )
    fig_hist.update_layout(barmode='group', height=800, yaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig_hist, use_container_width=True)
    
# Pie Chart Function

st.set_page_config(page_title="FILIPINO INCOME AND EXPENDITURE DASHBOARD", page_icon="🇵🇭", layout="wide")
st.title("🇵🇭 FILIPINO INCOME AND EXPENDITURE: MULTIVARIATE ANALYSIS")

# ---- SIDEBAR ----
with st.sidebar:
    st.subheader('📖 EXPLORATORY DATA ANALYSIS')
    st.subheader('📊 Plot Style')
    sidebar_plot = st.selectbox('Select a plot style:',('Histogram (by Income Class)', 'Pie Chart (by Income Class)', 'Geomapping (by Region)'))
    if(sidebar_plot == 'Histogram (by Income Class)'):
        st.subheader('📂 Features')
        sidebar_features = st.selectbox('Select a feature:',('Main Source of Income', 'Household Head Highest Grade Completed', 'Household Head Job or Business Indicator', 'Household Head Class of Worker'))
        status = st.radio("Select Orientation: ", ('Vertical', 'Horizontal'))
    elif(sidebar_plot == 'Pie Chart (by Income Class)'):
        st.subheader('📂 Features')
        sidebar_features = st.selectbox('Select a feature:',('Main Source of Income', 'Highest Educational Degree Completed by Household Head', 'Household Head Job or Business Indicator', 'Household Head Class of Worker'))  
    elif(sidebar_plot == 'Geomapping (by Region)'):
        st.subheader('📂 Features')
        sidebar_features = st.selectbox('Select a feature:',('Annual Income', 'Annual Expenditure', 'Monthly Income per Capita', 'Monthly Expenditure per Capita'))


# ---- HISTOGRAM ----
if (sidebar_plot == 'Histogram (by Income Class)') and (sidebar_features == 'Main Source of Income'):
    if (status == 'Vertical'):
        histogram_x(sidebar_features)
    else:
        histogram_y(sidebar_features)
    if st.checkbox("VIEW DATASET"):
        dataset()
elif (sidebar_plot == 'Histogram (by Income Class)') and (sidebar_features == 'Household Head Highest Grade Completed'):
    if (status == 'Vertical'):
        histogram_x(sidebar_features)
    else:
        histogram_y(sidebar_features)
    if st.checkbox("VIEW DATASET"):
        dataset()
elif (sidebar_plot == 'Histogram (by Income Class)') and (sidebar_features == 'Household Head Job or Business Indicator'):
    if (status == 'Vertical'):
        histogram_x(sidebar_features)
    else:
        histogram_y(sidebar_features)
    if st.checkbox("VIEW DATASET"):
        dataset()
elif (sidebar_plot == 'Histogram (by Income Class)') and (sidebar_features == 'Household Head Class of Worker'):
    if (status == 'Vertical'):
        histogram_x(sidebar_features)
    else:
        histogram_y(sidebar_features)
    if st.checkbox("VIEW DATASET"):
        dataset()
        
# ---- PIE CHART ----
if (sidebar_features == 'Main Source of Income') and (sidebar_plot == 'Pie Chart (by Income Class)'):
    st.title('Main Source of Income by Household Head')
    
    #pie chart main source of income by household head
    labels = data['Main Source of Income'].value_counts().index
    values = data['Main Source of Income'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_traces(textposition='inside', hole=.3)
    fig.update_layout(uniformtext_minsize=20, uniformtext_mode='hide',
                  height=1000)
    st.plotly_chart(fig, use_container_width=True)
    
    #pie chart source of income by income class
    st.title('Main Source of Income by Income Class')
    # Pie Chart Labels
    plabel = employment_poor['Main Source of Income'].value_counts().index
    mlabel = employment_middle['Main Source of Income'].value_counts().index
    rlabel = employment_rich['Main Source of Income'].value_counts().index

    poor = employment_poor['Main Source of Income'].value_counts()
    middle = employment_middle['Main Source of Income'].value_counts()
    rich = employment_rich['Main Source of Income'].value_counts()
    
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
    fig_pie_income.update_layout(uniformtext_minsize=15, uniformtext_mode='hide', 
                  height=500)
    st.plotly_chart(fig_pie_income, use_container_width=True)
    
    if st.checkbox("VIEW DATASET"):
        dataset()
    
elif (sidebar_features == 'Highest Educational Degree Completed by Household Head') and (sidebar_plot == 'Pie Chart (by Income Class)'):
    st.title('Highest Educational Degree Completed by Household Head')
    
    #pie chart highest educational degree by household head
    labels = data['Household Head Highest Grade Completed'].value_counts().index
    values = data['Household Head Highest Grade Completed'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_traces(textposition='inside', hole=.3)
    fig.update_layout(uniformtext_minsize=20, uniformtext_mode='hide',
                  height=1000)
    st.plotly_chart(fig, use_container_width=True)
    
    #pie chart grade completed by income class
    st.title('Highest Educational Degree Completed by Income Class')
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
    fig_pie_income.update_layout(uniformtext_minsize=15, uniformtext_mode='hide', 
                  height=500)
    st.plotly_chart(fig_pie_income, use_container_width=True)
    
    if st.checkbox("VIEW DATASET"):
        dataset()
    
elif (sidebar_features == 'Household Head Job or Business Indicator') and (sidebar_plot == 'Pie Chart (by Income Class)'):
    st.title('Household Head Job or Business Indicator by Household Head')
    
    #pie chart household head job or business by household head
    labels = data['Household Head Job or Business Indicator'].value_counts().index
    values = data['Household Head Job or Business Indicator'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_traces(textposition='inside', hole=.3)
    fig.update_layout(uniformtext_minsize=20, uniformtext_mode='hide',
                  height=1000)
    st.plotly_chart(fig, use_container_width=True)
    
    #pie chart head job or business by income class
    st.title('Household Head Job or Business Indicator by Income Class')
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
    fig_pie_income.update_layout(uniformtext_minsize=15, uniformtext_mode='hide', 
                  height=500)
    st.plotly_chart(fig_pie_income, use_container_width=True)
    
    if st.checkbox("VIEW DATASET"):
        dataset()
    
elif (sidebar_features == 'Household Head Class of Worker') and (sidebar_plot == 'Pie Chart (by Income Class)'):
    st.title('Household Head Job or Business Indicator by Household Head')
    
    #pie chart main source of income by household head
    labels = data['Household Head Job or Business Indicator'].value_counts().index
    values = data['Household Head Job or Business Indicator'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_traces(textposition='inside', hole=.3)
    fig.update_layout(uniformtext_minsize=20, uniformtext_mode='hide',
                  height=1000)
    st.plotly_chart(fig, use_container_width=True)
    
    #pie chart source of income by income class
    st.title('Household Head Job or Business Indicator by Income Class')
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
    fig_pie_income.update_layout(uniformtext_minsize=15, uniformtext_mode='hide', 
                  height=500)
    st.plotly_chart(fig_pie_income, use_container_width=True)
    
    if st.checkbox("VIEW DATASET"):
        dataset()  

# ---- GEOMAPPING ----
if (sidebar_features == 'Annual Income') and (sidebar_plot == 'Geomapping (by Region)'):
    st.image(annual_income, output_format="auto")
    
    if st.checkbox("VIEW DATASET"):
        dataset()

elif (sidebar_features == 'Annual Expenditure') and (sidebar_plot == 'Geomapping (by Region)'):
    st.image(annual_expenditure, output_format="auto")
    
    if st.checkbox("VIEW DATASET"):
        dataset()

elif (sidebar_features == 'Monthly Income per Capita') and (sidebar_plot == 'Geomapping (by Region)'):
    st.image(monthly_income, output_format="auto")
    
    if st.checkbox("VIEW DATASET"):
        dataset()

elif (sidebar_features == 'Monthly Expenditure per Capita') and (sidebar_plot == 'Geomapping (by Region)'):
    st.image(monthly_expenditure, output_format="auto")
    
    if st.checkbox("VIEW DATASET"):
        dataset()   
