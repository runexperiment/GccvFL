
#include<stdio.h>

int main()
{
    int N, i;
    int sum = 0;
    scanf("%d", &N);
    for(i = 1; i <= N; i++)
    {
        sum += i * (i + 1) / 2;


    }
    printf("%d", sum);
    return 0;
}
