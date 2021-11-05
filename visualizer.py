import nflfastpy
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns; sns.set_style('whitegrid');



# load in our data
df = nflfastpy.load_pbp_data(year=2021)

# isolate the columns relevant to us
df = df[['yardline_100', 'rush_attempt', 'rusher_player_id', 'rusher_player_name']]

df = df.loc[df['rush_attempt'] == 1]

player_id_table = df[['rusher_player_id', 'rusher_player_name']].groupby('rusher_player_id', as_index=False).first()

df.head()

player_ids = df['rusher_player_id'].unique()

# instantiate our bins
new_df_data = {
    'rusher_player_id': [],
    '1 - 10 yardline': [],
    '11 - 20 yardline': [],
    '21 - 30 yardline': [],
    '31 - 40 yardline': [],
    '41 - 60 yardline': [],
    '61 - 80 yardline': [],
    '81 - 100 yardline': []
}
num_rushes = []
for player_id in player_ids:

    player_df = df.loc[df['rusher_player_id'] == player_id]

    rushes = player_df['yardline_100'].tolist()
    # only include players with greater than 10 rushing attempts
    if len(rushes) < 10:
        continue

    new_df_data['rusher_player_id'].append(player_id)

    levels = {
        '1 - 10 yardline': (-1, 11),
        '11 - 20 yardline': (10, 21),
        '21 - 30 yardline': (20, 31),
        '31 - 40 yardline': (30, 41),
        '41 - 60 yardline': (40, 61),
        '61 - 80 yardline': (60, 81),
        '81 - 100 yardline': (80, 100)
    }
    
    
    for level, (min, max) in levels.items():
        num_level_touches = len(list(filter(lambda x: x > min and x < max, rushes)))
        new_df_data[level].append(num_level_touches / len(rushes))
    num_rushes.append(len(rushes))

        
rushing_df = pd.DataFrame(new_df_data)
rushing_df['Attempts'] = num_rushes

# look up player's name using the player_id_table
rushing_df = rushing_df.merge(player_id_table, on='rusher_player_id', how='left')\
.set_index('rusher_player_name').drop('rusher_player_id', axis=1)

rushing_df.head()

# top 15 running backs
rushing_df = rushing_df.sort_values(by = 'Attempts',ascending = False).head(15)

# order by inside the 10 yardline
rushing_df_plot = rushing_df.sort_values(by='1 - 10 yardline')

# optional player selector

notable_players = ['A.Kamara', 'J.Jacobs', 
                   'J.Robinson', 'N.Chubb', 
                   'D.Montgomery', 'D.Cook',
                   'D.Henry', 'K.Hunt',
                   'Z.Moss', 'C.Edwards-Helaire',
                   'E.Elliot', 'J.Mixon']

# plot our visualization as a horizontal stacked bar plot
ax = rushing_df_plot.drop('Attempts',axis=1).plot.barh(stacked=True, colormap='tab20c',width = 0.5);

# adding text
c = 0
for i in rushing_df_plot['Attempts']:
    ax.text(0.01, -0.2 + c, i, size = 16)
    c +=1
ax.text(0,14.6,'Number of Rushes', size = 10)

plt.gcf().set_size_inches(10, 10);

ax.set_title('Where are RBs are getting their carries through week 5?', fontsize=12)
ax.legend(loc=1); # set the legend in the top right corner                   