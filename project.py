# %% [markdown]
# # 1. first step to explore the data

# %% [markdown]
# > ### before I do any thing i will import the liberaryes I will use in this project 

# %%
# for data mangment and manipulation 

import pandas as pd 
import numpy as np

# for visualis data

import matplotlib.pyplot as plt
import seaborn as sns

# for model traing and feature selection

from sklearn.preprocessing import *
from sklearn.model_selection import *
from sklearn.feature_selection import * 

# %% [markdown]
# ### graphes setup and theme

# %%
sns.set_style("darkgrid")
theme = sns.color_palette("rocket")

# %% [markdown]
# importing data 

# %%
google_df = pd.read_csv(r"./data/Google_data_cleaned.csv")
sip = '-'*100
google_df

# %%
print(f"the columns name of the data are \n{google_df.columns}")

# %%
print(google_df.info())

# %%
print(google_df.dtypes)

# %%
google_df.nunique()

# %%
google_df.isna().sum()

# %%
google_df.loc[google_df.loc[:,"size(kb)"].isna()]

# %%
google_df.shape

# %%
google_df.duplicated().sum()

# %% [markdown]
# # I have noteced some unwanted data and empy cells on the data 

# %% [markdown]
# ## the unwanted data
# they are four columns [unnamed, current_ver, update_month, update_year]

# %%
google_df.drop(google_df.columns[[0, 10, -2, -1]],axis=1,inplace=True)

# %%
google_df.isna().sum()

# %% [markdown]
# > ## filling empty cells with the best crosponding values

# %% [markdown]
# filling the empty cells of rating column based on category

# %%
median_rating =dict(google_df.groupby("category")["rating"].median())

for key in median_rating:
    value = median_rating[key]
    data = google_df[google_df["category"] == key]
    google_df["rating"][google_df["category"] == key] = data["rating"].fillna(value);

# %%
print(google_df.isna().sum())

# %% [markdown]
# filling andrioid_ver from the most supported verison 

# %%
mode_ver =google_df["android_ver"].mode()[0]

google_df["android_ver"].fillna(mode_ver, inplace=True)

# %%
print(google_df.isna().sum())

# %% [markdown]
# filling size column with the avarge of each catigory

# %%
avarge = dict(google_df.groupby(["category"])["size(kb)"].mean())

for key in median_rating:
    value = median_rating[key]
    data = google_df[google_df["category"] == key]
    google_df["size(kb)"][google_df["category"] == key] = data["size(kb)"].fillna(value);

# %%
print(google_df.isna().sum())

# %% [markdown]
# > # Q and A 
# > <hr styel="theme:red;">
# > <ol>
# > <li>What is the most supported android version?</li>
# > <li>What is the most reted gunara of games?</li>
# > <li>Find top 10 social media apps by rating</li>
# > <li>Find top 10 games by rating</li>
# > <li>What is the most expensiev app and what its rating</li>
# > <li>top 10 action games</li>
# > <li>What is The avarge size for games?</li>
# > <li>What is the avarge size of social media apps?</li>
# > <li>What is the most number of reviews and for which app?</li>
# > <li>What is the % of paid and free apps?</li>
# ></ul>

# %%
# What is the most supported android version?

most_android_ver = google_df["android_ver"].value_counts()

x = most_android_ver.index

sns.set_style("darkgrid")

sns.barplot(x=x,y=most_android_ver,palette="icefire")
plt.xticks(rotation = 65);

print(f"the most supported android version is {most_android_ver.index[0]}")

# %% [markdown]
# What is the most reted gunara of games?

# %%
genres = google_df['genres']

for i in range(len(genres)):
    genres[i] = genres[i].split(";")[-1]

# %%
data = dict(google_df.groupby(['category','genres'])["rating"].mean())

data_dict = {}
for key in data:
    key1 = key[0]
    key2 = key[-1]
    if key1 == "GAME":
        data_dict[key2] = data[key]

data_s = pd.Series(data_dict)

data_s.sort_values(ascending=False,inplace=True)

# print(data_s)

x = data_s.index
sns.barplot(y=x, x=data_s,palette="icefire") # i have reversed it to be more redable 
# plt.xticks(rotation=90);

print(f'the most rated genre is "{x[0]}" with avarge rating of {data_s[0]}')

# %% [markdown]
# 3. top 10 socila media apps

# %%
rating = dict(google_df.groupby(['category','app'])[("rating")].mean())
n_reviews = dict(google_df.groupby(['category','app'])["reviews"].mean())

social = []


for i in range(len(rating)):

    key = list(rating.keys())[i]
    app_type = key[0]
    app_name = key[1]

    dic = {}

    if app_type == "SOCIAL" :

        dic["app_name"] = app_name
        dic["rating"] = rating[key]
        dic["reviews"] = n_reviews[key]

        social.append(dic)

social_df = pd.DataFrame(social)

sorted_ = social_df.sort_values(["reviews","reviews"],ascending=False ,ignore_index=True)

print(sorted_.head(10))

d = sorted_.head(10)

sns.barplot(data=d, y="app_name", x="rating",palette="icefire")
plt.show()
sns.barplot(data=d, y="app_name", x="reviews",palette="icefire")

# %% [markdown]
# 4. top 10 games on the store

# %%

data = dict(google_df.groupby(['category',"app"])["rating"].mean())

n_reviews = dict(google_df.groupby(['category','app'])["reviews"].mean())


games = []

for i in range(len(data)):

    key = list(data.keys())[i]
    app_type = key[0]
    app_name = key[1]

    dic = {}

    if app_type == "GAME" :

        dic["app_name"] = app_name
        dic["rating"] = data[key]
        dic["reviews"] = n_reviews[key]

        games.append(dic)

games_df = pd.DataFrame(games)

# print(games_df)

games_df.sort_values(["reviews","rating"],ascending=False,inplace=True, ignore_index=True)

d = games_df.head(10)

print(d)

sns.barplot(data=d, y="app_name", x="rating",palette="icefire");
plt.show();
sns.barplot(data=d, y="app_name", x="reviews",palette="icefire");

# %% [markdown]
# 5. the most expensev apps and its ratings
# 

# %%
google_df.loc[:,["app","rating","price","installs"]][google_df["price"].max() == google_df['price']]

# %% [markdown]
# 6. the best 10 action games?

# %%
data = dict(google_df.groupby(['category','genres','app'])["rating"].mean())
n_reviews = dict(google_df.groupby(['category','genres','app'])["reviews"].mean())

games = []

for i in range(len(data)):

    key = list(data.keys())[i]
    test = key[:-1]
    app_type = key[0]
    app_name = key[2]
    game_type = key[1]

    dic = {}

    if app_type == "GAME":

        if game_type == "Action":

            dic["app_name"] = app_name
            dic["rating"] = data[key]
            dic["reviews"] = n_reviews[key]

            games.append(dic)
        else:
            pass

games_df = pd.DataFrame(games)

games_df.sort_values(["reviews","rating"],ascending=False,inplace=True, ignore_index=True)

d = games_df.head(10)

print(d)

sns.barplot(data=d, y="app_name", x="rating",palette="icefire");
plt.show();
sns.barplot(data=d, y="app_name", x="reviews",palette="icefire");

# %% [markdown]
# 7. what is the avarge size for games 

# %%
data = dict(google_df.groupby(["category"])['size(kb)'].mean())

print(f'The averge size of games is {data["GAME"]/1000} mg')

# %% [markdown]
# 8. what is the averge size for social media

# %%
print(f'The averge size of Social media apps is {data["SOCIAL"]/1000} mg')

# %% [markdown]
# 9. what is the most number of reviews and for which app

# %%
google_df[google_df['reviews']== google_df['reviews'].max()]

# %% [markdown]
# 10. what is the % of paid and free apps

# %%
pi = google_df['type'].value_counts()

plt.pie(pi,colors=theme,labels=["free","non_free"], explode=[0.3,0.2]);


