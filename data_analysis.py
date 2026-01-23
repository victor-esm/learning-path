import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import xlabel, legend
from sympy.geometry.entity import rotate

# data downloaded from IBGE: TODO download directly from the website
df = pd.read_csv('tabela6835.csv', sep=';', skiprows=3, decimal=',', nrows=28)

# correct the row index
df.reset_index(inplace=True) 
# remove unnecessary columns
df.drop(columns=['index', 'Nível', '2017', '2018'], inplace=True) 
# remove unnecessary rows
df.drop(labels=0, axis=0, inplace=True)
# use meaningful names
df.rename(columns={'Cód.':'Estado', 'Brasil e Unidade da Federação':'2017', 'Unnamed: 4': '2018'}, inplace=True)
print(df.head(10))
print(df.info())
# create specific frames for each year
data_from_2017 = df.loc[:,['Estado', '2017']]
data_from_2018 = df.loc[:,['Estado', '2018']]
data_from_2017.sort_values(by='2017', ascending=False, inplace=True)
data_from_2018.sort_values(by='2018', ascending=False, inplace=True)

# Visualization
ticks_y_axis = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90 ,100]
state_colors = [(1.0, 0.9, 0.0), 'red', 'darkorange', 'red', 'red', (1.0, 0.9, 0.0), (1.0, 0.9, 0.0), 'darkorange', 'blue', 'blue', 'green',
                'blue', 'blue', 'darkorange', 'blue', (1.0, 0.9, 0.0), 'green', 'blue', 'blue', 'green', 'green', 'green',
                'darkorange', 'green', 'blue', 'green', 'blue']
# TODO substitute the list for a dictionary with the state names as keys and a color column to the original df

ax = data_from_2018.plot(kind='bar', x='Estado', y='2018', ylim=(0,100), yticks=ticks_y_axis, legend=False, color=state_colors, edgecolor='white', linewidth=3)
ax.grid(visible=True, alpha=0.2)
plt.xlabel("State")
plt.ylabel("[%]")
plt.title("Proportion of the brazilian population using (a) safely managed sanitation services and \n (b) handwashing facilities with water and soap\nIBGE -  2018",
          fontweight='bold', pad=20, fontsize=15)
plt.savefig("plt.png", dpi=300, bbox_inches='tight')
plt.show()


