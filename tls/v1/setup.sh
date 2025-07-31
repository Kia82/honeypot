sudo apt install openssl build-essential pkg-config libssl-dev 

openssl req -x509 -newkey rsa:4096 -sha256 -nodes -days 365 -keyout server.key -out server.crt -subj "/CN=localhost" 

gcc -Wall -Wextra -o server_tls server_tls.c -lssl -lcrypto 

gcc -Wall -Wextra -o client_tls client_tls.c -lssl -lcrypto 


