import re
import unicodedata
import pandas as pd
import requests as r
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time

# get time now
last_updated_raw = datetime.now() - timedelta(hours = 4)
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
    'GLADIOLUS': {'tank_id': 48059,
                  'section': 0,
                  'seq': 2,
                  'main_tank_id': 4462,
                  'main_tank': None,
                  'main_color': None,
                  'main_awards_html': None},
    'TULIP': {'tank_id': 45920,
              'section': 0,
              'seq': 3,
              'main_tank_id': None,
              'main_tank': 'SSpritEE',
              'main_color': 'red',
              'main_awards_html': '<span class="awards-sprite a0-3"></span><span class="awards-sprite a3-1"></span><span class="awards-sprite a5-3"></span>'},
    'HIBISCUS': {'tank_id': 45859,
                 'section': 0,
                 'seq': 4,
                 'main_tank_id': 850,
                 'main_tank': None,
                 'main_color': None,
                 'main_awards_html': None},
    'DAHLIA': {'tank_id': 48641,
               'section': 0,
               'seq': 5,
               'main_tank_id': 10502,
                 'main_tank': None,
                 'main_color': None,
                 'main_awards_html': None},
    'DAISY': {'tank_id': 48103,
              'section': 0,
              'seq': 6,
              'main_tank_id': 6281,
              'main_tank': None,
              'main_color': None,
              'main_awards_html': None},
    'BUTTERCUP': {'tank_id': 48264,
                  'section': 0,
                  'seq': 7,
                  'main_tank_id': 575,
                  'main_tank': None,
                  'main_color': None,
                  'main_awards_html': None},
    'HYDRANGEA': {'tank_id': 49521,
                  'section': 0,
                  'seq': 8,
                  'main_tank_id': None,
                  'main_tank': 'Secret',
                  'main_color': 'gray',
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
    'terrestrial TULIP': {'tank_id': 48240,
                          'section': 1,
                          'seq': 3,
                          'main_tank_id': 45920,
                          'main_tank': None,
                          'main_color': None,
                          'main_awards_html': None},
    'radiant ROSE': {'tank_id': 48222,
                     'section': 1,
                     'seq': 4,
                     'main_tank_id': 45863,
                     'main_tank': None,
                     'main_color': None,
                     'main_awards_html': None}
}

#----- Scraper functions

def scrape_text_from_link(link):
    trials = 0
    print link
    try:
        response = r.get(link)
    except:
        time.sleep(5)
        trials += 1
        if trials < 10:
            scrape_text_from_link(link)
    return BeautifulSoup(response.text)

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

def make_roster_md(roster_out_file, master_tanks_df, flower_dict = flower_dict, last_updated = last_updated):
    roster = open(roster_out_file, 'w')
    roster.write('{:.roster}\n')
    # main flowers
    for j in range(len(flower_dict)):
        for i in flower_dict.values():
            if i['seq'] == j and i['section'] == 0:
                write_md_from_tank_id(roster, master_tanks_df, tank_id = i['tank_id'], end = 'no')
                if i['main_tank_id'] != None:
                    write_md_from_tank_id(roster, master_tanks_df, tank_id = i['main_tank_id'])
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
    for j in range(len(flower_dict)):
        for i in flower_dict.values():
            if i['seq'] == j and i['section'] == 1:
                write_md_from_tank_id(roster, master_tanks_df, tank_id = i['tank_id'], end = 'no')
                write_md_from_tank_id(roster, master_tanks_df, tank_id = i['main_tank_id'], end = 'yes')
    roster.write('\n## LAST UPDATED\n\n')
    roster.write('<span class="last_updated">')
    roster.write(last_updated)
    roster.write('</span>')
    roster.close()

#----- Stats functions

def write_stats_md_from_index(stats, df, i):
    stats.write('|<span class="')
    stats.write(df.ix[i, 'tank_color'])
    stats.write('">')
    stats.write(df.ix[i, 'tank_name'])
    stats.write('</span><span class="awards-container">')
    stats.write(df.ix[i, 'tank_awards_html'])
    stats.write('</span>|<span class="stat stat_hours stat_sorted">')
    stats.write(df.ix[i, 'time_played'])
    stats.write('</span>|<span class="stat stat_kills">')
    stats.write(df.ix[i, 'kills'])
    stats.write('</span>|<span class="stat stat_deactivated">')
    stats.write(df.ix[i, 'deactivated'])
    stats.write('</span>|\n')

def make_stats_md(stats_out_file, master_tanks_df, flower_dict = flower_dict, last_updated = last_updated):
    stats = open(stats_out_file, 'w')
    stats.write('{:.stats}\n')
    stats.write('|<span class="stat_header">Flower</span>')
    stats.write('|<span class="stat_header stat_hours stat_sorted">Hours &nbsp;&darr;</span>')
    stats.write('|<span class="stat_header stat_kills">Kills</span>')
    stats.write('|<span class="stat_header stat_deactivated">Deact.</span>|\n')
    flower_df = pd.DataFrame()
    for i in flower_dict.values():
        flower_df = pd.concat([flower_df, master_tanks_df.ix[master_tanks_df['tank_id'] == i['tank_id'], ['tank_name', 'tank_color', 'tank_awards_html', 'time_played', 'time_played_decimal', 'kills', 'deactivated']]], axis = 0)    
        flower_df = flower_df.sort_values('time_played_decimal', ascending = False)
        flower_df.reset_index(drop = True, inplace = True)
    for i in range(flower_df.shape[0]):
        write_stats_md_from_index(stats, flower_df, i)
    stats.write('\n## LAST UPDATED\n\n')
    stats.write('<span class="last_updated">')
    stats.write(last_updated)
    stats.write('</span>')
    stats.close()

#----- Main

if __name__ == "__main__":
    # run scraper, generate current csv
    master_tanks_df = loop_all_flowers()
    master_tanks_df.to_csv('./data/flowers_stats_now.csv', sep = ',', header = True, index = False, quotechar = '"')
    # update alltime csv
    flowers_stats_alltime_filename = './data/flowers_stats_alltime.csv'
    flowers_stats_alltime = pd.read_csv(flowers_stats_alltime_filename)
    flowers_stats_alltime = pd.concat([flowers_stats_alltime, master_tanks_df], axis = 0)
    flowers_stats_alltime.to_csv(flowers_stats_alltime_filename, sep = ',', header = True, index = False, quotechar = '"')
    # create roster.md
    make_roster_md(roster_out_file = './index.md', master_tanks_df = master_tanks_df)
    # create stats.md
    make_stats_md(stats_out_file = './stats.md', master_tanks_df = master_tanks_df)
