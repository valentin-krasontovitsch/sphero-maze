from spherov2 import scanner
from spherov2.sphero_edu import EventType, SpheroEduAPI
from spherov2.commands.sensor import (
    CollisionDetectionMethods,
    Sensor,
    SensitivityBasedCollisionDetectionMethods,
    SensitivityLevels,
)
from spherov2.types import Color
import sys
import time


SPEED = 100


def say_hello(sphero, name):
    msg = "Hello! My name is {}. I can do a lot of cool stuff! I can say Hello"
    print(msg.format(name))

    for c in "Hello":
        sphero.set_matrix_character(c, Color(255, 0, 0))
        time.sleep(0.2)

    sphero.clear_matrix()


def point_north(sphero):
    print("If you calibrate my compass I can tell you which direction is north")
    sphero.calibrate_compass()
    sphero.set_compass_direction(0)
    color = Color(0, 255, 0)

    for _ in range(3):
        time.sleep(0.2)
        sphero.set_matrix_line(3, 0, 3, 7, color)
        sphero.set_matrix_line(4, 0, 4, 7, color)
        sphero.set_matrix_pixel(2, 6, color)
        sphero.set_matrix_pixel(5, 6, color)
        time.sleep(0.3)
        sphero.clear_matrix()


def roll_distance(sphero, distance_cm):
    start = sphero.get_distance()
    sphero.set_speed(SPEED)

    while True:
        rolled_cm = sphero.get_distance() - start
        if rolled_cm > distance_cm:
            sphero.set_speed(0)
            break


def roll(sphero, distance_cm):
    start = sphero.get_distance()
    sphero.set_speed(SPEED)

    while True:
        time.sleep(0.1)
        print(f"accel: {sphero.get_acceleration()}")
        rolled_cm = sphero.get_distance() - start
        if rolled_cm > distance_cm:
            sphero.set_speed(0)
            break


def sensors(sphero):
    location = sphero.get_location()
    msg = (
        "I can tel you my location relative to the start of "
        "the program: x: {x}, y: {y}"
    )
    print(msg.format(**location))
    print("But I spin a lot so it is not very accurate")


def measure_light(sphero):
    while True:
        try:
            lum = sphero.get_luminosity()
            print(f"measured luminosity of {lum}")
        except KeyboardInterrupt:
            break


def roll_until_dark(sphero):
    start = sphero.get_distance()
    sphero.set_speed(SPEED)
    while True:
        lum = sphero.get_luminosity()
        print(f"{lum=}")
        if lum["ambient_light"] < 150:
            sphero.set_speed(0)
            break
    rolled_cm = sphero.get_distance() - start
    print(f"{rolled_cm=}")


def on_collision(api):
    api.stop_roll()
    print("Collision")


def roll_until_wall(sphero):
    sphero.set_speed(SPEED)
    z_values = []
    while True:
        try:
            time.sleep(0.1)
            accel = sphero.get_acceleration()
            x = accel["x"]
            y = accel["y"]
            z = accel["z"]
            z_values.append(z)
            print(accel)
            continue
            if accel["x"] < 0:
                print("collliisssion!!!")
                sphero.set_speed(0)
                break
        except KeyboardInterrupt:
            print(z_values)
            break


def mapper(sphero):
    while True:
        roll_until_dark(sphero)
        sphero.spin(90, 1)  # with clock
        roll_distance(sphero, 10)


def main():
    name = sys.argv[-1]
    toy = scanner.find_toy(toy_name=name)
    with SpheroEduAPI(toy) as sphero:
        # from spherov2.utils import ToyUtil

        # ToyUtil.configure_collision_detection(toy)

        # sphero.register_event(EventType.on_collision, on_collision)
        # say_hello(sphero, name)
        # point_north(sphero)
        # roll(sphero, 100)
        # sensors(sphero)
        # measure_light(sphero)
        # roll_until_dark(sphero)
        roll_until_wall(sphero)


if __name__ == "__main__":
    main()
