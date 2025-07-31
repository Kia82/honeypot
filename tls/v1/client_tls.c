// Simple TLS client using OpenSSL 1.1+ / 3.x
// Compile with: gcc -Wall -Wextra -o client_tls client_tls.c -lssl -lcrypto

#define _POSIX_C_SOURCE 200809L
#include <arpa/inet.h>
#include <netdb.h>
#include <openssl/err.h>
#include <openssl/ssl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define SERVER_HOST "127.0.0.1"
#define SERVER_PORT "4443"
#define BUF_SIZE    4096

static int tcp_connect(const char *host, const char *port) {
    struct addrinfo hints = {.ai_family = AF_INET, .ai_socktype = SOCK_STREAM};
    struct addrinfo *res;
    if (getaddrinfo(host, port, &hints, &res) != 0) { perror("getaddrinfo"); exit(EXIT_FAILURE); }

    int s = socket(res->ai_family, res->ai_socktype, res->ai_protocol);
    if (s < 0) { perror("socket"); exit(EXIT_FAILURE); }

    if (connect(s, res->ai_addr, res->ai_addrlen) < 0) { perror("connect"); exit(EXIT_FAILURE); }
    freeaddrinfo(res);
    return s;
}

int main(void) {
    /* OpenSSL one-time init */
    SSL_load_error_strings();
    OpenSSL_add_ssl_algorithms();

    const SSL_METHOD *method = TLS_client_method();
    SSL_CTX *ctx = SSL_CTX_new(method);
    if (!ctx) { fprintf(stderr, "SSL_CTX_new failed\n"); ERR_print_errors_fp(stderr); exit(EXIT_FAILURE); }

    /* Optionally verify server certificate (using default system store or custom) */
    SSL_CTX_set_default_verify_paths(ctx);
    SSL_CTX_set_verify(ctx, SSL_VERIFY_NONE, NULL); // SSL_VERIFY_PEER
    SSL_CTX_set_min_proto_version(ctx, TLS1_2_VERSION);

    int sock = tcp_connect(SERVER_HOST, SERVER_PORT);

    SSL *ssl = SSL_new(ctx);
    SSL_set_fd(ssl, sock);

    if (SSL_connect(ssl) <= 0) {
        fprintf(stderr, "TLS handshake failed\n"); ERR_print_errors_fp(stderr); exit(EXIT_FAILURE);
    }
    printf("[+] Connected with %s encryption\n", SSL_get_cipher(ssl));

    /* Read from STDIN, send, print echo */
    char buf[BUF_SIZE];
    int n;
    while ((n = fread(buf, 1, sizeof(buf), stdin)) > 0) {
        SSL_write(ssl, buf, n);
        int m = SSL_read(ssl, buf, sizeof(buf));
        fwrite(buf, 1, m, stdout);
    }

    SSL_shutdown(ssl);
    SSL_free(ssl);
    close(sock);
    SSL_CTX_free(ctx);
    EVP_cleanup();
    return 0;
}

