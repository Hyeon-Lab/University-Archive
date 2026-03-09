#include <stdio.h>

// ------------------------------------------------
// 1. 필수 매크로 정의 확인 (ifndef 사용)
// ------------------------------------------------
#ifndef BAUD_RATE
// BAUD_RATE가 정의되어 있지 않다면 컴파일 오류 발생
#error "Compile Error: BAUD_RATE is not defined. -DBAUD_RATE=<value> "
#endif

// ------------------------------------------------
// 2. 정의된 값의 유효성 검사 (if 사용)
// ------------------------------------------------
#if BAUD_RATE != 9600 && BAUD_RATE != 115200
// BAUD_RATE가 유효한 값 목록에 없다면 컴파일 오류 발생
#error "Compile Error: Unsupported BAUD_RATE (Type 9600 or 115200)"
#endif

// ------------------------------------------------
// 3. 모든 검사를 통과한 경우 (정상 코드)
// ------------------------------------------------

int main()
{
	printf("baud_rate.c\n");
	printf("Baud Rate: %d bps\n", BAUD_RATE);
	return 0;
}