/* mesurer_openssl.c — LA BASELINE OpenSSL EVP AES-128-GCM (2sown2h3z) :
 * même machine, même entrée 4096 o (le clair du rig, la clé et l'IV aux
 * mêmes valeurs — le protocole : la comparaison au périmètre équivalent,
 * n=20, cœur épinglé, RDTSCP). */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <sched.h>
#include <string.h>
#include <openssl/evp.h>
#include "donnees_rig.h"

static uint64_t cyc[32];
int main(void) {
    cpu_set_t m; CPU_ZERO(&m); CPU_SET(1, &m);
    sched_setaffinity(0, sizeof(m), &m);
    unsigned char ct[4112], tag[16];
    uint64_t t0, t1; uint32_t a, d;
    int n;
    /* l'échauffement */
    for (int w = 0; w < 10; w++) {
        EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
        EVP_EncryptInit_ex(ctx, EVP_aes_128_gcm(), NULL, NULL, NULL);
        EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_IVLEN, 12, NULL);
        EVP_EncryptInit_ex(ctx, NULL, NULL, CLES, COMPTEURS);
        EVP_EncryptUpdate(ctx, ct, &n, CLAIR, 4096);
        EVP_EncryptFinal_ex(ctx, ct, &n);
        EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_GET_TAG, 16, tag);
        EVP_CIPHER_CTX_free(ctx);
    }
    for (int i = 0; i < 32; i++) {
        __asm__ volatile("rdtscp" : "=a"(a), "=d"(d) :: "rcx");
        t0 = ((uint64_t)d << 32) | a;
        for (int k = 0; k < 10; k++) {
            EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
            EVP_EncryptInit_ex(ctx, EVP_aes_128_gcm(), NULL, NULL, NULL);
            EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_IVLEN, 12, NULL);
            EVP_EncryptInit_ex(ctx, NULL, NULL, CLES, COMPTEURS);
            EVP_EncryptUpdate(ctx, ct, &n, CLAIR, 4096);
            EVP_EncryptFinal_ex(ctx, ct, &n);
            EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_GET_TAG, 16, tag);
            EVP_CIPHER_CTX_free(ctx);
        }
        __asm__ volatile("rdtscp" : "=a"(a), "=d"(d) :: "rcx");
        t1 = ((uint64_t)d << 32) | a;
        cyc[i] = t1 - t0;
    }
    for (int i = 0; i < 32; i++) for (int j = i + 1; j < 32; j++)
        if (cyc[j] < cyc[i]) { uint64_t t = cyc[i]; cyc[i] = cyc[j]; cyc[j] = t; }
    double med = (double)(cyc[15] + cyc[16]) / 2.0 / 10.0;
    double iqr = (double)(cyc[23] + cyc[24]) / 2.0 - (double)(cyc[7] + cyc[8]) / 2.0;
    printf("BASELINE OpenSSL EVP AES-128-GCM 4096 o (n=20, 10 appels/mesure) : "
           "mediane=%.1f c [IQR %.1f] -> %.4f c/octet@4096\n",
           med, iqr / 10.0, med / 4096.0);
    return 0;
}
