#!/usr/bin/env python3

import statistics
import struct
import threading
import time
import traceback

from dsf.commands.basecommands import HttpEndpointType
from dsf.http import HttpEndpointConnection
from dsf.connections import CommandConnection

import smbus

BOWDEN_WASTE = 10.0
SPOOL_WEIGHT = 230.0
AVERAGING_WINDOW = 10
I2C_ADDRESS = 0x08

load_cell_weight = 0.0


def load_cell_monitor():
    print("Load Cell Monitor started.")

    global load_cell_weight

    while True:
        try:
            bus = smbus.SMBus(1)
            readings = []
            while True:
                data = bus.read_i2c_block_data(I2C_ADDRESS, 4)
                readings.append(struct.unpack("<f", bytes(data[:4]))[0])
                load_cell_weight = statistics.mean(readings)
                readings = readings[:AVERAGING_WINDOW]
                time.sleep(3)
        except:
            print("I2C read failed - resetting...")
            time.sleep(5)


async def respond_filament_load_cell(http_endpoint_connection: HttpEndpointConnection):
    global load_cell_weight

    await http_endpoint_connection.read_request()

    body = "approx. {:.0f}g filament left".format(
        load_cell_weight - SPOOL_WEIGHT - BOWDEN_WASTE,
    )
    await http_endpoint_connection.send_response(200, body)
    http_endpoint_connection.close()


def add_dsf_http_endpoint():
    while True:
        try:
            print("command connection started.")

            cmd_connection = CommandConnection()
            cmd_connection.connect()
            print("command connection connected.")

            endpoint = None
            endpoint = cmd_connection.add_http_endpoint(
                HttpEndpointType.GET, "filament-load-cell", "reading"
            )
            endpoint.set_endpoint_handler(respond_filament_load_cell)
            print("HTTP endpoint added:", endpoint.endpoint_path)
            return
        except Exception as e:
            print("Closing connection: ", e)
            traceback.print_exc()
            cmd_connection.close()
            if endpoint:
                endpoint.close()
        time.sleep(1)


if __name__ == "__main__":
    time.sleep(5)  # let everything boot and connect
    threading.Thread(target=load_cell_monitor).start()
    add_dsf_http_endpoint()
