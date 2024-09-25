import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_most_used_payment_method_df(df):
  most_used_payment_method_df = df.groupby(by='payment_type').order_id.nunique().sort_values(ascending=False).reset_index()
  most_used_payment_method_df.rename(columns={
      'order_id': 'order_count'
  }, inplace=True)

  return most_used_payment_method_df

def create_best_worst_sellers_df(df):
  best_worst_sellers_df = df.groupby(by='seller_id').price.nunique().reset_index()

  return best_worst_sellers_df

def create_monthly_delivery_time_df(df):
  monthly_delivery_time_df = df.resample(rule='M', on='order_purchase_timestamp').agg({
      'order_id': 'nunique',
      'delivery_time': 'mean'
  })
  monthly_delivery_time_df.index = monthly_delivery_time_df.index.strftime('%B')
  monthly_delivery_time_df = monthly_delivery_time_df.reset_index()
  monthly_delivery_time_df.fillna(0, inplace=True)

  return monthly_delivery_time_df

def create_rfm_df(df):
  rfm_df = df.groupby(by='seller_id', as_index=False).agg({
    'order_approved_at': 'max',
    'order_id': 'nunique',
    'price': 'sum'
  })
  rfm_df.columns = ['seller_id', 'max_order_timestamp', 'frequency', 'monetary']
  rfm_df['max_order_timestamp'] = rfm_df['max_order_timestamp'].dt.date
  recent_date = df['order_purchase_timestamp'].dt.date.max()
  rfm_df['recency'] = rfm_df['max_order_timestamp'].apply(lambda x: (recent_date - x).days)
  rfm_df.drop('max_order_timestamp', axis=1, inplace=True)

  return rfm_df

all_df = pd.read_csv('dashboard/main_data.csv')

datetime_columns = [
    'shipping_limit_date',
    'order_purchase_timestamp',
    'order_approved_at',
    'order_delivered_carrier_date',
    'order_delivered_customer_date',
    'order_estimated_delivery_date'
]
all_df.sort_values(by='order_purchase_timestamp', inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df['order_purchase_timestamp'].min()
max_date = all_df['order_purchase_timestamp'].max()

years = all_df['order_purchase_timestamp'].dt.year.unique()
years = sorted(years, reverse=True)

with st.sidebar:
  st.header('Brazilian E-Commerce Dashboard')
  year = st.selectbox(
    label="Select a year",
    options=years,

  )

main_df = all_df[all_df['order_purchase_timestamp'].dt.year == year]

best_worst_sellers_df = create_best_worst_sellers_df(main_df)
most_used_payment_method_df = create_most_used_payment_method_df(main_df)
monthly_delivery_time_df = create_monthly_delivery_time_df(main_df)
rfm_df = create_rfm_df(main_df)


# Metric
col1, col2, col3 = st.columns(3, gap='medium')
with col1:
  st.metric(label='Total Seller', value=all_df['seller_id'].nunique())

with col2:
  st.metric(label='Total Product', value=all_df['product_id'].nunique())

with col3:
  st.metric(label='Total Order', value=all_df['order_id'].nunique())


# Barplot
st.subheader('Most Frequently Used Payment Method')

fig, ax = plt.subplots(figsize=(20, 10))
colors = ['#050C9C', '#A7E6FF', '#A7E6FF', '#A7E6FF', '#A7E6FF']
sns.barplot(
    x='payment_type',
    y='order_count',
    data=most_used_payment_method_df,
    palette=colors
)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)


# Double barplot
st.subheader('Best and Worst Sellers')

col1, col2 = st.columns(2)

with col1:
  fig, ax = plt.subplots(figsize=(20, 10))
  colors = ['#050C9C', '#A7E6FF', '#A7E6FF', '#A7E6FF', '#A7E6FF']
  sns.barplot(
      x='seller_id',
      y='price',
      data=best_worst_sellers_df.sort_values(by='price', ascending=False).head(5),
      palette=colors,
      ax=ax
  )
  ax.set_ylabel(None)
  ax.set_xlabel('Seller ID', fontsize=30)
  ax.set_title('Top 5 Sellers', loc='center', fontsize=40)
  ax.tick_params(axis='x', labelsize=20, labelrotation=70)
  ax.tick_params(axis='y', labelsize=30)
  st.pyplot(fig)

with col2:
  fig, ax = plt.subplots(figsize=(20, 10))
  colors = ['#050C9C', '#A7E6FF', '#A7E6FF', '#A7E6FF', '#A7E6FF']
  sns.barplot(
      x='seller_id',
      y='price',
      data=best_worst_sellers_df.sort_values(by='price', ascending=True).head(5),
      palette=colors,
      ax=ax
  )
  ax.set_ylabel(None)
  ax.set_xlabel('Seller ID', fontsize=30)
  ax.invert_xaxis()
  ax.yaxis.set_label_position("right")
  ax.yaxis.tick_right()
  ax.set_title('Bottom 5 Sellers', loc='center', fontsize=40)
  ax.tick_params(axis='x', labelsize=20, labelrotation=70)
  ax.tick_params(axis='y', labelsize=30)
  st.pyplot(fig)


# Line Chart
st.subheader('Average Monthly Delivery Time ({})'.format(year))

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_delivery_time_df['order_purchase_timestamp'],
    monthly_delivery_time_df['delivery_time'],
    marker='o',
    linewidth=2,
    color='#050C9C'
)
ax.set_ylabel('Delivery time (days)', fontsize=15)
ax.set_xlabel(None)
ax.set_ylim(0, round(monthly_delivery_time_df['delivery_time'].max() + 10))
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=25, labelrotation=30)
st.pyplot(fig)


# Pie Chart
st.subheader('Delivery Performance')

late_delivery_precentage = (main_df['delivery_delay'] > 0).mean() * 100
on_time_delivery_precentage = 100 - late_delivery_precentage

fig, ax = plt.subplots()
ax.pie(
    x=[on_time_delivery_precentage, late_delivery_precentage],
    labels=['On Time', 'Late'],
    colors=['#3572EF', '#FF204E'],
    autopct='%1.1f%%',
    explode=[0.1, 0]
)
st.pyplot(fig)


# Triple Bar Plot
st.subheader('Best Seller Based on RFM Parameters')
col1, col2, col3 = st.columns(3)
with col1:
  avg_recency = round(rfm_df.recency.mean(), 1)
  st.metric('Average Recency (days)', value=avg_recency)

with col2:
  avg_frequency = round(rfm_df.frequency.mean(), 2)
  st.metric('Average Frequency', value=avg_frequency)

with col3:
  avg_frequency = format_currency(rfm_df.monetary.mean(), "BRL", locale='pt_BR')
  st.metric('Average Monetary', value=avg_frequency)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors = ['#050C9C', '#050C9C', '#050C9C', '#050C9C', '#050C9C']

sns.barplot(
    y='recency',
    x='seller_id',
    data=rfm_df.sort_values(by='recency', ascending=True).head(5),
    palette=colors,
    ax=ax[0]
)
ax[0].set_ylabel(None)
ax[0].set_xlabel('seller_id', fontsize=30)
ax[0].set_title('By Recency (days)', loc='center', fontsize=50)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=20, labelrotation=80)

sns.barplot(
    y='frequency',
    x='seller_id',
    data=rfm_df.sort_values(by='frequency', ascending=False).head(5),
    palette=colors,
    ax=ax[1]
)
ax[1].set_ylabel(None)
ax[1].set_xlabel('seller_id', fontsize=30)
ax[1].set_title('By Frequency', loc='center', fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=20, labelrotation=80)

sns.barplot(
    y='monetary',
    x='seller_id',
    data=rfm_df.sort_values(by='monetary', ascending=False).head(5),
    palette=colors,
    ax=ax[2]
)
ax[2].set_ylabel(None)
ax[2].set_xlabel('seller_id', fontsize=30)
ax[2].set_title('By Monetary', loc='center', fontsize=50)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=20, labelrotation=80)

st.pyplot(fig)
