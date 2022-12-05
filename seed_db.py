from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Boolean, Float
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import pymysql
import csv

Base = declarative_base()


class Batters(Base):
    __tablename__ = 'batters'
    id = Column(String(256), primary_key=True)
    name = Column(String(256))
    tm = Column(String(256))
    lg = Column(String(256))
    g = Column(Integer)
    ab = Column(Integer)
    r = Column(Integer)
    h = Column(Integer)
    db = Column(Integer)
    tp = Column(Integer)
    hr = Column(Integer)
    rbi = Column(Integer)
    sb = Column(Integer)
    cs = Column(Integer)
    bb = Column(Integer)
    so = Column(Integer)
    hbp = Column(Integer)
    sf = Column(Integer)
    ibb = Column(Integer)
    available = Column(Boolean, nullable=False, default=True)


class Pitchers(Base):
    __tablename__ = 'pitchers'
    id = Column(String(256), primary_key=True)
    name = Column(String(256))
    tm = Column(String(256))
    lg = Column(String(256))
    w = Column(Integer)
    l = Column(Integer)
    g = Column(Integer)
    cg = Column(Integer)
    sho = Column(Integer)
    sv = Column(Integer)
    ip = Column(Float)
    h = Column(Integer)
    er = Column(Integer)
    hr = Column(Integer)
    bb = Column(Integer)
    ibb = Column(Integer)
    so = Column(Integer)
    hbp = Column(Integer)
    available = Column(Boolean, nullable=False, default=True)


def blankIfNone(str):
    if str is not None:
        return str
    return ''


def combineBatterEntries(entryList):
    player = Batters()
    first = entryList[0]
    player.id = first['id']
    player.name = first['name']
    player.tm = "|".join([entry['tm'] for entry in entryList])
    player.lg = "|".join([entry['lg'] for entry in entryList])
    player.g = sum([entry['g'] for entry in entryList])
    player.ab = sum([entry['ab'] for entry in entryList])
    player.r = sum([entry['r'] for entry in entryList])
    player.h = sum([entry['h'] for entry in entryList])
    player.db = sum([entry['db'] for entry in entryList])
    player.tp = sum([entry['tp'] for entry in entryList])
    player.hr = sum([entry['hr'] for entry in entryList])
    player.rbi = sum([entry['rbi'] for entry in entryList])
    player.sb = sum([entry['sb'] for entry in entryList])
    player.cs = sum([entry['cs'] for entry in entryList])
    player.bb = sum([entry['bb'] for entry in entryList])
    player.so = sum([entry['so'] for entry in entryList])
    player.hbp = sum([entry['hbp'] for entry in entryList])
    player.sf = sum([entry['sf'] for entry in entryList])
    player.ibb = sum([entry['ibb'] for entry in entryList])
    return player


def combinePitcherEntries(entryList):
    player = Pitchers()
    first = entryList[0]
    player.id = first['id']
    player.name = first['name']
    player.tm = "|".join([entry['tm'] for entry in entryList])
    player.lg = "|".join([entry['lg'] for entry in entryList])
    player.w = sum([entry['w'] for entry in entryList])
    player.l = sum([entry['l'] for entry in entryList])
    player.g = sum([entry['g'] for entry in entryList])
    player.cg = sum([entry['cg'] for entry in entryList])
    player.sho = sum([entry['sho'] for entry in entryList])
    player.sv = sum([entry['sv'] for entry in entryList])
    player.ip = sum([entry['ip'] for entry in entryList])
    player.h = sum([entry['h'] for entry in entryList])
    player.er = sum([entry['er'] for entry in entryList])
    player.hr = sum([entry['hr'] for entry in entryList])
    player.bb = sum([entry['bb'] for entry in entryList])
    player.ibb = sum([entry['ibb'] for entry in entryList])
    player.so = sum([entry['so'] for entry in entryList])
    player.hbp = sum([entry['hbp'] for entry in entryList])
    return player


def load_batters(db_session, file_name='static/csv/updated-batters.csv'):
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        player_entries = {}
        line_cnt = 0
        for row in reader:
            if line_cnt == 0:
                # this is the names of the columns
                cols = list(row)
            else:
                entry = {"id": row[18], "name": row[0], "tm": row[1], "lg": row[2], "g": int(row[3]),
                         "ab": int(row[4]), "r": int(row[5]), "h": int(row[6]), "db": int(row[7]),
                         "tp": int(row[8]), "hr": int(row[9]), "rbi": int(row[10]),
                         "sb": int(row[11]), "cs": int(row[12]), "bb": int(row[13]),
                         "so": int(row[14]), "hbp": int(row[15]), "sf": int(row[16]), "ibb": int(row[17])}
                if entry['id'] not in player_entries:
                    player_entries[entry['id']] = []
                player_entries[entry['id']].append(entry)
            line_cnt += 1
        player_list = []
        for _, entryList in player_entries.items():
            player = combineBatterEntries(entryList)
            player_list.append(player)
        db_session.add_all(player_list)
        db_session.commit()
        print('added batters')


def load_pitchers(db_session, file_name='static/csv/updated-pitchers.csv'):
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        player_entries = {}
        line_cnt = 0
        for row in reader:
            if line_cnt == 0:
                # this is the names of the columns
                cols = list(row)
            else:
                entry = {"id": row[17], "name": row[0], "tm": row[1], "lg": row[2], "w": int(row[3]),
                         "l": int(row[4]), "g": int(row[5]), "cg": int(row[6]), "sho": int(row[7]),
                         "sv": int(row[8]), "ip": float(row[9]), "h": int(row[10]),
                         "er": int(row[11]), "hr": int(row[12]), "bb": int(row[13]),
                         "ibb": int(row[14]), "so": int(row[15]), "hbp": int(row[16])}
                if entry['id'] not in player_entries:
                    player_entries[entry['id']] = []
                player_entries[entry['id']].append(entry)
            line_cnt += 1
        player_list = []
        for _, entryList in player_entries.items():
            player = combinePitcherEntries(entryList)
            player_list.append(player)
        db_session.add_all(player_list)
        db_session.commit()
        print('added pitchers')


if __name__ == '__main__':
    engine = create_engine('mysql+pymysql://fantasy_baseball:password@localhost/fantasy_baseball')
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        load_batters(session)
        #load_pitchers(session)
