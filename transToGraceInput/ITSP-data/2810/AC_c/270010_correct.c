/*numPass=4, numTotal=4
Verdict:ACCEPTED, Visibility:1, Input:"1 1", ExpOutput:"The area of (1.0000,1.0000), (1.0000,0) and (0,1.0000) is 0.5000.
", Output:"The area of (1.0000,1.0000), (1.0000,0) and (0,1.0000) is 0.5000."
Verdict:ACCEPTED, Visibility:1, Input:"-1 1", ExpOutput:"The area of (-1.0000,1.0000), (-1.0000,0) and (0,1.0000) is 0.5000.
", Output:"The area of (-1.0000,1.0000), (-1.0000,0) and (0,1.0000) is 0.5000."
Verdict:ACCEPTED, Visibility:0, Input:"-100 -9", ExpOutput:"The area of (-100.0000,-9.0000), (-100.0000,0) and (0,-9.0000) is 450.0000.
", Output:"The area of (-100.0000,-9.0000), (-100.0000,0) and (0,-9.0000) is 450.0000."
Verdict:ACCEPTED, Visibility:0, Input:"0.0001 -1000", ExpOutput:"The area of (0.0001,-1000.0000), (0.0001,0) and (0,-1000.0000) is 0.0500.
", Output:"The area of (0.0001,-1000.0000), (0.0001,0) and (0,-1000.0000) is 0.0500."
*/
#include<stdio.h>

int main()
{
    float a,b,area;
    scanf("%f %f",&a, &b);
    area=.5*a*b;
    if (area>0)
    {
        printf("The area of (%.4f,%.4f), (%.4f,0) and (0,%.4f) is %.4f.",a,b,a,b,area);
    }
    else
    {
        printf("The area of (%.4f,%.4f), (%.4f,0) and (0,%.4f) is %.4f.",a,b,a,b,-area);
    }


    return 0;
}
int foo(int x,int y) {
    if (x > y) {
        return x;
    } else {
        return y;
    }
}
int main2()
{
    //to determine sign of a number
    float n;
    scanf("%f",&n);
    if(n>0)
    {
        printf("%.4f is positive,%n");//number is positive
    }
    else
    {
        if (n==0)
        {
            printf("input is zero");//number is 0
        }
        else
        {
            printf("%.4f is negative,%n");
        }
    }//number is negative

    return 0;
}
double bar(double a, double b, double c) {
    double d = a * b + c;
    return d;
}
