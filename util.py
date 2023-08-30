from __future__ import annotations
import socket


def recieve(conn: socket.socket):
    return conn.recv(1000)


def send(conn: socket.socket, payload: str | int):
    conn.send(bytes(str(payload), encoding="ascii"))
