This SSL honeypot is a decoy server that mimics vulnerable SSL/TLS services, e.g., expired certificates and weak cipher suites, to attract attackers and collect telemetry. By doing so, defenders can observe the attackers' behavior in a controlled environment. The goal is to capture tactics, tools, and payloads used by the attackers. 


Launched in a DMZ or a VLAN. 

Uses KVM to turn a Linux machine into a hypervisor. 

Motherboard must support Intel VT or AMD-V.

Use iptables or ufw to block all in-bound and out-bound traffic to all ports apart from ports 443, 25, 587. 

### HTTPS Web Service
`pt install nginx openssl`

`openssl req -x509 -nodes -days 1 -subj "/CN=old-webserver" -newkey rsa:2048 -keyout /etc/nginx/ssl/honey.key -out /etc/nginx/ssl/honey.crt`

To enable legacy TLS version and weak ciphers open `/etc/nginx/sites-enabled/default`

`openssl s_client -connect <IP>:443 -tls1`

`nmap --script ssl-enum-ciphers -p443 <IP>`






### STARTTLS-enabled SMTP and IMAP

Use Postfix for SMTP.

Edit `/etc/postfix/main.cf`

`/etc/ssl/certs/honeypot.crt`

`/etc/ssl/private/honeypot.key`





Use Dovecot for IMAP.

`/etc/dovecot/conf.d/10-ssl.conf`






