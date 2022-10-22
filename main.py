import socket
import pyfiglet
from datetime import datetime
import time
import sys
import typer
from rich.progress import track
from typing import Optional


app = typer.Typer()

banner = pyfiglet.figlet_format("Port Scanner")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def check_port(hostname, port):
    socket.setdefaulttimeout(1)
    result = sock.connect_ex((hostname, port))
    if result == 0:
        return True


def specified_port(hostname, port):
    try:
        if check_port(hostname, port):
            print("Port {} is open".format(port))
        sock.close()
    except socket.gaierror:
        print("[!]Hostname could not be resolved")
        sys.exit()
    except socket.error:
        print("[!]Couldn't connect to server")
        sys.exit()


def print_banner(banner, hostname):
    print(banner)
    print("-" * 50)
    print("Scanning Target: " + hostname)
    print("Scanning started at: " + str(datetime.now().strftime("%H:%M:%S, %d/%m/%Y")))
    print("-" * 50)


@app.command()
def scan_ports(hostname: str, port: Optional[int] = 0):
    print_banner(banner, hostname)
    if port != 0:
        for _ in track(range(100), description="Processing..."):
            time.sleep(0.01)
        if specified_port(hostname, port):
            print(f"Port {port} is open")
        else:
            print(f"Port {port} is closed")
    else:
        for value in track(range(1, 65535), description="Processing..."):
            time.sleep(0.01)
            specified_port(hostname, value)
        print("Processed 65535 ports in total")


@app.command()
def ping(hostname: str):
    print_banner(banner, hostname)
    try:
        print(f"Pinging {hostname}")
        for _ in track(range(100), description="Processing..."):
            time.sleep(0.01)
        host = socket.gethostbyname(hostname)
        print(f"Host {hostname} is up")
    except socket.gaierror:
        print("Host is down")

    
if __name__ == "__main__":
    app()
    
    
