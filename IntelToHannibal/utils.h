#ifndef UTILS_H
#define UTILS_H
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <time.h>

#define START_ADDR_PATTERN	":10040000"
#define STOP_ADDR_PATTERN	":101BF000"
#define OUT_FILE_NAME		"bootloader_memory.h"
#define TMP_FILE_NAME		"/tmp/.h"
//#define CLEAN_OUT

//******** TERMINAL COLOR
#define KRED	"\033[31m"
#define KGRN   	"\033[32m"
#define KYEL   	"\033[33m"
#define KBLU   	"\033[34m"
#define KMAG   	"\033[35m"
#define KCYN   	"\033[36m"
#define KWHT   	"\033[37m"
#define RESET	"\033[0m"

#define print_kblu(fmt, args...)		\
do {									\
	fprintf( stdout, "%s", KBLU );		\
	fprintf( stdout, fmt, ##args);	    \
	fprintf( stdout, "%s", RESET );	    \
} while (0)
#define print_kgrn(fmt, args...)		\
do {									\
	fprintf( stdout, "%s", KGRN );		\
	fprintf( stdout, fmt, ##args);	    \
	fprintf( stdout, "%s", RESET );	    \
} while (0)
#define print_kred(fmt, args...)		\
do {									\
	fprintf( stdout, "%s", KRED );		\
	fprintf( stdout, fmt, ##args);	    \
	fprintf( stdout, "%s", RESET );	    \
} while (0)
#define print_kyel(fmt, args...)		\
do {									\
	fprintf( stdout, "%s", KYEL );		\
	fprintf( stdout, fmt, ##args);	    \
	fprintf( stdout, "%s", RESET );	    \
} while (0)
#define print_kmag(fmt, args...)		\
do {									\
	fprintf( stdout, "%s", KMAG );		\
	fprintf( stdout, fmt, ##args);	    \
	fprintf( stdout, "%s", RESET );	    \
} while (0)



#endif // UTILS_H
