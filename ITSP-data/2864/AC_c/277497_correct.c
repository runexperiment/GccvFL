
#include<stdio.h>

int check_prime(int num)
{
    int i;
    if(num == 1)
    {
        return 0;
    }

    for(i = 2; i <= num - 1; i++)

    {
        if(num % i == 0)
        {
            return 0;
        }


    }

    return 1;
}

int main()
{
    int i, n1, n2;
    scanf("%d %d", &n1, &n2);
    for(i = n1; i <= n2; i++)

        if(check_prime(i))
        {
            printf("%d ", i);
        }


    return 0;
}
