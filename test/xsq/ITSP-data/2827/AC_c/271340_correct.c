
#include<stdio.h>

int main()
{
    float x1, x2, x3;
    float y1, y2, y3;
    scanf("%f %f %f %f %f %f", &x1, &y1, &x2, &y2, &x3, &y3);
    float Y2 = y2 - y1;
    float Y3 = y3 - y1;
    float X2 = x2 - x1;
    float X3 = x3 - x1;
    if(X2 != 0 && X3 != 0)
    {
        float slope1 = Y2 / X2;
        float slope2 = Y3 / X3;
        if(slope1 == slope2)
        {
            printf("All the points are on same line.");
        }
        else
        {
            printf("All the points are not on same line.");
        }
    }
    else if(X2 == 0 && X3 == 0)
    {
        printf("All the points are on same line.");
    }
    else
    {
        printf("All the points are not on same line.");
    }
    return 0;
}
