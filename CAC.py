# Supress warnings
import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)

# importing necessary python libraries and the dataset
import pandas as pd
import plotly.graph_objects as go

my_data = pd.read_csv('customer_acquisition_cost_dataset (1).csv')
print(my_data.head())

# checking missing values, data types, shape of the data
print(my_data.info())

# check the dimension of the data
print(f'The data has {my_data.shape[0]} rows and {my_data.shape[1]} columns.')

# Alternative to `.describe()`/describing data with more detailed summary
'''from skimpy import skim
skim(my_data)'''   # was unable to install package/use describe method instead

# check missing values in %age
missing_values = (
    my_data.isnull().sum()/len(my_data)*100
).astype(int)

print(f'Column\t\t\t% missing')
print(f'{"-"}'*35)
print(missing_values)

# calculating the customer acquisition cost
my_data['CAC'] = my_data['Marketing_Spend'] / my_data['New_Customers']

import plotly.express as px
fig = px.bar(my_data, x='Marketing_Channel', y='CAC', title='CAC by Marketing Channel')
fig.show()
# dealing with outliers, looking at the CAC marketing channels
fig1 = px.box(
    x=my_data['Marketing_Spend'],
    orientation='h',
    title='Boxplot of the Target (Marketing_Spend) - With Outliers'
)

fig1.update_layout(xaxis_title='Target')
fig1.show()

# looking at the new relationship for the CAC and the new acquired customers
fig2 = px.scatter(my_data, x='New_Customers',
                  y='CAC', color='Marketing_Channel',
                  title='CAC vs. New Customers ',
                  trendline='ols')
fig2.show()

# Calculate the summary statistics for each marketing channel
''' marketing_channels = my_data.group('Marketing_Channel')
summary_stats = marketing_channels.agg({'Customer_Acquisition_Cost': ['count', 'mean', 'median', 'std', 'min', 'max']})
# Print the summary statistics
# print(summary_stats)'''
summary_stats = my_data.groupby('Marketing_Channel')['CAC'].describe()
print(summary_stats)

# conversion rate of the  marketing campaign
my_data['Conversion_Rate'] = my_data['New_Customers'] / my_data['Marketing_Spend'] * 100

# Conversion Rates by Marketing Channel
fig3 = px.bar(my_data, x='Marketing_Channel', y='Conversion_Rate', title='Marketing Channel by Conversion Rates ')
fig3.show()

# Calculate the break-even customers for each marketing channel
break_even_customers = (my_data['Marketing_Spend'] / my_data['CAC'])

# Print the break-even customers for each marketing channel
print(break_even_customers)

#  marketing channel
fig4 = px.bar(my_data, x='Marketing_Channel', y='Conversion_Rate',
              title='Conversion_Rate by Marketing Channel')
fig4.show()
# comparing the actual customers acquired with the break-even customers for each marketing channel
fig5 = go.Figure()

# Actual Customers Acquired
fig5.add_trace(go.Bar(x=my_data['Marketing_Channel'], y=my_data['New_Customers'],
                      name='Actual Customers Acquired', marker_color='grey'))

# Break-Even Customers
fig5.add_trace(go.Bar(x=my_data['Marketing_Channel'], y=my_data['Conversion_Rate'],
                      name='Conversion_Rate', marker_color='pink'))

# Update the layout
fig5.update_layout(barmode='group', title=' Conversion Rate by Marketing Channel vs. Actual Customers acquired',
                   xaxis_title='Marketing Channel', yaxis_title='Number of Customers')

# Show the chart
fig5.show()
