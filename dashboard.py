import streamlit as st
import pandas as pd

st.set_page_config(page_title = "Cell Analysis", layout="wide")
st.title("Cell Analysis Dashboard")

st.write("Interactive dashboard for immune cell analysis")

part2_tab, part3_tab, part4_tab = st.tabs(["Part 2", "Part 3", "Part 4"])

with part2_tab:
    st.header("Part 2")
    st.subheader("Analysis of cell type frequency")
    cell_frequency = pd.read_csv('outputs/part2/part2.csv')

    st.dataframe(cell_frequency, use_container_width=True)

with part3_tab:
    st.header("Part 3")
    st.subheader("Statistical Analysis of treatment response to miraclib for patients with melanoma")

    st.subheader("Cell frequency of patients with melanoma receiving miraclib")
    cell_frequency_response = pd.read_csv('outputs/part3/frequency.csv')
    st.dataframe(cell_frequency_response, use_container_width=True)
    st.image('outputs/part3/boxplot.png', width = 600)
    st.text("""Looking at the table and boxplot, most frequencies for the cell types appear to be very similar between the responders and nonresponders.
Only cd5_t_cell appears to be noticeably different be different by the naked eye. 
To assess this, we will do more statistical testing to see if this difference is truly significant.""")

    st.subheader("Statistical Analysis of difference in cell frequency of patients with melanoma")
    summary = pd.read_csv('outputs/part3/summary.csv')
    st.dataframe(summary, use_container_width=True)

    st.image('outputs/part3/b_cell_histogram.png', width = 500)
    st.image('outputs/part3/cd4_t_cell_histogram.png', width = 500)
    st.image('outputs/part3/cd8_t_cell_histogram.png', width = 500)
    st.image('outputs/part3/monocyte_histogram.png', width = 500)
    st.image('outputs/part3/nk_cell_histogram.png', width = 500)

    st.text("""Looking at the histograms of the different cell populations, the distributions of all appear to be roughly normal. 
Additionally, our response groups and independent and have similar variances. 
So, we can do a t-test to see if there's a significant difference in average percentages""")

    st.text("*Calculations of t-values and p-values can be found by running part3.py*")

    p_values = pd.read_csv('outputs/part3/p_values.csv')
    st.dataframe(p_values, use_container_width=True)
    st.text("""Looking at the p-values for our tests, at alpha = 0.05
Between the yes responders and no responders, there is a statistically significant difference between the average relative percentages in cell count for cd4_t_cell.""")

with part4_tab:
    st.header("Part 4")
    st.subheader("Subset Analysis of cell frequency for patients with melanoma")

    st.text("melanoma PBMC samples at baseline for patients treated with miraclib")
    table_41 = pd.read_csv('outputs/part4/1.csv')
    st.dataframe(table_41, use_container_width=True)

    st.text("Count of melanoma PBMC samples from each project")
    table_421 = pd.read_csv('outputs/part4/2_1.csv')
    st.dataframe(table_421, use_container_width=True)

    st.text("Count of melanoma PBMC samples by response status")
    table_422 = pd.read_csv('outputs/part4/2_2.csv')
    st.dataframe(table_422, use_container_width=True)

    st.text("Count of melanoma PBMC samples by sex")
    table_423 = pd.read_csv('outputs/part4/2_3.csv')
    st.dataframe(table_423, use_container_width=True)

