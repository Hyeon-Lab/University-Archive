#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>


#pragma pack(push, 1) // padding 제거 
typedef struct {
	char name[50];
	int id;
	int score;
	double average;
} Packet;
#pragma pack(pop)

void error_handling(char *message);

int main(int argc, char *argv[])
{
	int serv_sock;
	int clnt_sock;

	struct sockaddr_in serv_addr;
	struct sockaddr_in clnt_addr;
	socklen_t clnt_addr_size;
	int len = 0;
	socklen_t optlen;
	int option;

	Packet recv_data, send_data;
	memset(&recv_data, 0, sizeof(Packet));

	if (argc != 2)
	{
		printf("Usage : %s <port>\n", argv[0]);
		exit(1);
	}
	// 1단계: 소켓 생성
	serv_sock = socket(PF_INET, SOCK_STREAM, 0);
	if (serv_sock == -1)
		error_handling("socket() error");

	// SO_REUSEADDR 설정 
	optlen = sizeof(option);
	option = 1;
	setsockopt(serv_sock, SOL_SOCKET, SO_REUSEADDR, &option, optlen);

	memset(&serv_addr, 0, sizeof(serv_addr));
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
	serv_addr.sin_port = htons(atoi(argv[1]));

	// 2단계: bind
	if (bind(serv_sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) == -1)
		error_handling("bind() error");

	// 3단계: listen
	if (listen(serv_sock, 5) == -1)
		error_handling("listen() error");

	clnt_addr_size = sizeof(clnt_addr);
	// 4단계: accept
	clnt_sock = accept(serv_sock, (struct sockaddr *)&clnt_addr, &clnt_addr_size);
	if (clnt_sock == -1)
		error_handling("accept() error");
	else
		printf("Connected Client IP: %s\n", inet_ntoa(clnt_addr.sin_addr));

	/*------------------------------------------------------------
	 * [Rx] C Server <--- Java Client
	 *------------------------------------------------------------*/	
	len = read(clnt_sock, &recv_data, sizeof(Packet));
	if (len == -1)
		error_handling("read() error!");
	else
		printf("[Rx] packet len: %d\n", len);

	printf("[Rx] name: %s, id: %d, score: %d, average: %.1f\n",
		   recv_data.name, recv_data.id, recv_data.score, recv_data.average);

	/*------------------------------------------------------------
	 * [Tx] C Server ---> Java Client
	 *------------------------------------------------------------*/
	memset(&send_data, 0, sizeof(Packet));

	strcpy(send_data.name, "Dennis Richie");
	send_data.id = 2000;
	send_data.score = 80;
	send_data.average = 85.9;

	printf("[Tx] name: %s, id: %d, score: %d, average: %.1f\n",
		   send_data.name, send_data.id, send_data.score, send_data.average);

	write(clnt_sock, &send_data, sizeof(Packet));

	close(clnt_sock);
	close(serv_sock);
	return 0;
}

void error_handling(char *message)
{
	fputs(message, stderr);
	fputc('\n', stderr);
	exit(1);
}
