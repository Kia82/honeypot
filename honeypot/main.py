from .services.http_service.http_service import http_main
from .services.ssh.ssh import ssh_main
import threading

if __name__ == "__main__":
    http_thread = threading.Thread(target=http_main)
    ssh_thread = threading.Thread(target=ssh_main)


    http_thread.start()
    ssh_thread.start()