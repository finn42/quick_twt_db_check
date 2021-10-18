import sys
import os
import time
import datetime as dt
import math
import numpy as np 
import scipy as sp
import pandas as pd
import pingouin as pg


# facilitate counting of 
def ind_set(df,col_sorted,thresh1,thresh2):
    t1 = df[col_sorted].searchsorted(thresh1)
    t2 = df[col_sorted].searchsorted(thresh2)
    return df.loc[t1:t2-1]

def ind_set_counts(df,col_sort,bins):
	#bins is a series/array of stamps in the same value as that in sorted colum of df col_sorted
	df=df.sort_values(col_sort).reset_index()
	df_counted = pd.DataFrame()
	df_counted['Bounds']= bins
	df_counted['Counts'] = 0
	for i in range(len(df_counted)-1):
		df_sub = ind_set(df,col_sort,bins[i],bins[i+1])
		df_counted.loc[i,'Counts']=len(df_sub) #or maybe it's 1?

	df_sub =df.loc[df[col_sort].searchsorted(bins[len(bins)-1]):]
	df_counted.loc[len(bins)-1,'Counts']=len(df_sub) #or maybe it's 1?
	return df_counted

def ind_set_unique_counts(df,col_sorted,col_unique,bins):
	#bins is a series/array of stamps in the same value as that in sorted colum of df col_sorted
	df=df.sort_values(col_sorted).reset_index()
	df_counted = pd.DataFrame()
	df_counted['Bounds']= bins
	df_counted['Counts'] = 0
	for i in range(len(df_counted)-1):
		df_sub = ind_set(df,col_sorted,bins[i],bins[i+1])
		df_counted.loc[i,'Counts']=len(df_sub[col_unique].unique()) #or maybe it's 1?

	df_sub =df.loc[df[col_sorted].searchsorted(bins[len(bins)-1]):]
	df_counted.loc[len(bins)-1,'Counts']=len(df_sub[col_unique].unique()) #or maybe it's 1?
	return df_counted

def status_url(twt_series):
    # twt_series is a single row of tweet information from API
    #https://twitter.com/Mr_AZ_Fell/status/1401564080486420480
    # twitter.com/anyuser/status/
    # url = 'https://twitter.com/' + twt_series['user_screen_name'] + '/status/' + str(twt_series['id'])
    url = 'https://twitter.com/anyuser/status/' + str(int(twt_series['id']))
    print(url)
    return url

def citation(row): 
    # function to output details of a twt in APA
    # input: row from tweet database
    # output: human readable text string
    twt_dets = row['user_name'] + ' [@' + row['user_screen_name'] + ']' + '. ' + row['created_at'].strftime('(%Y, %m %d)') + '. ' + row['tweet'].replace('\n', ' ').replace('\r', '') + '[Tweet]. Twitter. '  + 'https://twitter.com/anyuser/status/' + str(int(row['id']))
    
    return twt_dets
    
def twt_dets(row): 
    # function to output more details of a twt 
    # input: row from tweet database
    # output: human readable text string
    
    twt_dets = row['user_name'] + ' [@' + row['user_screen_name'] + '],' + str(row['created_at']) + ':\n' + 'https://twitter.com/anyuser/status/' + str(int(row['id'])) + '\n' + row['tweet'] + '\n'
    
    if not np.isnan(row['retweeted_status_id']):
        twt_dets += 'RTs: ' + str(int(row['retweeted_status_retweet_count']))  + '\nLikes: ' + str(int(row['retweeted_status_favorite_count'])) + '\n'    

    if not np.isnan(row['in_reply_to_status_id']):
        twt_dets += 'Reply to [@' + row['in_reply_to_user_screen_name'] + ']: ' + 'https://twitter.com/anyuser/status/' + str(int(row['in_reply_to_status_id'])) + '\n'
    
    if not np.isnan(row['quoted_status_id']):
        twt_dets += 'Quote of ' + row['quoted_status_user_name'] + ' [@' + row['quoted_status_user_screen_name'] +  ']: ' + 'https://twitter.com/anyuser/status/' + str(int(row['quoted_status_id'])) + '\n'
        twt_dets += 'RTs: ' + str(int(row['quoted_status_retweet_count']))  + '\nLikes: ' + str(int(row['quoted_status_favorite_count'])) + '\n'    

    return twt_dets 
