
#include<stdio.h>

int main()
{
    int N, i, j;
    scanf("%d", &N);
    for(i = 1; i <= N; i++)
    {
        for(j = 1; j <= N; j++)
        {
            if(j < i)
            {
                printf("%d", N - i + j);
            }
            else
            {
                printf("%d", N);
            }
        }
        printf("\n");
    }


    return 0;
}
