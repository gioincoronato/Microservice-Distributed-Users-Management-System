import stomp
from time import sleep

if __name__ == "__main__":
    print("testing stomp")
    dest_send = "/queue/notifyservice"
    msg = "test"
    conn = stomp.Connection([("localhost", 61613)], auto_content_length= False)
    conn.connect(wait= True)
    conn.send(destination= dest_send, body= msg)
    sleep(1)
    print("message sended")
    conn.disconnect()

    