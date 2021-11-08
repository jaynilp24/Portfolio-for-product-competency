from numpy.core.fromnumeric import size
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def shorten_categories(categories, cutoff):
    map_categories = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            map_categories[categories.index[i]] = categories.index[i]
        else:
            map_categories[categories.index[i]] = 'Other'
    return map_categories

def clean_experience(x):
    if x ==  'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)

def clean_ed(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'

@st.cache
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "Age", "YearsCodePro", "Employment", "ConvertedComp"]]
    df = df[df["ConvertedComp"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed full-time"]
    df = df.drop("Employment", axis=1)

    df = df[df["Age"] < 65]
    df = df[df["Age"] > 17]
    country_map = shorten_categories(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)
    df = df[df["ConvertedComp"] <= 250000]
    df = df[df["ConvertedComp"] >= 10000]
    df = df[df["Country"] != "Other"]

    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_ed)
    df = df.rename({"ConvertedComp": "Salary"}, axis=1)
    return df

df = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    st.write(
        """
    ### Stack Overflow Developer Survey 2020
    """
    )

    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    colors = sns.color_palette('pastel')
    #ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    plt.pie(data, labels = data.index, colors = colors, autopct='%.0f%%')
    plt.show()
    plt.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.write("""#### Country-wise Data distribution """)

    st.pyplot(fig1)
    
    st.write(
        """
    #### Mean Salary Based On Country
    """
    )

    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write(
        """
    #### Mean Salary Based On Experience
    """
    )
    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)

    st.write(
        """
    #### Mean Salary Based On Age
    """
    )
    data = df.groupby(["Age"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)



