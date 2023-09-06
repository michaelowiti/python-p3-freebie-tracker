from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    freebies = relationship('Freebie', back_populates='company')
    devs = relationship('Dev', secondary='freebies', back_populates='companies')

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    freebies = relationship('Freebie', back_populates='dev')
    companies = relationship('Company', secondary='freebies', back_populates='devs')

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())

    dev_id = Column(Integer(), ForeignKey('devs.id'))
    dev = relationship('Dev', back_populates='freebies')

    company_id = Column(Integer(), ForeignKey('companies.id'))
    company = relationship('Company', back_populates='freebies')

    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"

    @classmethod
    def give_away(cls, dev, freebie):
        if freebie.dev == dev:
            freebie.dev = None

    @classmethod
    def received_one(cls, item_name):
        return cls.query.filter_by(item_name=item_name).first() is not None

    @classmethod
    def create_freebie(cls, dev, company, item_name, value):
        freebie = cls(dev=dev, company=company, item_name=item_name, value=value)
        # session.add(freebie)
        # session.commit()

    @classmethod
    def oldest_company(cls):
        return Company.query.order_by(Company.founding_year).first()