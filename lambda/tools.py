import socket

def get_ip(url: str):
  # url: www.google.com
  socket.gethostbyname(url)
