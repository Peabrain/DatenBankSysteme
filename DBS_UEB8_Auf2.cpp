//
//  main.cpp
//  kmeans
//
//  Created by PeabrainC64 on 02.07.17.
//  Copyright © 2017 PeabrainC64. All rights reserved.
//

#include <iostream>
#include <math.h>

struct DATA
{
    float x,y;
    float distToZ[3];
};
DATA data[] =
{
    {22,57},
    {79,46},
    {61,52},
    {14,20},
    {22,14},
    {75,17},
    {81,40},
    {2,91},
    {96,63},
    {4,31}
};

int main(int argc, const char * argv[]) {
    // insert code here...
    std::cout << "k-Means\n";
    DATA z[3] =
    {
        {14,20},
        {0,0},
        {96,63}
    };
    
    z[1].x = (z[0].x + z[2].x) / 2;
    z[1].y = (z[0].y + z[2].y) / 2;
    int k = 1;
    while(1)
    {
        DATA newZ[3] = {{0,0},{0,0},{0,0}};
        int newZcount[3] = {0,0,0};
        printf("Step %i\n",k++);
        for(int i = 0;i < 10;i++)
        {
            float zdist = 100000000000000000;
            int zidx = -1;
            for(int j = 0;j < 3;j++)
            {
                float z1 = sqrt((z[j].x - data[i].x) * (z[j].x - data[i].x) + (z[j].y - data[i].y) * (z[j].y - data[i].y));
                if(z1 < zdist)
                {
                    zdist = z1;
                    zidx = j;
                }
            }
            if(zidx != -1)
            {
                newZ[zidx].x += data[i].x;
                newZ[zidx].y += data[i].y;
                newZcount[zidx]++;
                printf("set: %i (%2.2f,%2.2f),\tcluster: %i\n",i,data[i].x,data[i].y,zidx);
            }
        }
        int count = 0;
        for(int j = 0;j < 3;j++)
        {
            newZ[j].x /= (float)newZcount[j];
            newZ[j].y /= (float)newZcount[j];
            printf("cluster(%i): old (%2.2f,%2.2f), ",j + 1,z[j].x,z[j].y);
            float xd = newZ[j].x - z[j].x;
            float yd = newZ[j].y - z[j].y;
            float delta  = sqrt(xd * xd + yd * yd);
            if(delta < (float)2/(float)3)
                count++;
            z[j].x = newZ[j].x;
            z[j].y = newZ[j].y;
            printf("new (%2.2f,%2.2f), Delta = %f\n",z[j].x,z[j].y,delta);
        }
        if(count == 3) break;
    }
    return 0;
}
