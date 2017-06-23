#include <math.h>
#include <stdio.h>
#include <stdlib.h>

static void c_phongShader(int x, int y, double z, double nx, double ny, double nz, int nlights, double *lxs, double *lys, double *lzs, double **Ias, double **Ids, double **Iss, double* bal, double vx, double vy, double vz, double *Ka, double *Kd, double *Ks, int a, double *Cin, int *Cout) {
    double vxx = vx - x;
    double vyy = vy - y;
    double vzz = vz - z;
    double vd = sqrt(vxx * vxx + vyy * vyy + vzz * vzz);
    double Vx = vxx / vd;
    double Vy = vyy / vd;
    double Vz = vzz / vd;
    Cin[0] = Ka[0] * bal[0];
    Cin[1] = Ka[1] * bal[1];
    Cin[2] = Ka[2] * bal[2];
    int i;
    double lxx;
    double lyy;
    double lzz;
    double ld;
    double Lmx;
    double Lmy;
    double Lmz;
    double Lmn;
    double Rmx;
    double Rmy;
    double Rmz;
    double diff;
    double RmV;
    double spec;
    int j;
    for(i = 0; i < nlights; i++) {
        lxx = lxs[i] - x;
        lyy = lys[i] - y;
        lzz = lzs[i] - z;
        ld = sqrt(lxx*lxx+lyy*lyy+lzz*lzz);
        Lmx = lxx / ld;
        Lmy = lyy / ld;
        Lmz = lzz / ld;
        Lmn = Lmx * nx + Lmy * ny + Lmz * nz;
        Rmx = 2 * Lmn * nx - Lmx;
        Rmy = 2 * Lmn * ny - Lmy;
        Rmz = 2 * Lmn * nz - Lmz;
        diff = Lmn < 0 ? 0 : Lmn;
        RmV = Rmx*Vx+Rmy*Vy+Rmz*Vz;
        if (RmV <= 0) {
            spec = 0;
        }
        else if(RmV >= 1) {
            spec = 1;
        }
        else {
            spec = pow(RmV, a);
        }
        for(j = 0; j < 3; j++) {
            Cin[j] += Ka[j]*Ias[i][j] + Kd[j]*Ids[i][j]*diff + Ks[j]*Iss[i][j]*spec;
        }
    }
    for(i = 0; i < 3; i++) {
        Cout[i] = (int)(255*(Cin[i] > 1 ? 1 : pow(Cin[i], 1/2.2)));
    }
}

int main() {
    int x = 300;
    int y = 300;
    double z = 300;
    double nx = 1;
    double ny = 0;
    double nz = 0;
    int nlights = 2;
    double Ia[] = {1., 0.5, 0.6};
    double *Id = Ia;
    double Is[] = {1., 0.8, 0.9};
    double *Ias[] = {Ia, Ia};
    double *Ids[] = {Id, Id};
    double *Iss[] = {Is, Is};
    double lxs[] = {400, 500};
    double lys[] = {300, 250};
    double lzs[] = {350, 250};
    double bal[] = {0.1, 0.2, 0.1};
    double vx = 250;
    double vy = 250;
    double vz = 20000;
    double Ka[] = {0.2, 0.3, 0.8};
    double *Kd = Ka;
    double Ks[] = {0.5, 0.5, 1};
    int a = 10;
    double *Cin = calloc(sizeof(double), 3);
    int *Cout = calloc(sizeof(int), 3);
    phongShader( x,  y,  z,  nx,  ny,  nz,  nlights, lxs, lys, lzs, Ias, Ids, Iss, bal,  vx,  vy,  vz,  Ka,  Kd, Ks,  a,  Cin,  Cout);
    printf("%d %d %d", Cout[0], Cout[1], Cout[2]);
}
