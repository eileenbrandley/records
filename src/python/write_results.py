import numpy as np
import datetime

from src.flask import sqlite as sq

SPRINT_DISTANCES = ['100', '200', '300', '400', '400HW', '100HW', '400HM', '110HM']
FIELD_EVENTS = ['HJ', 'TJ', 'LJ', 'Hep', 'Dec', 'JT', 'HT', 'SP', 'DT']

def get_race_time(row):
    time = row['Perf'] if row['Unnamed: 5'] is np.nan else row['Unnamed: 5']
    if row['Event'] in SPRINT_DISTANCES:
        return parse_sprint_time(time)
    else:
        return parse_race_time(time)


def parse_sprint_time(time):
    return float(time)


def get_race_position(row):
    return row['Pos'] if np.isnan(row['Unnamed: 8']) else row['Unnamed: 8']


def parse_race_time(time_str):
    split_time = [float(t) for t in time_str.split(':')]
    if len(split_time) > 2:
        if split_time[0] > 9:
            m, s, _ = split_time
            h = 0
        else:
            h, m, s = split_time
    else:
        h, m, s = [0] + split_time
    return h * 60 * 60 + m * 60 + s


def parse_race_date(date_input):
    s = datetime.datetime.strptime(date_input, '%d %b %y')
    return s.timestamp()


def get_athlete_id(name, db):
    query = f"SELECT id FROM athletes WHERE name = \"{name}\""
    return sq.fetch_data(query, db)[1][0]


def get_event_id(event, db):
    query = f"SELECT id FROM events WHERE name = \"{event}\""
    event_data = sq.fetch_data(query, db)
    if len(event_data) == 1:
        sq.execute_statement(f"INSERT INTO events (name) values (\"{event}\")", db)
        event_data = sq.fetch_data(query, db)
    return event_data[1][0]


def get_venue_id(venue, db):
    query = f"SELECT id FROM venues WHERE name = \"{venue}\""
    venue_data = sq.fetch_data(query, db)
    if len(venue_data) == 1:
        sq.execute_statement(f"INSERT INTO venues (name) values (\"{venue}\")", db)
        venue_data = sq.fetch_data(query, db)
    return venue_data[1][0]


def get_meeting_id(meeting, date, db):
    query = f"SELECT id FROM meetings WHERE name = \"{meeting}\" AND date = \"{date}\""
    meeting_data = sq.fetch_data(query, db)
    if len(meeting_data) == 1:
        sq.execute_statement(f"INSERT INTO meetings (name, date) values (\"{meeting}\", \"{date}\")", db)
        meeting_data = sq.fetch_data(query, db)
    return meeting_data[1][0]


def set_race_result(athlete_id, event_id, meeting_id, venue_id, time, position, db):
    if position is None:
        query = f"""
        INSERT INTO results (athlete_id, event_id, meeting_id, venue_id, time) 
        values ({athlete_id}, {event_id}, {meeting_id}, {venue_id}, {time})"""
    else:
        query = f"""
        INSERT INTO results (athlete_id, event_id, meeting_id, venue_id, time, position) 
        values ({athlete_id}, {event_id}, {meeting_id}, {venue_id}, {time}, {position})"""
    sq.execute_statement(query, db)

def set_dataframe_row(row, db):
    pos = None if np.isnan(get_race_position(row)) or get_race_position(row) == 0 else get_race_position(row)
    t = get_race_time(row)
    date = parse_race_date(row['Date'])

    athlete_id = get_athlete_id(name=row['Name'], db=db)
    meeting_id = get_meeting_id(meeting=row['Meeting'], date=date, db=db)
    event_id = get_event_id(event=row['Event'], db=db)
    venue_id = get_venue_id(venue=row['Venue'], db=db)
    set_race_result(athlete_id, event_id, meeting_id, venue_id, t, pos, db)

def set_results_from_dataframe(df, db):
    not_saved = []
    for i, row in df.iterrows():
        if True in [i in row['Event'] for i in FIELD_EVENTS]: # This seems inefficient and should be rewritten
            print(f"Field event, row {i} ignored")
        else:
            try:
                set_dataframe_row(row, db)
            except:
                not_saved.append(i)
    return not_saved
