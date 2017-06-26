import re
import unicodedata
import numpy as np
import pandas as pd
import requests as r
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time

# get time now
last_updated_raw = datetime.now() #- timedelta(hours = 4)
last_updated = last_updated_raw.strftime('%B %d, %Y, %-I:%M %p') + ' Eastern Time'

flower_dict = {
    'ROSE': {'tank_id': 45863,
             'section': 0,
             'seq': 0,
             'main_tank_id': None,
             'main_tank': 'Cross-Walk Calvin',
             'main_color': 'purple',
             'main_awards_html': '<span class="awards-sprite a0-3"></span><span class="awards-sprite a1-2"></span><span class="awards-sprite a2-2"></span><span class="awards-sprite a3-2"></span><span class="awards-sprite a5-2"></span><span class="awards-sprite a6-1"></span><span class="awards-sprite a7-1"></span>'},
    'LOTUS': {'tank_id': 46146,
              'section': 0,
              'seq': 1,
              'main_tank_id': None,
              'main_tank': 'SoMeBoDy',
              'main_color': 'purple',
              'main_awards_html': '<span class="awards-sprite a0-3"></span><span class="awards-sprite a1-3"></span><span class="awards-sprite a2-3"></span><span class="awards-sprite a3-3"></span><span class="awards-sprite a4-3"></span><span class="awards-sprite a5-2"></span>'},
    'TULIP': {'tank_id': 45920,
              'section': 0,
              'seq': 2,
              'main_tank_id': None,
              'main_tank': 'SSpritEE',
              'main_color': 'red',
              'main_awards_html': '<span class="awards-sprite a0-3"></span><span class="awards-sprite a3-1"></span><span class="awards-sprite a5-3"></span>'},
    'HIBISCUS': {'tank_id': 45859,
                 'section': 0,
                 'seq': 3,
                 'main_tank_id': 850,
                 'main_tank': None,
                 'main_color': None,
                 'main_awards_html': None},
    'DAHLIA': {'tank_id': 48641,
               'section': 0,
               'seq': 4,
               'main_tank_id': 10502,
                 'main_tank': None,
                 'main_color': None,
                 'main_awards_html': None},
    'GLADIOLUS': {'tank_id': 48059,
                  'section': 0,
                  'seq': 5,
                  'main_tank_id': None,
                  'main_tank': 'Battlefield-2',
                  'main_color': 'purple',
                  'main_awards_html': '<span class="awards-sprite a0-3"></span><span class="awards-sprite a1-3"></span><span class="awards-sprite a2-3"></span><span class="awards-sprite a3-3"></span><span class="awards-sprite a4-3"></span><span class="awards-sprite a5-3"></span><span class="awards-sprite a6-1"></span><span class="awards-sprite a8-1"></span>'},
    'HYDRANGEA': {'tank_id': 49521,
                  'section': 0,
                  'seq': 6,
                  'main_tank_id': None,
                  'main_tank': 'KILLER12',
                  'main_color': 'red',
                  'main_awards_html': '<span class="awards-sprite a0-3"></span><span class="awards-sprite a1-3"></span><span class="awards-sprite a2-3"></span><span class="awards-sprite a3-3"></span><span class="awards-sprite a5-2"></span>'},
    'VIOLET': {'tank_id': 50618,
                'section': 0,
                'seq': 7,
                'main_tank_id': 575,
                'main_tank': None,
                'main_color': None,
                'main_awards_html': None},
    'DAISY': {'tank_id': 48103,
              'section': 0,
              'seq': 8,
              'main_tank_id': 6281,
              'main_tank': None,
              'main_color': None,
              'main_awards_html': None},
    'LILAC': {'tank_id': 47770,
              'section': 0,
              'seq': 9,
              'main_tank_id': None,
              'main_tank': 'Secret',
              'main_color': 'gray',
              'main_awards_html': None},
    'ORCHID': {'tank_id': 47786,
               'section': 0,
               'seq': 10,
               'main_tank_id': None,
               'main_tank': 'Secret',
               'main_color': 'gray',
               'main_awards_html': None},
    'TRILLIUM': {'tank_id': 48665,
                 'section': 1,
                 'seq': 0,
                 'main_tank_id': 48059,
                 'main_tank': None,
                 'main_color': None,
                 'main_awards_html': None},
    'CHRYSANTHEMUM': {'tank_id': 47835,
                      'section': 1,
                      'seq': 1,
                      'main_tank_id': 45863,
                      'main_tank': None,
                      'main_color': None,
                      'main_awards_html': None},
    'JASMINE': {'tank_id': 48487,
                'section': 1,
                'seq': 2,
                'main_tank_id': 46146,
                'main_tank': None,
                'main_color': None,
                'main_awards_html': None},
    'BUTTERCUP': {'tank_id': 48264,
                  'section': 1,
                  'seq': 3,
                  'main_tank_id': 50618,
                  'main_tank': None,
                  'main_color': None,
                  'main_awards_html': None},
    'terrestrial TULIP': {'tank_id': 48240,
                          'section': 1,
                          'seq': 4,
                          'main_tank_id': 45920,
                          'main_tank': None,
                          'main_color': None,
                          'main_awards_html': None},
    'radiant ROSE': {'tank_id': 48222,
                     'section': 1,
                     'seq': 5,
                     'main_tank_id': 45863,
                     'main_tank': None,
                     'main_color': None,
                     'main_awards_html': None},
    'luminosity LOTUS': {'tank_id': 50111,
                         'section': 1,
                         'seq': 6,
                         'main_tank_id': 46146,
                         'main_tank': None,
                         'main_color': None,
                         'main_awards_html': None},
    'DESERT ROSE': {'tank_id': 49974,
                     'section': 1,
                     'seq': 7,
                     'main_tank_id': 45863,
                     'main_tank': None,
                     'main_color': None,
                     'main_awards_html': None},
    'SILENT LOTUS': {'tank_id': 49966,
                     'section': 1,
                     'seq': 8,
                     'main_tank_id': 46146,
                     'main_tank': None,
                     'main_color': None,
                     'main_awards_html': None},
    'BLACK DAHLIA': {'tank_id': 50007,
                     'section': 1,
                     'seq': 9,
                     'main_tank_id': 48641,
                     'main_tank': None,
                     'main_color': None,
                     'main_awards_html': None}
}

#----- Scraper functions

def scrape_text_from_link(link):
    trials = 0
    try:
        response = r.get(link)
    except:
        time.sleep(5)
        trials += 1
        if trials < 10:
            scrape_text_from_link(link)
    return BeautifulSoup(response.text, 'lxml')

def check_remove_key(my_dict, key_name):
    if my_dict.has_key(key_name):
        my_dict.pop(key_name)
    return my_dict

def check_add_empty_key(my_dict, key_name):
    if my_dict.has_key(key_name):
        pass
    else:
        my_dict[key_name] = ''
    return my_dict

def replace_color_value(color):
    if color == 'color0':
        color = 'red'
    if color == 'color1':
        color = 'purple'
    if color == 'color2':
        color = 'blue'
    if color == 'color3':
        color = 'orange'
    return color

def create_tables_from_page_html(tank_results_html, tank_id, my_map = 'World', last_updated_raw = last_updated_raw):
    # make sure tank exists
    if tank_results_html.find_all('div', class_ = 'tank-header'):
        tank_dict = {}
        for t in tank_results_html.find_all('div', class_ = 'tank-header'):
            for i in t.find_all('h1'):
                i_str = str(i)
                # if tank has awards
                if re.search('awards-sprite', i_str):
                    awards_start = i_str.find('<span')
                    # replace multi-whitespace with single whitespace
                    awards = i_str[awards_start:]
                    awards = re.sub('\\s+', ' ', awards)
                    awards = awards.split(' ')
                    tank_awards_html = ' '.join(awards[:-1])
                    i_str = i_str[:awards_start]
                # if tank does not have awards
                else:
                    tank_name_end = i_str.find('</h1>')
                    i_str = i_str[:tank_name_end]
                    tank_awards_html = ''
                tank_name_start = i_str.find('">') + 2
                tank_name = i_str[tank_name_start:].strip()
                tank_color = i_str[11:tank_name_start-2]
                # structure fields
                tank_dict['tank_name'] = tank_name
                tank_dict['tank_color'] = replace_color_value(tank_color)
                tank_dict['tank_awards_html'] = tank_awards_html
                tank_dict['tank_id'] = tank_id
                pd.DataFrame([tank_dict])
        for t in tank_results_html.find_all('div', class_ = 'section-tank-mapset-info'):
            for tank_map in t.find_all('h2'):
                tank_map = tank_map.text
                tank_map = re.sub('\\s+', '', tank_map)
                if tank_map == my_map:
                    for row in t.find_all('tr'):
                        cols = row.find_all('td')
                        # cleaning attribute name
                        attribute_name = cols[0].text
                        attribute_name = re.sub('\\:\\s+', '', attribute_name)
                        attribute_name = re.sub(' ', '_', attribute_name)
                        attribute_name = attribute_name.lower()
                        # cleaning attribute value
                        attribute_value = cols[1].text
                        attribute_value = re.sub('\\s+', '', attribute_value)
                        tank_dict[attribute_name] = attribute_value
        for j in ['rank', 'promotion_points']:
            tank_dict = check_remove_key(tank_dict, j)
        for j in ['kills', 'deactivated', 'time_played']:
            tank_dict = check_add_empty_key(tank_dict, j)
    tank_dict['time'] = last_updated_raw
    return pd.DataFrame([tank_dict])

def extract_time(time_played, time_index):
    try:
        time_list = time_played.split(':')
        time_piece = time_list[time_index]
        if time_piece == '':
            return 0
        else:
            return time_piece
    except:
        return 0

def loop_all_flowers(flower_dict = flower_dict, no_param_url = 'https://tankpit.com/tank_profile/?tank_id='):
    master_tanks_df = pd.DataFrame()
    # flower tanks
    for flower_info_dict in flower_dict.values():
        tank_id = flower_info_dict['tank_id']
        # scrape
        tank_results_html = scrape_text_from_link(no_param_url + str(tank_id))
        # make tables
        tanks_df = create_tables_from_page_html(tank_results_html, tank_id)
        if flower_info_dict['section'] == 0:
            tanks_df['tank_cat'] = 0
        if flower_info_dict['section'] == 1:
            tanks_df['tank_cat'] = 1
        # check to make sure not an empty row (col 1 = time, col 2 = tank_cat)
        if tanks_df.shape[1] > 2:
            # concat
            master_tanks_df = pd.concat([master_tanks_df, tanks_df], axis = 0)
    # main tanks
    for flower_info_dict in flower_dict.values():
        tank_id = flower_info_dict['main_tank_id']
        section = flower_info_dict['section']
        if tank_id != None and section == 0:
            # scrape
            tank_results_html = scrape_text_from_link(no_param_url + str(tank_id))
            # make tables
            tanks_df = create_tables_from_page_html(tank_results_html, tank_id)
            tanks_df['tank_cat'] = 2
            # check to make sure not an empty row (col 1 = time, col 2 = tank_cat)
            if tanks_df.shape[1] > 2:
                # concat
                master_tanks_df = pd.concat([master_tanks_df, tanks_df], axis = 0)
    # re-order cols
    master_tanks_df = master_tanks_df[["time", "tank_id", "tank_name", "tank_color", "tank_awards_html", "kills", "deactivated", "time_played", "tank_cat"]]
    master_tanks_df.reset_index(drop = True, inplace = True)
    # structuring time
    master_tanks_df['time_played_hours'] = master_tanks_df['time_played'].apply(lambda x: extract_time(x, 0)).astype(int)
    master_tanks_df['time_played_mins'] = master_tanks_df['time_played'].apply(lambda x: extract_time(x, 1)).astype(int)
    master_tanks_df['time_played_secs'] = master_tanks_df['time_played'].apply(lambda x: extract_time(x, 2)).astype(int)
    master_tanks_df['time_played_decimal'] = master_tanks_df['time_played_hours'] + (master_tanks_df['time_played_mins'] / 60.) + (master_tanks_df['time_played_secs'] / 3600.)
    return master_tanks_df

#----- Hours log functions

def change_nas_to_zeros(df):
    return df.fillna(0)

def change_zeros_to_nas(df):
    return df[df != 0]

def format_time_col(df, time_col = 'time', time_format = '%Y-%m-%d %H:%M:%S'):
    df[time_col] = pd.to_datetime(df[time_col], format = time_format)
    return df

def concat_now_to_alltime_long(df_T, df_now, stat = 'time_played_decimal', time_col = 'time'):
    tmp_dict = {}
    tmp_dict[time_col] = list(df_now[time_col])[0]
    for i in range(df_now.shape[0]):
        if df_now.ix[i, 'tank_cat'] in [0, 1]:
            tmp_dict[str(df_now.ix[i, 'tank_id'])] = df_now.ix[i, stat]
    df_T = pd.concat([df_T, pd.DataFrame([tmp_dict])], axis = 0)
    df_T.reset_index(drop = True, inplace = True)
    return df_T

def groupby_max_time(df_T, time_col = 'time'):
    cols = [i for i in df_T.columns if i != time_col]
    df_T = change_nas_to_zeros(df_T)
    df_T = df_T.groupby(cols, as_index = False)[time_col].max()
    df_T = df_T.sort_values(time_col)
    df_T.reset_index(drop = True, inplace = True)
    return df_T

#----- Sum diff functions

def subset_df_to_timeframe(df, days, time_col = 'time'):
    time_earliest = datetime.now() - timedelta(hours = 4) - timedelta(minutes = 60 * 24 * days)
    df = format_time_col(df)
    df = df.ix[df[time_col] > time_earliest, :]
    df.reset_index(drop = True, inplace = True)
    return df

def get_diff_df(df, time_col = 'time'):
    df = df.set_index(time_col).diff()
    df.reset_index(drop = False, inplace = True)
    df = df.drop(0, axis = 0)
    df.reset_index(drop = True, inplace = True)
    df = change_nas_to_zeros(df)
    return df

def sum_diff(df, diff_col_name, time_col = 'time'):
    df = df.drop(time_col, axis = 1)
    df = df[(df < 20) & (df > 0)]
    df = change_nas_to_zeros(df)
    df = df.sum()
    df = df.reset_index(drop = False)
    df.columns = ['tank_id', diff_col_name]
    df[diff_col_name] = df[diff_col_name].round(2)
    df['tank_id'] = df['tank_id'].astype(int)
    return df

#----- Roster functions

def write_md_from_tank_id(roster, df, tank_id, end = 'yes'):
    roster.write('|<span class="')
    roster.write(list(df.ix[df['tank_id'] == tank_id, 'tank_color'])[0])
    roster.write('">')
    roster.write(list(df.ix[df['tank_id'] == tank_id, 'tank_name'])[0])
    roster.write('</span><span class="awards-container">')
    roster.write(list(df.ix[df['tank_id'] == tank_id, 'tank_awards_html'])[0])
    roster.write('</span>')
    if end == 'yes':
        roster.write('|\n')

def make_roster_md(roster_out_file, df_now, flower_dict = flower_dict, last_updated = last_updated):
    roster = open(roster_out_file, 'w')
    roster.write('\n## ROSTER\n\n')
    roster.write('{:.roster}\n')
    roster.write('|<span class="roster_header">Flower</span>')
    roster.write('|<span class="roster_header">Main Tank</span>|\n')
    # main flowers
    for j in range(len(flower_dict)):
        for i in flower_dict.values():
            if i['seq'] == j and i['section'] == 0:
                write_md_from_tank_id(roster, df_now, tank_id = i['tank_id'], end = 'no')
                if i['main_tank_id'] != None:
                    write_md_from_tank_id(roster, df_now, tank_id = i['main_tank_id'])
                else:
                    roster.write('|<span class="')
                    roster.write(i['main_color'])
                    roster.write('">')
                    roster.write(i['main_tank'])
                    roster.write('</span>')
                    if i['main_tank'] != 'Secret':
                        roster.write('<span class="awards-container">')
                        roster.write(i['main_awards_html'])
                        roster.write('</span>')
                    roster.write('|\n')
    roster.write('\n## ALTS\n\n')
    # alts
    roster.write('{:.roster}\n')
    roster.write('|<span class="roster_header">Alt</span>')
    roster.write('|<span class="roster_header">Main Flower</span>|\n')
    for j in range(len(flower_dict)):
        for i in flower_dict.values():
            if i['seq'] == j and i['section'] == 1:
                write_md_from_tank_id(roster, df_now, tank_id = i['tank_id'], end = 'no')
                write_md_from_tank_id(roster, df_now, tank_id = i['main_tank_id'], end = 'yes')
    roster.write('\n## LAST UPDATED\n\n')
    roster.write('<span class="last_updated">')
    roster.write(last_updated)
    roster.write('</span>')
    roster.close()

#----- Stats functions

def write_stats_md_from_index(stats, df, i, col1, col2, col3):
    stats.write('|<span class="')
    stats.write(df.ix[i, 'tank_color'])
    stats.write('">')
    stats.write(df.ix[i, 'tank_name'])
    stats.write('</span><span class="awards-container">')
    stats.write(df.ix[i, 'tank_awards_html'])
    stats.write('</span>|<span class="stat stat_hours' + col1 + '">')
    stats.write(df.ix[i, 'time_played'])
    stats.write('</span>|<span class="stat stat_kills' + col2 + '">')
    stats.write(df.ix[i, 'kills'])
    stats.write('</span>|<span class="stat stat_deactivated' + col3 + '">')
    stats.write(df.ix[i, 'deactivated'])
    stats.write('</span>|\n')

def make_stats_md(stats_out_file, df_now, sort_by, sort_list, flower_dict = flower_dict, last_updated = last_updated):
    # some logic to determine which column get bolded
    col_sorted = ' stat_sorted'
    col_sorted_extra = ' &nbsp;&darr;'
    col1, col1_link, col1_extra, col2, col2_link, col2_extra, col3, col3_link, col3_extra = '', '', '', '', '', '', '', '', ''
    if sort_by == 'time_played_decimal':
        col1 = col_sorted
        col1_extra = col_sorted_extra
        col2_link = '<a href="https://tankpit-flowers.github.io/stats-kills">'
        col2_extra = '</a>'
        col3_link = '<a href="https://tankpit-flowers.github.io/stats-deact">'
        col3_extra = '</a>'
    if sort_by == 'kills_decimal':
        col2 = col_sorted
        col2_extra = col_sorted_extra
        col1_link = '<a href="https://tankpit-flowers.github.io/stats">'
        col1_extra = '</a>'
        col3_link = '<a href="https://tankpit-flowers.github.io/stats-deact">'
        col3_extra = '</a>'
    if sort_by == 'deactivated_decimal':
        col3 = col_sorted
        col3_extra = col_sorted_extra
        col1_link = '<a href="https://tankpit-flowers.github.io/stats">'
        col1_extra = '</a>'
        col2_link = '<a href="https://tankpit-flowers.github.io/stats-kills">'
        col2_extra = '</a>'
    # writeout
    stats = open(stats_out_file, 'w')
    stats.write('\n## STATS\n\n')
    stats.write('{:.stats}\n')
    stats.write('|<span class="stat_header">Flower</span>')
    stats.write('|<span class="stat_header stat_hours' + col1 + '">' + col1_link + 'Hours' + col1_extra + '</span>')
    stats.write('|<span class="stat_header stat_kills' + col2 + '">' + col2_link + 'Kills' + col2_extra + '</span>')
    stats.write('|<span class="stat_header stat_deactivated' + col3 + '">' + col3_link + 'Deact.' + col3_extra + '</span>|\n')
    flower_df = pd.DataFrame()
    for i in flower_dict.values():
        flower_df = pd.concat([flower_df, df_now.ix[df_now['tank_id'] == i['tank_id'], ['tank_name', 'tank_color', 'tank_awards_html', 'time_played', 'time_played_decimal', 'kills', 'deactivated']]], axis = 0) 
    flower_df['kills_decimal'] = flower_df['kills']
    flower_df.ix[flower_df['kills_decimal'] == '', 'kills_decimal'] = None
    flower_df['kills_decimal'] = flower_df['kills_decimal'].fillna('0')
    flower_df['kills_decimal'] = flower_df['kills_decimal'].astype(float)
    flower_df['deactivated_decimal'] = flower_df['deactivated']
    flower_df.ix[flower_df['deactivated_decimal'] == '', 'deactivated_decimal'] = None
    flower_df['deactivated_decimal'] = flower_df['deactivated_decimal'].fillna('0')
    flower_df['deactivated_decimal'] = flower_df['deactivated_decimal'].astype(float)
    flower_df = flower_df.sort_values(sort_list, ascending = False)
    flower_df.reset_index(drop = True, inplace = True)
    for i in range(flower_df.shape[0]):
        write_stats_md_from_index(stats, flower_df, i, col1, col2, col3)
    stats.write('\n## LAST UPDATED\n\n')
    stats.write('<span class="last_updated">')
    stats.write(last_updated)
    stats.write('</span>')
    stats.close()

#----- Activity functions

def make_string_clean_zero(my_number, round_to = 2):
    my_number = str(round(my_number, round_to))
    if my_number == '0.0':
        my_number = ''
    # else:
    #     if make_time == True:
    #         # also turn decimal into time format with colon
    #         hours, minutes = my_number.split('.')
    #         minutes = int(np.ceil((int(minutes) / 100.) * 60., 0))
    #         if minutes >= 10:
    #             my_number = hours + ':' + str(minutes)
    #         else:
    #             my_number = hours + ':0' + str(minutes)
    return my_number

def write_activity_md_from_index(activity, df, i, col1, col2, col3):
    activity.write('|<span class="')
    activity.write(df.ix[i, 'tank_color'])
    activity.write('">')
    activity.write(df.ix[i, 'tank_name'])
    activity.write('</span><span class="awards-container">')
    activity.write(df.ix[i, 'tank_awards_html'])
    activity.write('</span>|<span class="activity activity_col1' + col1 + '">')
    activity.write(make_string_clean_zero(df.ix[i, 'hours_day']))
    activity.write('</span>|<span class="activity activity_col2' + col2 + '">')
    activity.write(make_string_clean_zero(df.ix[i, 'hours_week']))
    activity.write('</span>|<span class="activity activity_col3' + col3 + '">')
    activity.write(make_string_clean_zero(df.ix[i, 'hours_month']))
    activity.write('</span>|\n')

def make_activity_md(activity_out_file, df_now, sort_by, sort_list, flower_dict = flower_dict, last_updated = last_updated):
    # some logic to determine which column get bolded
    col_sorted = ' activity_sorted'
    col_sorted_extra = ' &nbsp;&darr;'
    col1, col1_link, col1_extra, col2, col2_link, col2_extra, col3, col3_link, col3_extra = '', '', '', '', '', '', '', '', ''
    if sort_by == 'hours_day':
        col1 = col_sorted
        col1_extra = col_sorted_extra
        col2_link = '<a href="https://tankpit-flowers.github.io/activity-week">'
        col2_extra = '</a>'
        col3_link = '<a href="https://tankpit-flowers.github.io/activity-month">'
        col3_extra = '</a>'
    if sort_by == 'hours_week':
        col2 = col_sorted
        col2_extra = col_sorted_extra
        col1_link = '<a href="https://tankpit-flowers.github.io/activity">'
        col1_extra = '</a>'
        col3_link = '<a href="https://tankpit-flowers.github.io/activity-month">'
        col3_extra = '</a>'
    if sort_by == 'hours_month':
        col3 = col_sorted
        col3_extra = col_sorted_extra
        col1_link = '<a href="https://tankpit-flowers.github.io/activity">'
        col1_extra = '</a>'
        col2_link = '<a href="https://tankpit-flowers.github.io/activity-week">'
        col2_extra = '</a>'
    # writeout
    activity = open(activity_out_file, 'w')
    activity.write('\n## HOURS OF ACTIVITY\n\n')
    activity.write('{:.activity}\n')
    activity.write('|<span class="activity_header">Flower</span>')
    activity.write('|<span class="activity_header activity_col1' + col1 + '">' + col1_link + 'Day' + col1_extra + '</span>')
    activity.write('|<span class="activity_header activity_col2' + col2 + '">' + col2_link + 'Week' + col2_extra + '</span>')
    activity.write('|<span class="activity_header activity_col3' + col3 + '">' + col3_link + 'Month' + col3_extra +'</span>|\n')
    flower_df = pd.DataFrame()
    for i in flower_dict.values():
        flower_df = pd.concat([flower_df, df_now.ix[df_now['tank_id'] == i['tank_id'], ['tank_name', 'tank_color', 'tank_awards_html', 'hours_day', 'hours_week', 'hours_month']]], axis = 0)    
    flower_df = flower_df.sort_values(sort_list, ascending = False)
    flower_df.reset_index(drop = True, inplace = True)
    for i in range(flower_df.shape[0]):
        write_activity_md_from_index(activity, flower_df, i, col1, col2, col3)
    activity.write('\n## LAST UPDATED\n\n')
    activity.write('<span class="last_updated">')
    activity.write(last_updated)
    activity.write('</span>')
    activity.close()

#----- Top 100

def get_tank_table_from_list(tank_id_list, no_param_url = 'https://tankpit.com/tank_profile/?tank_id='):
    master_tanks_df = pd.DataFrame()
    for tank_id in tank_id_list:
        # scrape
        tank_results_html = scrape_text_from_link(no_param_url + str(tank_id))
        # make tables
        tanks_df = create_tables_from_page_html(tank_results_html, tank_id)
        # concat
        master_tanks_df = pd.concat([master_tanks_df, tanks_df], axis = 0)
        master_tanks_df.reset_index(drop = True, inplace = True)
    return master_tanks_df[["tank_id", "tank_name", "tank_color", "tank_awards_html"]]

def write_t100_md_from_index(t100, df, i):
    t100.write('|' + str(i + 1))
    t100.write('|<span class="')
    t100.write(df.ix[i, 'tank_color'])
    t100.write('">')
    t100.write(df.ix[i, 'tank_name'])
    t100.write('</span><span class="awards-container">')
    t100.write(df.ix[i, 'tank_awards_html'])
    t100.write('</span>|\n')

def make_t100_md(t100_out_file, t100_df):
    t100 = open(t100_out_file, 'w')
    t100.write('\n## TRUE TOP 100\n\n')
    t100.write('{:.true-t100}\n')
    for i in range(t100_df.shape[0]):
        write_t100_md_from_index(t100, t100_df, i)
    t100.close()

#----- Main

if __name__ == "__main__":
    # run scraper, generate stats_now csv
    df_now = loop_all_flowers()
    df_now.to_csv('./data/flowers_stats_now.csv', sep = ',', header = True, index = False, quotechar = '"')
    # update daily csv
    flowers_stats_daily_filename = './data/flowers_stats_daily.csv'
    flowers_stats_daily = pd.read_csv(flowers_stats_daily_filename)
    flowers_stats_daily = pd.concat([flowers_stats_daily, df_now], axis = 0)
    flowers_stats_daily.to_csv(flowers_stats_daily_filename, sep = ',', header = True, index = False, quotechar = '"')
    # update hours log
    df_T_filename = './data/flowers_hours_log.csv'
    df_T = pd.read_csv(df_T_filename)
    df_T = concat_now_to_alltime_long(df_T, df_now)
    df_T = format_time_col(df_T)
    df_T = groupby_max_time(df_T)
    df_T.to_csv(df_T_filename, sep = ',', header = True, index = False, quotechar = '"')
    # create roster.md
    make_roster_md(roster_out_file = './index.md', df_now = df_now)
    # create stats.md
    make_stats_md(stats_out_file = './stats.md', df_now = df_now, sort_by = 'time_played_decimal', sort_list = ['time_played_decimal', 'kills_decimal', 'deactivated_decimal'])
    make_stats_md(stats_out_file = './stats-kills.md', df_now = df_now, sort_by = 'kills_decimal', sort_list = ['kills_decimal', 'time_played_decimal', 'deactivated_decimal'])
    make_stats_md(stats_out_file = './stats-deact.md', df_now = df_now, sort_by = 'deactivated_decimal', sort_list = ['deactivated_decimal', 'time_played_decimal', 'kills_decimal'])
    # sum day
    hours_day = subset_df_to_timeframe(df_T, days = 1)
    hours_day = get_diff_df(hours_day)
    hours_day = sum_diff(hours_day, diff_col_name = 'hours_day')
    df_now = df_now.merge(hours_day, how = 'left', on = 'tank_id')
    # sum week
    hours_week = subset_df_to_timeframe(df_T, days = 7)
    hours_week = get_diff_df(hours_week)
    hours_week = sum_diff(hours_week, diff_col_name = 'hours_week')
    df_now = df_now.merge(hours_week, how = 'left', on = 'tank_id')
    # sum month
    hours_month = subset_df_to_timeframe(df_T, days = 30)
    hours_month = get_diff_df(hours_month)
    hours_month = sum_diff(hours_month, diff_col_name = 'hours_month')
    df_now = df_now.merge(hours_month, how = 'left', on = 'tank_id')
    # create activity.md
    make_activity_md(activity_out_file = './activity.md', df_now = df_now, sort_by = 'hours_day', sort_list = ['hours_day', 'hours_week', 'hours_month'])
    make_activity_md(activity_out_file = './activity-week.md', df_now = df_now, sort_by = 'hours_week', sort_list = ['hours_week', 'hours_day', 'hours_month'])
    make_activity_md(activity_out_file = './activity-month.md', df_now = df_now, sort_by = 'hours_month', sort_list = ['hours_month', 'hours_day', 'hours_week'])
    # to 100
    t100_df = pd.read_csv('./data/top_100.csv')
    t100_df = get_tank_table_from_list( list(t100_df['id']) )
    make_t100_md(t100_out_file = './top-100.md', t100_df = t100_df)
