# import pgm....
import streamlit as st
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import seaborn as sns
import plotly.express as px

# streamlit link...cd C:\Users\tathant\Documents\_PYTHON_T\_ASSIGNMENT

# set up page....
st.set_page_config(page_title='T Assignment',layout='wide')

# adding image
from PIL import Image
image= Image.open("C:/Users/tathant/Documents/_PYTHON_T/_ASSIGNMENT/Sales-Analysis-3.jpg")
new_image=image.resize((400,200))

col1,col2= st.columns(2)
with col1:
    st.image(new_image)
    st.markdown("**--------------------------------------------------------------------------------------------**")
with col2:
    st.title("Review of 5 Market Territories - 2012 to 2015")
    st.markdown('**This review is to explore specific market territories to increase profit-return or sales close-out.**')
    st.markdown("**--------------------------------------------------------------------------------------------**")
#Load the data table csv
od=pd.read_csv("C:/Users/tathant/Documents/_PYTHON_T//_ASSIGNMENT/T_sales_data.csv")

# change data type of columns to calculate
od['Country'] = od['Country'].astype('category')
od['Region'] = od['Region'].astype('category')
od['Market'] = od['Market'].astype('category')
od['Category'] = od['Category'].astype('category')
od['Sub-Category'] = od['Sub-Category'].astype('category')
od['Segment'] = od['Segment'].astype('category')
od['OrderPriority'] = od['OrderPriority'].astype('category')


# table with only selected columns
sd=od[['orderyear', 'ordermonth', 'Segment', 'OrderPriority', 'Country',
       'Region', 'Market', 'Category', 'Sub-Category', 'Sales', 'Discount',
       'Profit', 'ShippingCost', 'DeliveryDays','City',
       'ProductName', 'Quantity']]

#----------------------------------------------------------------
st.header("1_Result At a Glance(2012-15)")

#adding matrix (single result number, %, updown )
st.subheader("**What we achieved!**")

total_sale=sd['Sales'].sum()
total_profit=sd['Profit'].sum()
profit_bySale=(sd['Profit'].sum()/sd['Sales'].sum())*100

col1, col2, col3= st.columns(3)
col1.metric("**Total Sales**", total_sale)
col2.metric("**Total Profit**", total_profit)
col3.metric("**% Profit-return**", profit_bySale)
st.write(f"During 5 years, our sales value reached to USD {total_sale},which generated profit USD {total_profit}. It means we got {profit_bySale}% as profit for every 1USD sale did.")

st.subheader("**Where we are!**")

region_count=len(sd['Region'].unique())
country_count=len(sd['Country'].unique())
city_count=len(od['City'].unique())  #taken from od not sd

col1, col2, col3= st.columns(3)
col1.metric("**Regions**", region_count)
col2.metric("**Countries**", country_count)
col3.metric("**City**", city_count)
st.write(f"In five market territories, our sales reached to  {city_count} cities in {country_count} countries, existed at {region_count} regions around the world.")

with st.expander("See Region list with their sales here"):
     st.dataframe(od.groupby('Region')['Sales'].sum())
with st.expander("See Country list with their sales here"):
     st.dataframe(od.groupby('Country')['Sales'].sum())
with st.expander("See City list with their sales here"):
     st.dataframe(od.groupby('City')['Sales'].sum())

st.subheader("**What we sold!**")

category_count=len(sd['Category'].unique())
subcat_count=len(sd['Sub-Category'].unique())
product_count=len(od['ProductName'].unique())  #taken from od not sd

col1, col2, col3= st.columns(3)
col1.metric("**Product Categories**", category_count)
col2.metric("**Product Sub-Categories**", subcat_count)
col3.metric("**Product Items**", product_count)  #taken from od not sd
st.write(f"We can sold out total  {product_count} product items,  under {subcat_count} sub-categories.  Our sale items are listed by {category_count} categories.")

with st.expander("See Product category list with ordered quantities here"):
     st.dataframe(od.groupby('Category')['Quantity'].sum())
with st.expander("See Sub-category list with ordered quantities here"):
     st.dataframe(od.groupby('Sub-Category')['Quantity'].sum())
with st.expander("See product item list with ordered quantities here"):
     st.dataframe(od.groupby('ProductName')['Quantity'].sum())

st.subheader("**Our customers!**")

customer_headcount=len(od['CustomerName'].unique())
customer_frequency=len(od['CustomerName'])

image= Image.open("C:/Users/tathant/Documents/_PYTHON_T/_ASSIGNMENT/customers.jpg")
customers=image.resize((200,100))


col1, col2, col3= st.columns(3)
col1.image(customers)
col2.metric("**Total customers**", customer_headcount)
col3.metric("**Order Times**", customer_frequency)

st.write(f"We got loyal customers around  {customer_headcount} in four years,  who did  {customer_frequency} order times generating {total_profit} USD profit. Thanks to them!")

st.markdown("............................................................")


#----------------------------------------------------------------
st.header("2_Review on Annual Result Trend")

# annual result table and bar chart.....
result_annual=sd.groupby('orderyear').aggregate({'Sales':'sum','Profit':'sum'}).reset_index()
result_annual['profit_bySale']=(result_annual['Profit']/result_annual['Sales'])*100

with st.expander("See annual result table here"):
     st.dataframe(result_annual.style.highlight_max(axis=0))

fig_sale_annual=px.bar(result_annual,x='orderyear',y='Sales',
        orientation="v",
        title="<b>Annual Sales</b>")
fig_profit_annual=px.bar(result_annual,x='orderyear',y='Profit',
        orientation="v",
        title="<b>Annual Profit</b>")
fig_percentprofit_annual=px.bar(result_annual,x='orderyear',y='profit_bySale',color='profit_bySale',
        orientation="v",range_y=[10,12],
        title="<b>Profit on Sales amount</b>")

column1,column2,column3= st.columns(3)
with column1:
    st.plotly_chart(fig_sale_annual, use_container_width=True)
with column2:
    st.plotly_chart(fig_profit_annual, use_container_width=True)
with column3:
    st.plotly_chart(fig_percentprofit_annual, use_container_width=True)

st.markdown('**Findings: \nhighest sales and highest profit amounts achieved at 2015.  \nBut, the profit return on each 1$ sale is decreased from previous year 2014, from 11.8% to 11.6%.**')
st.markdown('**Suggestion: \nto explore the five territories about how they contributed in sale and prfit-return.**')
st.markdown("............................................................")

#----------------------------------------------------------------
st.header("3_Review on Results among five market territories")

# 5 territories' result table and bar chart.....
result_territory=sd.groupby('Market').aggregate({'Sales':'sum','Profit':'sum'}).reset_index()
result_territory['profit_bySale']=(result_territory['Profit']/result_territory['Sales'])*100
result_territory

# error ???? found as: Categorical is not ordered for operation max you can use .as_ordered() to change the Categorical to an ordered one
#st.dataframe(result_territory.style.highlight_max(axis=0))


fig_sale_territory=px.bar(result_territory,x='Market',y='Sales',color='Sales',
        orientation="v",
        title="<b>Annual Sales</b>")
fig_profit_territory=px.bar(result_territory,x='Market',y='Profit',color='Profit',
        orientation="v",
        title="<b>Annual Profit</b>")
fig_percentprofit_territory=px.bar(result_territory,x='Market',y='profit_bySale',color='profit_bySale',
        orientation="v",range_y=[8,14],
        title="<b>Profit on Sales amount</b>")

column1,column2,column3= st.columns(3)
with column1:
    st.plotly_chart(fig_sale_territory, use_container_width=True)
with column2:
    st.plotly_chart(fig_profit_territory, use_container_width=True)
with column3:
    st.plotly_chart(fig_percentprofit_territory, use_container_width=True)

st.markdown('**Findings: \n80% of profit come from EU,AP,USCA.  \nThe other two territories..LATAM&AFR can contrbutedonly 20%. \nAsia Pacific(AP) provided highest sales but lowest profit%-return ie. around 10%. \nIn contrast,  Europe (EU) provided high profit-return as 14% which is 4% higherthan AP.**')
st.markdown('**Suggestion:  \nTo consider business close-out on the Africa sale market.  \nTo increase AP profit-return as EU, by exploring which AP countries have lower sales-profit-return upon which item categories.**')
st.markdown("............................................................")


#----------------------------------------------------------------
st.header("4_Review of Asia Pacific Results by comparing with EU")

sd_AP=sd[sd['Market']=='Asia Pacific'].describe()
sd_EU=sd[sd['Market']=='Europe'].describe()

data_container = st.container()
with data_container:
    table1, table2 = st.columns(2)
    with table1:
        table1.subheader('Asia Pacific')
        st.table(sd_AP)
    with table2:
        table2.subheader('Europe')
        st.table(sd_EU)

st.markdown('**Findings: \nAverage delivery days and average shipping cost are more or less the same between AP and EU**')
st.markdown('**Average of discount given differ as 0.18 (AP) vs 0.09 (EU)**')
st.markdown("............................................................")


#----------------------------------------------------------------
st.header("5_Asia Pacific: Results by commodity categories (comparing to EU)")

AP=sd[(sd['orderyear']==2015) & (sd['Market']=="Asia Pacific")]
AP_category=AP.groupby('Category').aggregate({'Sales':'sum','Profit':'sum'}).reset_index()
AP_category['profit_bySale']=(AP_category['Profit']/AP_category['Sales'])*100

EU=sd[(sd['orderyear']==2015) & (sd['Market']=="Europe")]
EU_category=EU.groupby('Category').aggregate({'Sales':'sum','Profit':'sum'}).reset_index()
EU_category['profit_bySale']=(EU_category['Profit']/EU_category['Sales'])*100

APcategory_bar=px.bar(AP_category,x='Category',y='profit_bySale',color='profit_bySale')
EUcategory_bar=px.bar(EU_category,x='Category',y='profit_bySale',color='profit_bySale')

table_container= st.container()
with table_container:
    table1, table2 = st.columns(2)
    with table1:
        table1.subheader('Asia Pacific')
        st.table(AP_category)
    with table2:
        table2.subheader('Europe')
        st.table(EU_category)

bar_container= st.container()
with bar_container:
    bar1, bar2 = st.columns(2)
    with bar1:
        st.plotly_chart(APcategory_bar, use_container_width=True)        
    with bar2:
        st.plotly_chart(EUcategory_bar, use_container_width=True)

st.markdown('**Furniture & Technology Categories = similar profit-return between AP and EU**')
st.markdown('**Office Supplies = EU got high profit-return 15.9, which is nearly double of AP (8.9)**')
st.markdown('**Suggestion: \nFor taking action how to increase Office supply profit-return, it is need to explore AP Office supply results by country, by sub-category, by item, by month...**')
st.markdown("............................................................")

#----------------------------------------------------------------
st.header("6_Asia Pacific: Results of 2015 office supplies by Region, by Country, by Sub-category")

# APOS = filtering AP - 2015 - office supply only
APOS=sd[(sd['orderyear']==2015) & (sd['Market']=="Asia Pacific") & (sd['Category']=='Office Supplies')]

APOS_result_month=APOS.groupby('ordermonth').aggregate({'Sales':'sum','Profit':'sum'}).reset_index()
APOS_result_month['profit_bySale']=(APOS_result_month['Profit']/APOS_result_month['Sales'])*100

# APOSonly = filtering need columns only
APOSonly=APOS[['ordermonth','Region','Country',
       'Sub-Category', 'Sales', 'Discount',
       'Profit']]

# change data type of columns to calculate
APOSonly['Country'] = APOSonly['Country'].astype('category')
APOSonly['Region'] = APOSonly['Region'].astype('category')
APOSonly['Sub-Category'] = APOSonly['Sub-Category'].astype('category')

with st.expander("See detail table here"):
     APOSonly
st.markdown('** **')
#----------------------------------------------------------------
st.subheader("6.1_Monthly Sale vs Profit")

with st.expander("See AP monthly result table here"):
     st.dataframe(APOS_result_month.style.highlight_max(axis=0))

APOSmonth_combo=px.bar(APOS_result_month, x='ordermonth',y='Sales',color=None, title="Monthly Sales and Profit-return"
).add_traces(
    px.line(APOS_result_month, x="ordermonth", y="profit_bySale").update_traces(showlegend=True, name="Profit-return", yaxis="y2").data
).update_layout(yaxis2={"side":"right", "overlaying":"y"})
#APOSmonth_combo

APOSmonth_combo_profit=px.bar(APOS_result_month, x='ordermonth',y='Sales',color=None, title="Monthly Sales and Profit"
).add_traces(
    px.line(APOS_result_month, x="ordermonth", y="Profit").update_traces(showlegend=True, name="Profit", yaxis="y2").data
).update_layout(yaxis2={"side":"right", "overlaying":"y"})
#APOSmonth_combo_profit

bar_container= st.container()
with bar_container:
    bar1, bar2 = st.columns(2)
    with bar1:
        st.plotly_chart(APOSmonth_combo, use_container_width=True)
        st.markdown('**Monthly sale = uptrend   \nMonthly profit-return = downw in month 5,6,8,12   \n good return rate at month 3,4,7,10   \ndue to sold item type, ?price, ...**')        
    with bar2:
        st.plotly_chart(APOSmonth_combo_profit, use_container_width=True)
        st.markdown('**Monthly sale = uptrend   \nMonthly profit amount = downw in month 5,6,8,12 which made profit-return lower.   \nprofit up/down probably due to types of item sold, rate of discount given....etc.   \n we do not have sale price data**')

st.markdown('** **')

#---------------------------------------------------------------------
st.subheader("6.2_ Results by AP Regions")

APOS_result_region=APOSonly.groupby(by=['Region']).aggregate({'Sales':'sum','Profit':'sum'})
APOS_result_region['profit_bySale']=(APOS_result_region['Profit']/APOS_result_region['Sales'])*100
APOS_result_region=APOS_result_region.dropna()
APOS_result_region

st.markdown('**High sales regions = O, SEA, SA, EA   \nWA = High sales but loss  \nCA = lower sales with loss**')
st.markdown('**Suggestion: Ocenia and SEA have highest sales but having lower profit return in comparing to SA/EA.**')

st.markdown('** **')



# ???? only AP regions ?????
# APOSReg=APOS[['Region','Sales','Profit']]
# P_APOSReg=APOSReg.pivot_table(index="Region",aggfunc='sum').dropna()
# P_APOSReg

# name = st.text_input("Enter Region to view county-level result table")
# aaa=APOSonly[APOSonly['Region']==name]
# st.dataframe(aaa.use_container_width=True)


# option=st.radio(label="Choose Region to view country-level result table",options=('Oceania','Southeastern Asia','Southern Asia','Eastern Asia','Western Asia','Central Asia'))

# if option == 'Oceania':
#     st.dataframe(APOSonly[APOSonly['Region']=='Oceania'].use_container_width=True)
# else:
#     "other"

#chat gpt
# name = st.text_input("Enter Region to view county-level result table")

# if name:
#     filtered_data = APOSonly[APOSonly['Region'] == name]
    
#     if not filtered_data.empty:
#         st.dataframe(filtered_data.style.highlight_max(axis=0))
#     else:
#         st.warning("No data available for the specified region.")

#---------------------------------------------------------------------
st.subheader("6.3_ Results by product sub-category at SEA, comparing to SA")

#APOS_SEA=APOS[(APOS['Region']=="Southeastern Asia")]
AP_SEA_OS=sd[(sd['orderyear']==2015) & (sd['Market']=="Asia Pacific") & (sd['Category']=='Office Supplies') & (sd['Region']=='Southeastern Asia')]

with st.expander("See detail result table here"):
    AP_SEA_OS

AP_SEA_OS_subcat=APOS.groupby('Sub-Category').aggregate({'Sales':'sum','Profit':'sum'}).reset_index()
AP_SEA_OS_subcat['profit_bySale']=(AP_SEA_OS_subcat['Profit']/AP_SEA_OS_subcat['Sales'])*100
AP_SEA_OS_subcat=AP_SEA_OS_subcat.dropna()
AP_SEA_OS_subcat   #??? how to highlight max

AP_SEA_OS_SC_Sale_boxplot = px.box(AP_SEA_OS, x="Sub-Category", y="Sales",title="Sales")
AP_SEA_OS_SC_Profit_boxplot  = px.box(AP_SEA_OS, x="Sub-Category", y="Profit",title='Profit')

graph_container= st.container()
with graph_container:
    graph1, graph2 = st.columns(2)
    with graph1:
        st.plotly_chart(AP_SEA_OS_SC_Sale_boxplot, use_container_width=True)
        st.markdown('**key sale contributing category are Appliances and Storage, among total 9 sub-categories.  Suggested to explore the reasons why other 7 sub-categories are with lower sale orders**')        
    with graph2:
        st.plotly_chart(AP_SEA_OS_SC_Profit_boxplot, use_container_width=True)
        st.markdown('**Major profit contributor is Appliance sub-category in SEA.  The second one, ie Storage, has narrow profit margin with several outliers.  Suggested to explore more about Storage.**')

st.markdown('** **')

#-----------------------------------------------------------------------
st.subheader("6.4_ Results of Items under 'Appliance' Sub-Category")

AP_SEA_OS_SC_Applianceall=sd[(sd['orderyear']==2015) & (sd['Market']=="Asia Pacific") & (sd['Category']=='Office Supplies') & (sd['Sub-Category']=='Appliances') & (sd['Region']=='Southeastern Asia')]

AP_SEA_OS_SC_Appliance=AP_SEA_OS_SC_Applianceall[['orderyear', 'ordermonth', 'Segment', 'OrderPriority', 'Country','City',
       'Sales', 'Discount','Profit', 'ShippingCost', 'DeliveryDays','ProductName',
       'Quantity']]

AP_SEA_OS_SC_Appliance=AP_SEA_OS_SC_Appliance.groupby('ProductName').aggregate({'Sales':'sum','Quantity':'sum','Profit':'sum'}).reset_index()
AP_SEA_OS_SC_Appliance['profit_bySale']=(AP_SEA_OS_SC_Appliance['Profit']/AP_SEA_OS_SC_Appliance['Sales'])*100
AP_SEA_OS_SC_Appliance=AP_SEA_OS_SC_Appliance.dropna()


with st.expander("See detail result table of Items under 'Appliance', here"):
    AP_SEA_OS_SC_Appliance

# ????cannot add color, ???how to filter by item.....
AP_SEA_OS_SC_Appliance_SaleProfit_scatterplot=px.scatter(AP_SEA_OS_SC_Appliance,color="ProductName",x="Sales",y="Profit",title="Sales vs Profit")
AP_SEA_OS_SC_Appliance_SaleDiscount_scatterplot=px.scatter(AP_SEA_OS_SC_Appliance,x="Sales",y="Quantity",title="Sales vs Quantity")


# graph_container= st.container()
# with graph_container:
#     graph1, graph2 = st.columns(2)
#     with graph1:
#         st.plotly_chart(AP_SEA_OS_SC_Appliance_SaleProfit_scatterplot, use_container_width=True)
#         st.markdown('**to add findings**')        
#     with graph2:
#         st.plotly_chart(AP_SEA_OS_SC_Appliance_SaleDiscount_scatterplot, use_container_width=True)
#         st.markdown('**to add findings**')


AP_SEA_OS_SC_Appliance_SaleQtyProfit_scatterplot= px.scatter_matrix(AP_SEA_OS_SC_Appliance,
    dimensions=["Sales", "Quantity", "Profit"],
    color="ProductName",title="Pattern of Sales vs Quantity vs Profit among Items under Appliance sub-category")
st.plotly_chart(AP_SEA_OS_SC_Appliance_SaleQtyProfit_scatterplot,use_container_width=True)
st.markdown('**Sales vs Profit = Hamilton Beach Refrigerator, White is the item with Highest sale and profit. In contrast, Hamilton Beach Microwave, White is the item with highest loss with high sales.   \nIn term of Quantity vs Profit... the finding is the same with these two items.   \nSALE ANALYSIS NEXT STEP:  \nTo explore individual items for new marketing actions, to consider least profit-return region and countries close out as necessary.**')
st.markdown('** **')

#-----------------------------------------------------------------------
#DRAFT


# ????cannot add color, ???how to filter by region.....
# AP_SEA_OS_SC_SaleProfit_scatterplot=px.scatter(AP_SEA_OS,x="Sales",y="Profit",title="Sales vs Profit")
# AP_SEA_OS_SC_SaleDiscount_scatterplot=px.scatter(AP_SEA_OS,x="Sales",y="Discount",title="Sales vs Discount")


# graph_container= st.container()
# with graph_container:
#     graph1, graph2 = st.columns(2)
#     with graph1:
#         st.plotly_chart(AP_SEA_OS_SC_SaleProfit_scatterplot, use_container_width=True)
#         st.markdown('**to add findings**')        
#     with graph2:
#         st.plotly_chart(AP_SEA_OS_SC_SaleDiscount_scatterplot, use_container_width=True)
#         st.markdown('**to add findings**')

# st.markdown('** **')




# APOSonly_SEAdes=APOSonly[APOSonly['Region']=='Southeastern Asia'].describe()
# APOSonly_SEAdes


# sd_sale_byCountry=sd.groupby('Country')['Sales'].sum().reset_index()

# map_sale_byCountry= px.choropleth(sd_sale_byCountry,locations='Country',locationmode='country names', color='Sales')
# st.plotly_chart(map_sale_byCountry)

# AP_SEA_OS_SalebyCountry= px.choropleth(AP_SEA_OS,locations='Country',locationmode='country names', color='Sales')
# st.plotly_chart(AP_SEA_OS_SalebyCountry)



# TO ASK

# ---- SIDEBAR ----
# st.sidebar.header("Please Filter Here:")
# market = st.sidebar.multiselect(
#     "Select the market:",
#     options=sd["Market"].unique(),
#     default=sd["Market"].unique())

# year = st.sidebar.multiselect(
#     "Select the year:",
#     options=sd["orderyear"].unique(),
#     default=sd["orderyear"].unique())

# sdsel = sd.query(
#     "Market == @market & orderyear ==@year")
