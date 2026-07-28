import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Simple Data Dashboard")
df=pd.read_csv('job_data.csv')
plt.style.use('dark_background')
st.title("Simple Data Dashboard")
st.header("Data Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Jobs", len(df))
col2.metric("Unique Job Titles", df["job_title"].nunique())
col3.metric("Unique Industries", df["industry"].nunique())
col4, col5, col6 = st.columns(3)
col4.metric("Remote Jobs", (df["location"] == "Remote").sum())
col5.metric("Locations", df["location"].nunique())
col6.metric("Average Salary", f"{df['salary'].mean():,.0f}")

def cat_by_exp(exp):
 if exp=="fresher":
  return df[df["experience_years"].isin([0, 1])].head(50)
 elif exp=="beginneer":
  return  df[df["experience_years"].isin([2,3])].head(50)
 elif exp=="intermediate":
  return df[df["experience_years"].isin([4,5,6])].head(50)
 elif exp=="experienced":
  return df[df["experience_years"].isin([7,8,9,10])].head(50)
 elif exp=="senior":
  return df[df["experience_years"].isin([11,12,13,14,15])].head(50)
inp=st.selectbox("Choose the Experience level (First 50 displayed)",["fresher","beginneer","intermediate","experienced","senior"])
st.write(cat_by_exp(inp))
expe=df["experience_years"].value_counts()
if st.button("plot by experience"):
   st.bar_chart(expe, x_label='Experience',y_label='Number of jobs')

def cat_by_sal(sal):
    if sal == "low":
        return df[df["salary"] < 100999][
            ["job_title", "salary"]
        ].round(2).head(50)
    elif sal == "mid":
        return df[
            (df["salary"] >= 100999) &
            (df["salary"] < 250000)
        ][["job_title", "salary"]].round(2).head(50)
    elif sal == "high":
        return df[df["salary"] > 250000][
            ["job_title", "salary"]
        ].round(2).head(50)

st.header("Data Categorized by Salary")
ip=st.selectbox("Choose a Salary Category (First 50 displayed)",["low","mid","high"])
st.write(cat_by_sal(ip))

def visualsal(sal):
 result= cat_by_sal(sal)
 result = result.drop_duplicates("job_title").head(10)
 ax=result.set_index('job_title')[["salary"]].plot(kind='bar',color="#190A5A")
 ax.set_title(f"Roles in {sal} salary category")
 ax.set_xlabel("Job Title")
 ax.set_ylabel("Salary Range")
 plt.xticks(rotation=35, ha="right")
 #plt.tight_layout()
 st.pyplot(ax.figure)
if st.button("Plot by Salaries"):
   visualsal(ip)

def filter_by_edu(edu):
    if edu == "Bachelor":
        return df[df["education_level"] == "Bachelor"][
            ["job_title", "salary", "experience_years", "skills_count", "industry", "company_size", "location"]
        ].round(2).head(50)
    elif edu == "Master":
        return df[df["education_level"] == "Master"][
            ["job_title", "salary", "experience_years", "skills_count", "industry", "company_size", "location"]
        ].round(2).head(50)
    elif edu == "PhD":
        return df[df["education_level"] == "PhD"][
            ["job_title", "salary", "experience_years", "skills_count", "industry", "company_size", "location"]
        ].round(2).head(50)
    elif edu == "Diploma":
        return df[df["education_level"] == "Diploma"][
            ["job_title", "salary", "experience_years", "skills_count", "industry", "company_size", "location"]
        ].round(2).head(50)
    elif edu == "High School":
        return df[df["education_level"] == "High School"][
            ["job_title", "salary", "experience_years", "skills_count", "industry", "company_size", "location"]
        ].round(2).head(50)

st.header("Data Filtered by Education")
edu_ip = st.selectbox("Choose an Education Level (First 50 displayed)", ["Bachelor", "Master", "PhD", "Diploma", "High School"])
st.write(filter_by_edu(edu_ip))

edu_counts = df["education_level"].value_counts()
if st.button("plot by education"):
    st.bar_chart(edu_counts,x_label="Education Level", y_label="Number of jobs")

M_D= df["job_title"].value_counts().reset_index()
M_D.columns=['Job Titles','Number of Roles']
st.header("Job Demand Count")
st.write(M_D)
res=M_D=df["job_title"].value_counts()
if st.button("Plot by Demand"):
   st.bar_chart(res,x_label='Job Titles',y_label='Number of Jobs')

avg_salary = df.groupby("job_title")[["salary"]].mean().round(2)
st.header("Average Salary by Role")
st.write(avg_salary)
if st.button("plot by average salary"):
   st.bar_chart(avg_salary,x_label='Job Titles',y_label='Average Salaries')

common_job_locs= df["location"].value_counts().reset_index()
common_job_locs.columns=['Job Locations','Number of Jobs']
st.header("Common Job Locations")
st.write(common_job_locs)
if st.button("plot jobs by locations"):
   res=df["location"].value_counts()
   st.bar_chart(res,x_label='Locations',y_label='Number of Jobs')

st.header("Job Count for Each Industry")
indust = df["industry"].value_counts()
st.write(indust)
if st.button("Plot data for Job by industry"):
  st.bar_chart(indust,x_label='Industry',y_label='Number of Jobs')

#functions for userinterface
#-------------------------------------------------------------------------
# def mostdemandjobs():
#  M_D.plot(kind="bar")
#  plt.title("Most Demanded Jobs")
#  plt.xlabel("Job Title")
#  plt.ylabel("Number of Job Listings")
#  plt.xticks(rotation=45, ha='right')
#  #plt.figure(figsize=(12, 6))
#  plt.tight_layout()
#  return plt.show()

# def avgsal():
#   #plt.figure(figsize=(12, 6))
#   avg_salary.plot(kind="bar")
#   plt.title("Average salaries by job titles")
#   plt.ylabel("Job Titles")
#   plt.xlabel("Average salaries")
#   plt.xticks(rotation=35, ha="right")
#   plt.tight_layout()
#   plt.show()

# def CJLvisuals():
#   common_job_locs.plot(kind='bar')
#   plt.title("Common Job Locations")
#   plt.ylabel('number of jobs')
#   plt.xlabel('locations')
#   plt.xticks(rotation=0)
#   plt.show()

# def expvisuals():
#  expe=df["experience"].value_counts()
#  expe.plot(kind="bar")
#  plt.title("Jobs by Experience Level")
#  plt.xlabel("Experience Required")
#  plt.ylabel("Number of jobs")
#  plt.xticks(rotation=35, ha="right")
#  #plt.figure(figsize=(12, 6))
#  plt.tight_layout()
#  plt.show()

#terminal interface
# print("Job Market Analyzer")
# print("----------------------------------------")
# while True:
#  print("select to view data: (0 to exit)")
#  ui=input("1.categorise by experience needed for jobs\n2.categorise by salary\n3.demand count of roles\n4.Average salary of different roles\n5.Common job locations: \n")
#  if ui == "1":
#   exp=input("enter the category to see it's required experience i.e beginneer, intermediate, experienced or senior: ")
#   print(cat_by_exp(exp))
#   ip=input("Do you want to visualize this data? Y/N: ")
#   if ip.lower()=="y":
#     expvisuals()
#  elif ui== "2":
#   cat=input("what category of salary do you want to see i.e low,mid,high: ")
#   print(cat_by_sal(cat))
#   ip = input("Do you want to visualize this data? Y/N: ")
#   if ip.lower()=="y":
#     visualsal(cat)
#  elif ui=="3":
#   print(M_D)
#   ip=input("Do you want to visualize this data? Y/N: ")
#   if ip.lower()=="y":
#     mostdemandjobs()
#  elif ui=="4":
#   print(avg_salary)
#   ip=input("Do you want to visualize this data? Y/N: ")
#   if ip.lower()=="y":
#     avgsal()
#  elif ui=="5":
#   print(common_job_locs)
#   ip=input("Do you want to visualize this data? Y/N: ")
#   if ip.lower()=="y":
#     CJLvisuals()
#   elif ui=="0":
#    break
