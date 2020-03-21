#include "utils.h"

FILE *outfile;
FILE *tfile;
char firstline[100], lastline[100];

uint32_t bytes;

void file_creation(struct stat *filestat)
{
	char line[100];
	char major_str[2+1];
	char minor_str[2+1];
	uint8_t major;
	uint8_t minor;

	memset(&major_str,	0, sizeof(major_str));
	memset(&minor_str,	0, sizeof(minor_str));

	strncpy(minor_str, &firstline[9], 2 );
	strncpy(major_str, &firstline[11], 2 );
	minor = strtol(minor_str, NULL, 16);
	major = strtol(major_str, NULL, 16);

	//printf("File changed time %s \n", ctime(&filestat->st_mtime) );
	fprintf(outfile, "/*\n");
	fprintf(outfile, " * File:\t%s\n", OUT_FILE_NAME );
	fprintf(outfile, " * Author:\tluigi.scagnet\n" );
	fprintf(outfile, " *\n" );
	fprintf(outfile, " * Created on:\t%s", ctime(&filestat->st_mtime) );
	fprintf(outfile, " */\n");
	fprintf(outfile, "#ifndef BOOTLOADER_MEMORY_H\n"				);
	fprintf(outfile, "#define BOOTLOADER_MEMORY_H\n"				);
	fprintf(outfile, "#include \"GenericTypeDefs.h\"\n"				);
	fprintf(outfile, "#define BOOTLOADER_VERSION 0x%02X%02X\n", major, minor);
	fprintf(outfile, "// CODE OF Bootloader %02X%02X\n",		major, minor);
	fprintf(outfile, "const tU32 bootloader_code[] = {\n"			);
#ifndef CLEAN_OUT
	fprintf(outfile, "\t/* BL START 0x200\n");
	fprintf(outfile, "\t * BL SIZE  0xC00\n");
	fprintf(outfile, "\t * BL END   0xE00 - 1 = 0xDFF\n");
	fprintf(outfile, "\t * BL Start Intel file 0400\n");
	fprintf(outfile, "\t * BL End   Intel file 1C00 - 1 = 0x1BFF\n");
	fprintf(outfile, "\t * First Line:\n");
	fprintf(outfile, "\t * %s", firstline);
	fprintf(outfile, "\t * Last Line:\n");
	fprintf(outfile, "\t * %s", lastline);
	fprintf(outfile, "\t */\n");
#endif
	while (fgets(line, sizeof(line), tfile))
		fprintf(outfile, "%s", line);
	fprintf(outfile, "};\n" );
	fprintf(outfile, "#endif	/* BOOTLOADER_MEMORY_H */\n\n" );
}

void parse_out(char *line)
{
	char datasize_str[2+1], address_str[4+1], datatype_str[2+1], data_str[8+1], checksum_str[2+1];
	char array_data_line[100];
	uint8_t i, datasize, datatype;
#ifndef CLEAN_OUT
	uint8_t checksum, bt;
#endif
	uint16_t address;
	uint32_t data;

	memset(&datasize_str,	0, sizeof(datasize_str));
	memset(&address_str,	0, sizeof(address_str));
	memset(&datatype_str,	0, sizeof(datatype_str));
	memset(&data_str,		0, sizeof(data_str));
	memset(&checksum_str,	0, sizeof(data_str));
	memset(&array_data_line,0, sizeof(data_str));

	strncpy(datasize_str, &line[1], 2 );
	datasize = strtol(datasize_str, NULL, 16);
	strncpy(address_str, &line[3], 4 );
	address = strtol(address_str, NULL, 16);
	strncpy(datatype_str, &line[7], 2 );
	datatype = strtol(datatype_str, NULL, 16);

	printf(":");
	print_kblu("%02X", datasize);
	print_kgrn("%04X", address);
	print_kred("%02X", datatype);

#ifndef CLEAN_OUT
	fprintf(tfile, "/* :");
	fprintf(tfile, "%02X ", datasize);
	fprintf(tfile, "%04X ", address);
	fprintf(tfile, "%02X ", datatype);
	fprintf(tfile, "*/ ");
#endif
	i=0;
	while(i<datasize)
	{
		strncpy(data_str, &line[9+(i*2)], 8 );
		data = strtol(data_str, NULL, 16);
		print_kyel("%08X", data);
		fprintf(tfile, "0x%08X, ", data);
		i+=4;
	}
#ifndef CLEAN_OUT
	bytes+=datasize;

	strncpy(checksum_str, &line[9+(datasize*2)], 2 );
	checksum = strtol(checksum_str, NULL, 16);
	print_kmag("%02X", checksum);
	bt = bytes%128 != 0 ? bytes%128 : 128;
	if(bt>=100)
		fprintf(tfile, " //%02X -- %d", checksum, bt);
	else
		fprintf(tfile, " //%02X --  %d", checksum, bt);
	fprintf(tfile, " bytes \t# %d", bytes);
#endif
	printf("\n");
	fprintf(tfile, "\n");

}

int main(int argc, char* argv[])
{
	FILE* infile;
	char line[100];
	bool out = false;
	struct stat filestat;

	if(argc<2)
	{
		printf("Inputfile needed\n");
		exit(1);
	}
	stat(argv[1],&filestat);
	infile = fopen(argv[1], "r");
	tfile = fopen(TMP_FILE_NAME, "w");
	bytes = 0;

	while (fgets(line, sizeof(line), infile))
	{
		if(strstr(line, START_ADDR_PATTERN) != NULL)
		{
			strcpy( firstline, line );
			out=true;
		}
		if(out)
		{
			strcpy( lastline, line );
			parse_out(line);
		}
		if(strstr(line, STOP_ADDR_PATTERN) != NULL)
			out=false;
	}
	//printf("===> %s \n", firstline);
	//printf("<=== %s \n", lastline);
	fclose(tfile);

	outfile = fopen(OUT_FILE_NAME, "w");
	tfile = fopen(TMP_FILE_NAME, "r");
	file_creation(&filestat);
	fclose(tfile);
	remove(TMP_FILE_NAME);

	fclose(outfile);
	fclose(infile);

	return 0;
}
