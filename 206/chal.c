#include <sys/ioctl.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <malloc.h>
#include <stdbool.h>

#define MIN_LEN 2
#define THRESHOLD 8
#define MAX_LEN 256

struct id_card_t {
  bool init;
  size_t age;
  union {
    char* long_name;
    char short_name [THRESHOLD];
  };
  bool has_short_name;
} id_card_t;

struct id_card_t id_card = {0};
char name_buffer[MAX_LEN+1];

char flag[MAX_LEN+1];

void menu() {
  puts("ID card utility");
  puts("1 - Edit ID");
  puts("2 - Print ID");
  puts("3 - Exit");
  printf("> ");
}

void load_flag() {
  int fd = open("./flag",O_RDONLY);
  if (fd < 0) {
    puts("ERROR: if you run this locally please add a dummy 'flag' file in the current working directory");
    exit(1);
  }
  read(fd,flag,MAX_LEN);
  close(fd);
}

size_t getnumber() {
  size_t cmd = 0;
  scanf("%zu",&cmd);
  getchar();
  return cmd;
}

void edit_id() {
  size_t name_len = 0;

  printf("age> ");
  id_card.age = getnumber();

  printf("name length> ");
  name_len = getnumber();

  if(name_len < MIN_LEN || name_len > MAX_LEN) {
    printf("invalid length: %zu\n",name_len);
    return;
  }

  printf("name> ");
  if(name_len <=  THRESHOLD) {
    id_card.has_short_name = true;
    fgets(id_card.short_name,name_len+1,stdin);
  } else {
    id_card.has_short_name = false;
    id_card.long_name = name_buffer;
    fgets(id_card.long_name,name_len+1,stdin);
  }
  id_card.init = true;
}

void print_id() {
  if(id_card.init) {
    printf("age: %zu\n",id_card.age);
    char* name = id_card.has_short_name ? id_card.short_name : id_card.long_name;
    printf("name: %s\n",name);
  } else {
    puts("id not initialized");
  }
}

int main() {
  setbuf(stdin,NULL);
  setbuf(stdout,NULL);
  setbuf(stderr,NULL);

  load_flag();
  while(1) {
    menu();
    switch(getnumber()) {
      case 1:
	edit_id();
	break;
      case 2:
	print_id();
	break;
      case 3:
	return 0;
	break;
      default:
	puts("unknown cmd");
	break;
    }
  }
}

