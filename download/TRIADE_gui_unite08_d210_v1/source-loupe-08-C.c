#include <stddef.h>
static const char hex_chars[] = "0123456789ABCDEF";

long long loupe_08_ligne(const unsigned char *src, size_t len, char *out, size_t offset) {
    if (!src || !out || len == 0 || len > 16) {
        return -5;
    }

    char *p = out;
    const unsigned char *s = src;

    size_t i;
    for (i = 0; i < 8; ++i) {
        *p++ = hex_chars[(offset >> (4 * (7 - i))) & 0xF];
    }
    *p++ = ' ';
    *p++ = ' ';

    for (i = 0; i < 16; ++i) {
        if (i < len) {
            *p++ = hex_chars[s[i] >> 4];
            *p++ = hex_chars[s[i] & 0xF];
        } else {
            *p++ = ' ';
            *p++ = ' ';
        }
        if (i < 15) {
            if (i == 7) {
                *p++ = ' ';
                *p++ = ' ';      /* le médian DOUBLÉ (Q1) */
            } else {
                *p++ = ' ';      /* le séparateur simple */
            }
        }
    }

    *p++ = ' ';
    *p++ = ' ';

    for (i = 0; i < 16; ++i) {
        if (i < len) {
            unsigned char c = s[i];
            *p++ = (c >= 0x20 && c <= 0x7E) ? c : '.';
        } else {
            *p++ = ' ';
        }
    }

    *p = '\0';

    return 0;
}
