// Simple TLS echo server using OpenSSL 1.1+ / 3.x
// Compile with: gcc -Wall -Wextra -o tls_server tls_server.c -lssl -lcrypto

#define _POSIX_C_SOURCE 200809L
#include <arpa/inet.h>
#include <errno.h>
#include <netinet/in.h>
#include <openssl/err.h>
#include <openssl/ssl.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define LISTEN_PORT 4443
#define CERT_FILE   "server.crt"
#define KEY_FILE    "server.key"
#define BACKLOG     10
#define BUF_SIZE    4096

static volatile sig_atomic_t keep_running = 1;
static void sigint_handler(int signo) { (void)signo; keep_running = 0; }

static int create_listen_socket(void) {
    int s = socket(AF_INET, SOCK_STREAM, 0);
    if (s < 0) { perror("socket"); exit(EXIT_FAILURE); }

    int opt = 1;
    setsockopt(s, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    struct sockaddr_in addr = { .sin_family = AF_INET,
                                .sin_addr.s_addr = htonl(INADDR_ANY),
                                .sin_port = htons(LISTEN_PORT) };
    if (bind(s, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("bind"); exit(EXIT_FAILURE);
    }
    if (listen(s, BACKLOG) < 0) {
        perror("listen"); exit(EXIT_FAILURE);
    }
    return s;
}

int main(void) {
    signal(SIGINT, sigint_handler);

    /* --- OpenSSL one-time init --- */
    SSL_load_error_strings();
    OpenSSL_add_ssl_algorithms();
    const SSL_METHOD *method = TLS_server_method();
    SSL_CTX *ctx = SSL_CTX_new(method);
    if (!ctx) { fprintf(stderr, "SSL_CTX_new failed\n"); ERR_print_errors_fp(stderr); exit(EXIT_FAILURE); }

    /* Use TLS 1.2+ only */
    SSL_CTX_set_min_proto_version(ctx, TLS1_2_VERSION);

    /* Load server cert & key */
    if (SSL_CTX_use_certificate_file(ctx, CERT_FILE, SSL_FILETYPE_PEM) <= 0 ||
        SSL_CTX_use_PrivateKey_file(ctx, KEY_FILE, SSL_FILETYPE_PEM) <= 0 ||
        !SSL_CTX_check_private_key(ctx)) {
        fprintf(stderr, "Failed loading cert/key\n"); ERR_print_errors_fp(stderr); exit(EXIT_FAILURE);
    }

    int listen_fd = create_listen_socket();
    printf("[+] TLS server listening on port %d … (Ctrl-C to stop)\n", LISTEN_PORT);

    while (keep_running) {
        struct sockaddr_in cli_addr;
        socklen_t len = sizeof(cli_addr);
        int client_fd = accept(listen_fd, (struct sockaddr *)&cli_addr, &len);
        if (client_fd < 0) {
            if (errno == EINTR) break;
            perror("accept"); continue;
        }

        char ip[INET_ADDRSTRLEN];
        inet_ntop(AF_INET, &cli_addr.sin_addr, ip, sizeof(ip));
        printf("[+] Connection from %s:%d\n", ip, ntohs(cli_addr.sin_port));

        SSL *ssl = SSL_new(ctx);
        SSL_set_fd(ssl, client_fd);

        if (SSL_accept(ssl) <= 0) {
            fprintf(stderr, "[-] TLS handshake failed\n");
            ERR_print_errors_fp(stderr);
        } else {
            char buf[BUF_SIZE];
            int n;
            while ((n = SSL_read(ssl, buf, sizeof(buf))) > 0) {
                SSL_write(ssl, buf, n);  // echo
            }
        }

        SSL_shutdown(ssl);
        SSL_free(ssl);
        close(client_fd);
        printf("[*] Connection closed\n");
    }

    close(listen_fd);
    SSL_CTX_free(ctx);
    EVP_cleanup();
    printf("Server terminated gracefully.\n");
    return 0;
}

