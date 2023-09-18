#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_path = 'Cost of Resistance Database.xlsx'
df = pd.read_excel(file_path)

# copy the data frame


# change column names
df = df.rename(columns={'Doubling Time of Sensitive Population (in h)': 'doubling_time_sens',
                        'Doubling Time of Resistant Population (in h)': 'doubling_time_res',
                        'IC50 of Sensitive Population': 'ic50_sens',
                        'IC50 of Resistant Population': 'ic50_res'})

df_filt = df.copy()

# filter out NaN values in doubling time and ic50 columns
df_filt = df_filt[df_filt['doubling_time_sens'].notna()]
df_filt = df_filt[df_filt['doubling_time_res'].notna()]
df_filt = df_filt[df_filt['ic50_sens'].notna()]
df_filt = df_filt[df_filt['ic50_res'].notna()]

# filter out values that are strings
df_filt = df_filt[df_filt['doubling_time_sens'].apply(lambda x: isinstance(x, (int, np.int64, float, np.float64)))]
df_filt = df_filt[df_filt['doubling_time_res'].apply(lambda x: isinstance(x, (int, np.int64, float, np.float64)))]
df_filt = df_filt[df_filt['ic50_sens'].apply(lambda x: isinstance(x, (int, np.int64, float, np.float64)))]
df_filt = df_filt[df_filt['ic50_res'].apply(lambda x: isinstance(x, (int, np.int64, float, np.float64)))]

ic50_change = df_filt['ic50_res']/df_filt['ic50_sens']
df_filt['ic50_change'] = ic50_change

doubling_time_change = df_filt['doubling_time_res']/df_filt['doubling_time_sens']
df_filt['doubling_time_change'] = doubling_time_change

#%% Plot ic50 change vs growth rate change

fig,ax_list = plt.subplots(ncols=3,figsize=(10,3))

use_indx = df_filt['doubling_time_change'] > 1

ax = ax_list[0]
ax.scatter(df_filt['ic50_change'][use_indx], df_filt['doubling_time_change'][use_indx],color='k',alpha=0.7)
ax.set_xlabel('IC$_{50}$ ratio \n(resistant/sensitive)',fontsize=14)
ax.set_ylabel('Doubling time ratio \n(resistant/sensitive)',fontsize=14)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

ax.tick_params(axis='both', which='major', labelsize=12)

ax.set_xscale('log')
# ax.set_yscale('log')
yl = ax.get_ylim();
yl = (1,yl[1]);
ax.set_ylim(yl);

# %% now filter doubling time data only
df_filt = df.copy()

df_filt = df_filt[df_filt['doubling_time_sens'].notna()]
df_filt = df_filt[df_filt['doubling_time_res'].notna()]
df_filt = df_filt[df_filt['doubling_time_sens'].apply(lambda x: isinstance(x, (int, np.int64, float, np.float64)))]
df_filt = df_filt[df_filt['doubling_time_res'].apply(lambda x: isinstance(x, (int, np.int64, float, np.float64)))]

doubling_time_ratio = df_filt['doubling_time_res']/df_filt['doubling_time_sens']
df_filt['doubling_time_ratio'] = doubling_time_ratio

#%% histogram of doubling time ratio

# fig,ax = plt.subplots()
ax = ax_list[1]

use_indx = df_filt['doubling_time_ratio'] > 1

hist = ax.hist(df_filt['doubling_time_ratio'][use_indx],bins=10,color='k',alpha=0.7);

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.tick_params(axis='both', which='major', labelsize=12)

ax.set_xlabel('Doubling time ratio \n(resistant/sensitive)',fontsize=14)
ax.set_ylabel('Count',fontsize=14)
# %% now filter ic50 data only
df_filt = df.copy()

df_filt = df_filt[df_filt['ic50_sens'].notna()]
df_filt = df_filt[df_filt['ic50_res'].notna()]
df_filt = df_filt[df_filt['ic50_sens'].apply(lambda x: isinstance(x, (int, np.int64, float, np.float64)))]
df_filt = df_filt[df_filt['ic50_res'].apply(lambda x: isinstance(x, (int, np.int64, float, np.float64)))]

ic50_ratio = df_filt['ic50_res']/df_filt['ic50_sens']
df_filt['ic50_ratio'] = ic50_ratio

#%% histogram of ic50 ratio

# fig,ax = plt.subplots()
ax = ax_list[2]

ic50_ratio_log = np.log10(np.array(ic50_ratio).astype(float))

doubling_time_ratio = df_filt['doubling_time_res']/df_filt['doubling_time_sens']
use_indx = doubling_time_ratio > 1

hist = ax.hist(ic50_ratio_log[use_indx],bins=10,color='k',alpha=0.7);

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.tick_params(axis='both', which='major', labelsize=12)

ax.set_xlabel('IC$_{50}$ ratio \n(resistant/sensitive)',fontsize=14)
ax.set_ylabel('Count',fontsize=14)
# ax.set_xscale('log')
fig.tight_layout()
# %%
