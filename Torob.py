import pyodbc
import pandas as pd
import matplotlib.pyplot as plt

# Establish a connection to the SQL Server
conn = pyodbc.connect("Driver={SQL Server};Server=.\MSSQL2019;Database=PythonData;Trusted_Connection=yes;")

# Query to retrieve data from the ProdoctInfo table
query1 = """
SELECT [id]
      ,[category_name]
      ,[titles]
      ,[min_price]
      ,[max_price]
      ,[avg_price]
      ,[min_num_shops]
      ,[max_num_shops]
      ,[avg_num_shops]
FROM [dbo].[ProdoctInfo]
"""

# Query to retrieve data from the TorobInfo table
query2 = """
SELECT [raw_query]
      ,[result]
      ,[clicked_result]
      ,[clicked_rank]
      ,[timestamp]
FROM [dbo].[TorobInfo]
"""

# Execute the queries and fetch the data
prodoct_info_data = pd.read_sql(query1, conn)
torob_info_data = pd.read_sql(query2, conn)


#Get a Sample Data From These Tables
QueryJoin='SELECT TOP(100000) P.* ,t.raw_query,t.clicked_rank,t.clicked_result,t.result,t.timestamp FROM ProdoctInfo AS p ' \
          'INNER JOIN TorobInfo AS t ON CAST(p.id AS NVARCHAR(50)) =  t.clicked_result '
# order BY NEWID()
join_info_data = pd.read_sql(QueryJoin, conn)


#-----------------------------------------------------------------------------------------------------------------------
#سوال 1
#با یک نمودار نشان دهید ایا تفاوت معناداری از لحاظ تعداد کلیک بر روی آیتم های یک کتگوری وجود دارد یا نه؟

# Plot a scatter plot to investigate the relationship between the title length and the number of clicks
# plt.figure(figsize=(10,5))
# a= join_info_data.loc[join_info_data['category_name'] == 'پخش خودرو']
# plt.bar(a['raw_query'], a['clicked_rank'])
# plt.xlabel('raw_query')
# plt.ylabel('Number of clicks')
# plt.show()


#-----------------------------------------------------------------------------------------------------------------------
#سوال2
#با یک نمودار نشان دهید احتمال کلیک شدن ایتم ها به طول اسم ایتم وابستگی ندارد
# plt.scatter(join_info_data["clicked_result"].str.len(), join_info_data["clicked_rank"])
# plt.xlabel("Item Name Length")
# plt.ylabel("Average rank of item clicked")
# plt.title("Item Name Length vs. Average rank of item clicked")
# plt.show()



#-----------------------------------------------------------------------------------------------------------------------
#سوال3
#ایتم ها را بر اساس تعداد کلیک مرتب کنید و برای هر کتگوری 10 ایتم پر کلیک را نشان دهید
# # Group the data by category name and product title, and count the number of clicks
# click_counts = join_info_data.groupby(['category_name', 'result'])['clicked_result'].sum()
# click_counts = click_counts.reset_index()
#
# # Sort the products based on the number of clicks for each category
# sorted_df = click_counts.groupby('category_name').apply(lambda x: x.sort_values(by='clicked_result', ascending=False))
#
# # Display the top 10 most clicked products for each category
# for category in sorted_df.index.levels[0]:
#     print('Top 10 most clicked products in', category)
#     print(sorted_df.loc[category].head(10))
#     print()
# #-----------------------------------------------------------------------------------------------------------------------
#سوال4
#یک نمودار Scatter رسم کنید که هر نقطه ان یک محصول و محور افقی تعداد دفعاتی است که ایتم بازیابی شده است
# و محور عمودی تعداد دفعاتی است که ایتم کلیک شده است. ایا این دو متغییر همبستگی دارند



# resultID = join_info_data.explode('result')['result']
# NumOfResultID = resultID.value_counts().reset_index(name='NumOfResultID')
#
# clickedResultID = join_info_data.explode('clicked_result')['clicked_result']
# NumOfResultIDClicked = clickedResultID.value_counts().reset_index(name='NumOfResultIDClicked')
#
# join_info_data_merged = NumOfResultID.merge(NumOfResultIDClicked, on='index', how='outer').fillna(0)
#
# plt.scatter(join_info_data_merged['NumOfResultID'], join_info_data_merged['NumOfResultIDClicked'])
# plt.xlabel('Number of retrieved items')
# plt.ylabel('Number of clicked items')
# plt.show()

# query = "SELECT result, clicked_result FROM [TorobInfo]"
# df = pd.read_sql(query, conn)
# NewDataFrame = pd.DataFrame(columns=['retrieved', 'clicked'])
# join_info_data['result'] = join_info_data['result'].str.split(',')
# join_info_data['clicked_result'] = join_info_data['clicked_result'].str.split(',')
# NewDataFrame = pd.DataFrame(columns=['retrieved_Data', 'clicked_Data'])
#
for _, row in join_info_data.iterrows():
    retrieved_Data = len(row['result'])
    clicked_Data = len(row['clicked_result'])
    NewDataFrame = NewDataFrame.append({'retrieved_Data': retrieved_Data, 'clicked_Data': clicked_Data}, ignore_index=True)
#
plt.figure(figsize=(10,5))
plt.scatter(NewDataFrame['retrieved_Data'], NewDataFrame['clicked_Data'])
plt.xlabel('Average number of shops')
plt.ylabel('Clicked rank')
plt.show()



# join_info_data = pd.read_sql(QueryJoin, conn)
# join_info_data['result'] = join_info_data['result'].str.split(',')
# join_info_data['clicked_result'] = join_info_data['clicked_result'].str.split(',')
# NewDataFrame = pd.DataFrame(columns=['retrieved_Data', 'clicked_Data'])
#
# for _, row in join_info_data.iterrows():
#     retrieved_Data = len(row['result'])
#     clicked_Data = len(row['clicked_result'])
#     NewDataFrame = NewDataFrame.append({'retrieved_Data': retrieved_Data, 'clicked_Data': clicked_Data}, ignore_index=True)
#
# plt.figure(figsize=(10,5))
# plt.scatter(NewDataFrame['retrieved_Data'], NewDataFrame['clicked_Data'])
# plt.xlabel('Retrieved data')
# plt.ylabel('Clicked data')
# plt.show()


# retrieval_counts = join_info_data.groupby('result')['raw_query'].count()
# click_counts = join_info_data.groupby('result')['clicked_result'].sum()
#
# # merged_df = pd.merge(df1, retrieval_counts, left_on='titles', right_on='result')
# merged_df = pd.merge(retrieval_counts, click_counts, left_on='retrieval_result', right_on='clicked_result')
# # corr = merged_df['raw_query'].corr(merged_df['clicked_result'])
# # print('Pearson correlation coefficient:', corr)
# # Plot a scatter plot to investigate the correlation between the number of retrievals and clicks
# plt.figure(figsize=(10,5))
# plt.scatter(merged_df['raw_query'], merged_df['clicked_result'])
# plt.xlabel('Retrieval count')
# plt.ylabel('Click count')
# plt.show()