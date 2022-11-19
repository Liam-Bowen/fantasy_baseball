from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import pymysql
import csv

Base = declarative_base()


class Player(Base):
    __tablename__ = 'player'
    id = Column(String(256), primary_key=True)
    name = Column(String(256))
    team = Column(String(256))
    league = Column(String(256))
    games = Column(Integer)
    at_bats = Column(Integer)
    runs = Column(Integer)
    hits = Column(Integer)
    doubles = Column(Integer)
    triples = Column(Integer)
    home_runs = Column(Integer)
    rbis = Column(Integer)
    stolen = Column(Integer)
    caught = Column(Integer)
    walks = Column(Integer)
    strikeout = Column(Integer)
    hbp = Column(Integer)
    sf = Column(Integer)
    ibb = Column(Integer)
    available = Column(Boolean, nullable=False, default=True)


def blankIfNone(str):
    if str is not None:
        return str
    return ''


def combinePlayerEntries(entryList):
    player = Player()
    first = entryList[0]
    player.id = first['id']
    player.name = first['name']
    player.team = "|".join([entry['team'] for entry in entryList])
    player.league = "|".join([entry['league'] for entry in entryList])
    player.games = sum([entry['games'] for entry in entryList])
    player.runs = sum([entry['runs'] for entry in entryList])
    player.hits = sum([entry['hits'] for entry in entryList])
    player.doubles = sum([entry['doubles'] for entry in entryList])
    player.triples = sum([entry['triples'] for entry in entryList])
    player.home_runs = sum([entry['home_runs'] for entry in entryList])
    player.rbis = sum([entry['rbis'] for entry in entryList])
    player.stolen = sum([entry['stolen'] for entry in entryList])
    player.caught = sum([entry['caught'] for entry in entryList])
    player.walks = sum([entry['walks'] for entry in entryList])
    player.strikeout = sum([entry['strikeout'] for entry in entryList])
    player.hbp = sum([entry['hbp'] for entry in entryList])
    player.sf = sum([entry['sf'] for entry in entryList])
    player.ibb = sum([entry['ibb'] for entry in entryList])
    return player


def load_players(db_session, file_name='static/csv/updated-batters.csv'):
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        player_entries = {}
        line_cnt = 0
        for row in reader:
            if line_cnt == 0:
                # this is the names of the columns
                cols = list(row)
            else:
                entry = {"id": row[18], "name": row[0], "team": row[1], "league": row[2], "games": int(row[3]),
                         "at_bats": int(row[4]), "runs": int(row[5]), "hits": int(row[6]), "doubles": int(row[7]),
                         "triples": int(row[8]), "home_runs": int(row[9]), "rbis": int(row[10]),
                         "stolen": int(row[11]), "caught": int(row[12]), "walks": int(row[13]),
                         "strikeout": int(row[14]), "hbp": int(row[15]), "sf": int(row[16]), "ibb": int(row[17])}
                if entry['id'] not in player_entries:
                    player_entries[entry['id']] = []
                player_entries[entry['id']].append(entry)
            line_cnt += 1
        player_list = []
        for _, entryList in player_entries.items():
            player = combinePlayerEntries(entryList)
            player_list.append(player)
        db_session.add_all(player_list)
        db_session.commit()
        print('added players')


if __name__ == '__main__':
    engine = create_engine('mysql+pymysql://fantasy_baseball:password@localhost/fantasy_baseball')
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        load_players(session)
