// compile with `gcc -static -O0 -m32 -s -Wl,--section-start=.text=0x11111111 2.c`
// note that -m32 is so addresses are short and --section-start is so there's no NULL in the address

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// this leaks memory but whatever, the program will exit quickly
char* read_flag(void) {
        FILE* f = fopen("flag", "r");
        char* flag = calloc(128, sizeof(char));
        fscanf(f, "%127s", flag);
        fclose(f);
        return flag;
}


int main() {
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
    setbuf(stdin, NULL);
	char input[128];
    char* flag = read_flag();

	printf("Input your magical spell! ");
	scanf("%127[^\n]", input);
	printf(input);
	printf("\nHope you got what you wanted!\n");
	fflush(stdout);

	return 0;
}
