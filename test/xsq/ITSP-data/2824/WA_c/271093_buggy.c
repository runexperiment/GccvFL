#include<stdio.h>

int main()
{
    int Y;
    scanf("%d",&Y);
    if(Y%4==0) 
    {
        if(Y%100==0&&Y%400==0)
        {
            printf("Leap Year");
        }
        else
        {
            printf("Not Leap Year");
        }
        if(Y%100!=0)
        {
            printf("Leap Year");
        }
    }
    else
    {
        printf("Not Leap Year");
    }
    
    return 0;
}
