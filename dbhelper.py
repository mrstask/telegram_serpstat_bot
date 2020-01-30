import json
import os
from sqlalchemy import Column, Integer, ForeignKey, MetaData, create_engine, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker, relationship
from settings import serpstat_popular_regions, PostgresConfig, develop


db_uri = PostgresConfig().postgres_db_path if develop else os.environ['DATABASE_URL']
engine = create_engine(db_uri)

meta = MetaData(engine)
Base = declarative_base()


association_table = Table('association', Base.metadata,
                          Column('user_id', Integer, ForeignKey('users.user_id')),
                          Column('r_id', Integer, ForeignKey('regions.r_id')))


class UserTable(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    api_key = Column(Integer, ForeignKey('keys.key_id'))
    regions = relationship('RegionTable', secondary=association_table, backref="users")


class RegionTable(Base):
    __tablename__ = 'regions'

    r_id = Column(Integer, primary_key=True)
    region_name = Column(String)
    region_code = Column(String)
    # users = relationship('UserTable', secondary=association_table, back_populates="regions")


class KeyTable(Base):
    __tablename__ = 'keys'

    key_id = Column(Integer, primary_key=True, autoincrement=True)
    children = relationship("UserTable")
    key = Column(String)


class PgHelper:
    def __init__(self, db_string):
        self.engine = create_engine(db_string)
        self.session = sessionmaker(bind=self.engine)
        self.session = self.session()

    def add_user(self, user_id: int) -> int:
        user_table = UserTable(**{'user_id': user_id})
        self.session.add(user_table)
        self.session.commit()
        return user_table.user_id

    def get_user(self, user_id: int):
        try:
            result = self.session.query(UserTable).filter_by(user_id=user_id).one()
            regions = [r.region_code for r in result.regions]
            return {'user_id': result.user_id, 'api_key': result.api_key, 'regions': regions}
        except NoResultFound:
            return None

    def get_user_key(self, user_id: int):
        try:
            result = self.session.query(KeyTable).join(UserTable).filter(UserTable.user_id == user_id).one()
            return {'api_key': result.key}
        except NoResultFound:
            return None

    def update_user_key(self, user_id: int, key_id: int):
        try:
            self.session.query(UserTable).filter_by(user_id=user_id).update({'api_key': key_id})
            self.session.commit()
        except Exception as e:
            raise (e, 'update_user_key')

    def add_key(self, key: str) -> int:
        key_table = KeyTable(**{'key': key})
        self.session.add(key_table)
        self.session.commit()
        return key_table.key_id

    def get_key_by_id(self, key_id: int):
        try:
            result = self.session.query(KeyTable).filter_by(key_id=key_id).one()
            return {'key_id': result.key_id, 'api_key': result.key}
        except NoResultFound:
            return None

    def get_key_by_value(self, key: str):
        try:
            result = self.session.query(KeyTable).filter_by(key=key).one()
            return {'key_id': result.key_id, 'api_key': result.key}
        except NoResultFound:
            return None

    def update_key(self, key_id: int, key: str):
        try:
            self.session.query(KeyTable).filter_by(key_id=key_id).update({'key': key})
            self.session.commit()
        except Exception as e:
            raise (e, 'update_user_key')

    def add_region_to_user(self, user_id: int, region_code: str):
        try:
            user = self.session.query(UserTable).filter_by(user_id=user_id).one()
            region = self.session.query(RegionTable).filter_by(region_code=region_code).one()
            user.regions.append(region)
            self.session.commit()
            return user.regions
        except NoResultFound:
            return None

    def add_region(self, region_code: str, region_name: str) -> int:
        region_table = RegionTable(**{'region_code': region_code, 'region_name': region_name})
        self.session.add(region_table)
        self.session.commit()
        return region_table.r_id

    def get_region_name(self, region_code: str) -> str:
        region = self.session.query(RegionTable).filter_by(region_code=region_code).one()
        return region.region_name


postgres_handler = PgHelper(db_uri)


def populate_regions():
    with open('serpstat_regions.json', 'r') as f:
        regions = json.load(f)
    for region in regions['regions']:
        if region['db_name'] in serpstat_popular_regions:
            postgres_handler.add_region(region['db_name'], region['country_name_en'])


def create_tables():
    Base.metadata.create_all(engine, checkfirst=True)


if __name__ == '__main__':
    Base.metadata.create_all(engine, checkfirst=True)
    populate_regions()
    # Base.metadata.drop_all(engine)
