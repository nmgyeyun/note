#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>



void func_test_lat(char *api_name, int i)
{
	long int r;
	float sleep_time;
	r = random() % 100;
	sleep_time = r * 1.0 / 100.0 + 0.5;

	printf("api %s %d sleep %0.3f second len %d...\n", api_name, i, sleep_time, strlen(api_name));
	sleep(sleep_time);
	
}

int main(void)
{
	int i;
	char api[10][16];

	for (i=0;i<10;i++) {
		snprintf(api[i], sizeof(api[i]), "api%d", i);
	}
		
	while (1) {
		for (i=0;i<10;i++) {
			func_test_lat(api[i], i);
		}
	}
}
