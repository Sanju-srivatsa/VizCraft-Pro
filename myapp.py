# Import necessary libraries
import pandas as pd
import plotly.express as px
import streamlit as st
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

# Set the configuration for the Streamlit page and theme
st.set_page_config(
    page_title='VizCraft',  # Title of the web page
    page_icon='🗿',  # Icon for the web page
    layout="wide"
)

# Custom CSS to style the tab headings
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab"] {
        font-size: 24px !important;
        font-weight: bold !important;
        color: #333 !important;
        background-color: #f0f0f0 !important;
        padding: 10px !important;
        border-radius: 10px !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #f63366 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar for file upload or example dataset
with st.sidebar:
    st.title("VizCraft")
    st.subheader("Data is Everything")
    st.markdown(
        """VizCraft is a powerful and user-friendly web application built with Streamlit that allows you to upload, explore, 
        analyze, and visualize datasets in CSV and Excel formats. This tool is ideal for data analysts, scientists, and anyone 
        interested in gaining insights from their data quickly and easily."""
    )
    #st.header("EAD Functionalities")
    #st.success("Connected ", icon="💚")
    st.sidebar.markdown("""
    [Example CSV input file](https://raw.githubusercontent.com/Sanju-srivatsa/VizCraft-Data-Science-App/main/titanic.csv)
    """)

# Display the title and subtitle of the web app
st.title('VizCraft: Interactive Data Navigator')
st.subheader('Explore, Analyze, and Visualize All in One Place.')

# Add spacing between title and file uploader
st.markdown("---")  # Horizontal rule for separation



# Initialize the `data` variable and the `is_example` flag
data = None
is_example = False

# File uploader component to upload CSV or Excel files
file = st.file_uploader('Drop csv or excel file', type=['csv', 'xlsx'])

# Check if the file is uploaded or load the example dataset
if file is not None:
    # Read the file based on its extension (CSV or Excel)
    if file.name.endswith('csv'):
        data = pd.read_csv(file)  # Read CSV file
    else:
        data = pd.read_excel(file)  # Read Excel file
else:
    if st.button('Press to use Example Dataset'):
        # Load the example dataset if no file is uploaded
        data = pd.read_csv('https://raw.githubusercontent.com/Sanju-srivatsa/VizCraft-Data-Science-App/main/titanic.csv')
        is_example = True  # Set flag to indicate that the example dataset is being used
        st.success('Example dataset loaded!')

# Ensure the tabs are displayed if data is available
if data is not None:
    # Display the uploaded data in a dataframe format
    st.subheader('Input Dataframe')
    st.dataframe(data)
    st.info('File is Successfully Loaded', icon='💡')
    st.markdown("---")

    # Create main tabs for the different sections
    main_tab1, main_tab2, main_tab3, main_tab4 = st.tabs(
        ['Pandas Profiling Report', 'Dataset Overview', 'Columns Values to Count', 'Groupby: Simplify Your Data Analysis'])

    # Tab 1: Pandas Profiling Report
    with main_tab1:
        st.subheader('Pandas Profiling Report')
        with st.spinner('Generating Pandas Profiling Report...'):
            pr = ProfileReport(data, explorative=True)
            st_profile_report(pr)

    # Tab 2: Basic Info About the Dataset
    with main_tab2:
        st.subheader('Dataset Overview')
        # Create subtabs for different types of information about the dataset
        tab1, tab2, tab3, tab4 = st.tabs(['Summary', 'Columns', 'Data Types', 'Head and Tail'])

        # Tab 1: Summary of the dataset
        with tab1:
            st.write(f'There are {data.shape[0]} rows and {data.shape[1]} columns in the dataset')
            st.subheader('Statistical Summary of the Dataset')
            st.dataframe(data.describe())

        # Tab 2: Names of the columns in the dataset
        with tab2:
            st.subheader('Column Names')
            st.dataframe(list(data.columns))
        # Tab 3: Data Types of the columns in the dataset
        with tab3:
            st.subheader('Data Types of Columns')
            st.dataframe(data.dtypes)

        # Tab 4: Head and Tail of the dataset
        with tab4:
            if is_example:
                st.warning("Currently, you are using an example file. To fully utilize this capability, submit an actual file.")
            else:
                st.subheader('Top Rows')
                top_rows = st.slider('Number of top rows you want', 1, data.shape[0], key='toprowslider')
                st.dataframe(data.head(top_rows))
                st.subheader('Bottom Rows')
                bottom_rows = st.slider('Number of bottom rows you want', 1, data.shape[0], key='bottomrowslider')
                st.dataframe(data.tail(bottom_rows))

    # Tab 3: Columns Values to Count
    with main_tab3:
        st.subheader('Columns Values to Count')
        st.markdown("---")
        if is_example:
            st.warning("Currently, you are using an example file. To fully utilize this capability, submit an actual file.")
        else:
            with st.expander('Value Count'):
                col1, col2 = st.columns(2)
                with col1:
                    column = st.selectbox('Choose Column Name', options=list(data.columns))
                with col2:
                    top_rows = st.number_input('Top Rows', min_value=1, step=1)

                count = st.button('Count')
                if count:
                    result = data[column].value_counts().reset_index().head(top_rows)
                    st.dataframe(result)
                    st.subheader('Visualization')
                    if not result.empty:
                        st.write(result)  # Display the DataFrame for debugging
                        if 'index' not in result.columns:
                            result = result.reset_index()
                        fig = px.bar(data_frame=result, x=column, y='count', text='count', template='presentation')
                        st.plotly_chart(fig)
                        fig = px.line(data_frame=result, x=column, y='count', text='count', template='presentation', markers=True)
                        st.plotly_chart(fig)
                        fig = px.pie(data_frame=result, names=column, values='count', template='presentation')
                        st.plotly_chart(fig)
                    else:
                        st.warning("No data to display in the bar chart.")

    # Tab 4: Groupby: Simplify Your Data Analysis
    with main_tab4:
        st.subheader('Groupby: Simplify Your Data Analysis')
        st.markdown("---")
        if is_example:
            st.warning("Currently, you are using an example file. To fully utilize this capability, submit an actual file.")
        else:
            st.write('The groupby lets you summarize your data by specific categories and groups')
            with st.expander('Groupby your Columns'):
                col1, col2, col3 = st.columns(3)
                with col1:
                    groupby_cols = st.multiselect('Choose Column(s) to group by', options=list(data.columns))
                with col2:
                    operations_col = st.selectbox('Choose Column for operation', options=list(data.columns))
                with col3:
                    operation = st.selectbox('Choose Operation', options=['sum', 'max', 'min', 'mean', 'median', 'count'])

                if groupby_cols:
                    result = data.groupby(groupby_cols).agg(
                        Result=(operations_col, operation)
                    ).reset_index()

                    st.dataframe(result)

                    st.subheader('Data Visualization')
                    graphs = st.selectbox('Choose your graphs', options=['line', 'bar', 'scatter', 'pie', 'sunburst'])
                    if graphs == 'line':
                        x_axis = st.selectbox('Choose X axis', options=list(result.columns))
                        y_axis = st.selectbox('Choose Y axis', options=list(result.columns))
                        color = st.selectbox('Color Information', options=[None] + list(result.columns))
                        fig = px.line(data_frame=result, x=x_axis, y=y_axis, color=color, markers=True)
                        st.plotly_chart(fig)
                    elif graphs == 'bar':
                        x_axis = st.selectbox('Choose X axis', options=list(result.columns))
                        y_axis = st.selectbox('Choose Y axis', options=list(result.columns))
                        color = st.selectbox('Color Information', options=[None] + list(result.columns))
                        facet_col = st.selectbox('Column Information', options=[None] + list(result.columns))
                        fig = px.bar(data_frame=result, x=x_axis, y=y_axis, color=color, facet_col=facet_col, barmode='group')
                        st.plotly_chart(fig)
                    elif graphs == 'pie':
                        values = st.selectbox('Choose Numerical Values', options=list(result.columns))
                        names = st.selectbox('Choose labels', options=list(result.columns))
                        fig = px.pie(data_frame=result, values=values, names=names)
                        st.plotly_chart(fig)
                    elif graphs == 'scatter':
                        x_axis = st.selectbox('Choose X axis', options=list(result.columns))
                        y_axis = st.selectbox('Choose Y axis', options=list(result.columns))
                        color = st.selectbox('Color Information', options=[None] + list(result.columns))
                        size = st.selectbox('Size Column', options=[None] + list(result.columns))
                        fig = px.scatter(data_frame=result, x=x_axis, y=y_axis, color=color, size=size)
                        st.plotly_chart(fig)
                    elif graphs == 'sunburst':
                        path = st.multiselect('Choose your Path', options=list(result.columns))
                        fig = px.sunburst(data_frame=result, path=path, values='Result')
                        st.plotly_chart(fig)
