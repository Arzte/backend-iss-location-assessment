#!/usr/bin/env python

import requests
import turtle
import time

__author__ = 'Iris Hofffmeyer'


def get_list_of_astronauts():
    """Return a list of of astronauts in space,
    as well as the total number of astronauts"""
    request = requests.get("http://api.open-notify.org/astros.json")
    astronaut_json = request.json()
    astronauts_in_space = astronaut_json['number']
    return astronaut_json['people'], astronauts_in_space


def get_current_location_of_space_station():
    """Return the geographic location of the space station,
    with the timestamp of that location"""
    request = requests.get("http://api.open-notify.org/iss-now.json")
    station = request.json()
    iss_position_tuple = (float(station['iss_position']['latitude']),
                          float(station['iss_position']['longitude']))
    return iss_position_tuple, station['timestamp']


def get_indianapolis_pass_times():
    request = requests.get("http://api.open-notify.org/iss-pass.json",
                           params={"lat": 39.7683333,
                                   "lon": -86.1580556,
                                   "n": 1})
    return request.json()['response'][0]['risetime']


def setup_screen():
    screen = turtle.Screen()
    screen.setup(width=720, height=360)
    screen.bgpic("map.gif")
    screen.setworldcoordinates(-180, -90, 180, 90)
    return screen


def create_city(timestamp):
    city = turtle.Turtle()
    city.penup()
    city.goto(-86.1580556, 39.7683333)
    city.pendown()
    city.color('yellow')
    city.write(time.ctime(timestamp), align="left")
    city.dot(5, "yellow")
    return city


def create_turle(iss_position, iss):
    turtle.register_shape("iss.gif")
    iss.shape("iss.gif")
    iss.penup()
    iss.goto(iss_position)
    iss.pendown()
    return iss


def update_iss(iss, screen):
    iss_location, _ = get_current_location_of_space_station()
    iss.penup()
    iss.goto(iss_location)
    iss.pendown()
    screen.ontimer(update_iss(iss, screen), 5000)


def main():
    list_of_astronauts, number_of_people_in_space = get_list_of_astronauts()
    iss_location, _ = get_current_location_of_space_station()
    passtime = get_indianapolis_pass_times()
    for astronaut in list_of_astronauts:
        print(f"{astronaut['name']} on board the {astronaut['craft']}")
    print(f"Total number of astronauts in space: {number_of_people_in_space}")

    screen = setup_screen()
    turt = create_city(passtime)
    iss = create_turle(iss_location, turt)
    turtle.exitonclick()
    update_iss(iss, screen)
    turtle.done()


if __name__ == '__main__':
    main()
