#!/usr/bin/python3
from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
import datetime

# parses wget http://burlingame.results.gokartracer.com/gkrburlingame/SpeedLimit.aspx

def allRacerHistoryFiles():
  return [ path for path in listdir('.') if 'RacerHistory' in path ]

def parseDate(fulldate):
  date, hourmin, pam = fulldate.split(' ')
  hours, minutes = hourmin.split(':')
  month, day, year = date.split('/')
  h = int(hours)
  if pam == "PM":
    h += 12
  return datetime.datetime(int(year), int(month), int(day), h,
                           int(minutes))

def parseRaceKart(racekart):
  if 'Monza' in racekart:
    race = 'monza'
  elif 'Yoko' in racekart:
    race = 'yoko'
  elif 'Super' in racekart:
    race = 'super'
  else:
    print("unknown race", racekart)
  kart = int(racekart.split(' ')[-1])
  return race, kart

def parseRacerFile(path):
  tracks = {'Monza': {}, 'Yokohama': {}}
  with open(path) as f:
    soup = BeautifulSoup(f.read())
    baseel = soup.find('body').find('form').find('table').find('table')
    all_links = baseel.find_all('a')
    for link in all_links:
      race, kart = parseRaceKart(link.string)
      timestamp = parseDate(link.parent.next_sibling.string.strip())

      print(timestamp, race, kart)


def compileStats():
  parseRacerFile(allRacerHistoryFiles()[0])


compileStats()
