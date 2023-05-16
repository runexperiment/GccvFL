/*numPass=5, numTotal=5
Verdict:ACCEPTED, Visibility:1, Input:"12345", ExpOutput:"Reverse of 12345 is 54321", Output:"Reverse of 12345 is 54321"
Verdict:ACCEPTED, Visibility:1, Input:"1331", ExpOutput:"Reverse of 1331 is 1331", Output:"Reverse of 1331 is 1331"
Verdict:ACCEPTED, Visibility:1, Input:"100", ExpOutput:"Reverse of 100 is 1", Output:"Reverse of 100 is 1"
Verdict:ACCEPTED, Visibility:0, Input:"0", ExpOutput:"Reverse of 0 is 0", Output:"Reverse of 0 is 0"
Verdict:ACCEPTED, Visibility:0, Input:"10", ExpOutput:"Reverse of 10 is 1", Output:"Reverse of 10 is 1"
*/
#include<stdio.h>

int main()
{
    int a,x=0;
    scanf("%d",&a);//input a(while initialisation)
    int f=a;
    while(a>0)//while condition
    {
        int d=a%10;//to get one digit
        x=x*10+d;
        a=a/10;//while updation
    }
    printf("Reverse of %d is %d",f,x);
    return 0;
}