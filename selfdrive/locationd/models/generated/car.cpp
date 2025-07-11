#include "car.h"

namespace {
#define DIM 9
#define EDIM 9
#define MEDIM 9
typedef void (*Hfun)(double *, double *, double *);

double mass;

void set_mass(double x){ mass = x;}

double rotational_inertia;

void set_rotational_inertia(double x){ rotational_inertia = x;}

double center_to_front;

void set_center_to_front(double x){ center_to_front = x;}

double center_to_rear;

void set_center_to_rear(double x){ center_to_rear = x;}

double stiffness_front;

void set_stiffness_front(double x){ stiffness_front = x;}

double stiffness_rear;

void set_stiffness_rear(double x){ stiffness_rear = x;}
const static double MAHA_THRESH_25 = 3.8414588206941227;
const static double MAHA_THRESH_24 = 5.991464547107981;
const static double MAHA_THRESH_30 = 3.8414588206941227;
const static double MAHA_THRESH_26 = 3.8414588206941227;
const static double MAHA_THRESH_27 = 3.8414588206941227;
const static double MAHA_THRESH_29 = 3.8414588206941227;
const static double MAHA_THRESH_28 = 3.8414588206941227;
const static double MAHA_THRESH_31 = 3.8414588206941227;

/******************************************************************************
 *                       Code generated with SymPy 1.12                       *
 *                                                                            *
 *              See http://www.sympy.org/ for more information.               *
 *                                                                            *
 *                         This file is part of 'ekf'                         *
 ******************************************************************************/
void err_fun(double *nom_x, double *delta_x, double *out_709253069857813121) {
   out_709253069857813121[0] = delta_x[0] + nom_x[0];
   out_709253069857813121[1] = delta_x[1] + nom_x[1];
   out_709253069857813121[2] = delta_x[2] + nom_x[2];
   out_709253069857813121[3] = delta_x[3] + nom_x[3];
   out_709253069857813121[4] = delta_x[4] + nom_x[4];
   out_709253069857813121[5] = delta_x[5] + nom_x[5];
   out_709253069857813121[6] = delta_x[6] + nom_x[6];
   out_709253069857813121[7] = delta_x[7] + nom_x[7];
   out_709253069857813121[8] = delta_x[8] + nom_x[8];
}
void inv_err_fun(double *nom_x, double *true_x, double *out_5721921606894944173) {
   out_5721921606894944173[0] = -nom_x[0] + true_x[0];
   out_5721921606894944173[1] = -nom_x[1] + true_x[1];
   out_5721921606894944173[2] = -nom_x[2] + true_x[2];
   out_5721921606894944173[3] = -nom_x[3] + true_x[3];
   out_5721921606894944173[4] = -nom_x[4] + true_x[4];
   out_5721921606894944173[5] = -nom_x[5] + true_x[5];
   out_5721921606894944173[6] = -nom_x[6] + true_x[6];
   out_5721921606894944173[7] = -nom_x[7] + true_x[7];
   out_5721921606894944173[8] = -nom_x[8] + true_x[8];
}
void H_mod_fun(double *state, double *out_1388721326752473306) {
   out_1388721326752473306[0] = 1.0;
   out_1388721326752473306[1] = 0;
   out_1388721326752473306[2] = 0;
   out_1388721326752473306[3] = 0;
   out_1388721326752473306[4] = 0;
   out_1388721326752473306[5] = 0;
   out_1388721326752473306[6] = 0;
   out_1388721326752473306[7] = 0;
   out_1388721326752473306[8] = 0;
   out_1388721326752473306[9] = 0;
   out_1388721326752473306[10] = 1.0;
   out_1388721326752473306[11] = 0;
   out_1388721326752473306[12] = 0;
   out_1388721326752473306[13] = 0;
   out_1388721326752473306[14] = 0;
   out_1388721326752473306[15] = 0;
   out_1388721326752473306[16] = 0;
   out_1388721326752473306[17] = 0;
   out_1388721326752473306[18] = 0;
   out_1388721326752473306[19] = 0;
   out_1388721326752473306[20] = 1.0;
   out_1388721326752473306[21] = 0;
   out_1388721326752473306[22] = 0;
   out_1388721326752473306[23] = 0;
   out_1388721326752473306[24] = 0;
   out_1388721326752473306[25] = 0;
   out_1388721326752473306[26] = 0;
   out_1388721326752473306[27] = 0;
   out_1388721326752473306[28] = 0;
   out_1388721326752473306[29] = 0;
   out_1388721326752473306[30] = 1.0;
   out_1388721326752473306[31] = 0;
   out_1388721326752473306[32] = 0;
   out_1388721326752473306[33] = 0;
   out_1388721326752473306[34] = 0;
   out_1388721326752473306[35] = 0;
   out_1388721326752473306[36] = 0;
   out_1388721326752473306[37] = 0;
   out_1388721326752473306[38] = 0;
   out_1388721326752473306[39] = 0;
   out_1388721326752473306[40] = 1.0;
   out_1388721326752473306[41] = 0;
   out_1388721326752473306[42] = 0;
   out_1388721326752473306[43] = 0;
   out_1388721326752473306[44] = 0;
   out_1388721326752473306[45] = 0;
   out_1388721326752473306[46] = 0;
   out_1388721326752473306[47] = 0;
   out_1388721326752473306[48] = 0;
   out_1388721326752473306[49] = 0;
   out_1388721326752473306[50] = 1.0;
   out_1388721326752473306[51] = 0;
   out_1388721326752473306[52] = 0;
   out_1388721326752473306[53] = 0;
   out_1388721326752473306[54] = 0;
   out_1388721326752473306[55] = 0;
   out_1388721326752473306[56] = 0;
   out_1388721326752473306[57] = 0;
   out_1388721326752473306[58] = 0;
   out_1388721326752473306[59] = 0;
   out_1388721326752473306[60] = 1.0;
   out_1388721326752473306[61] = 0;
   out_1388721326752473306[62] = 0;
   out_1388721326752473306[63] = 0;
   out_1388721326752473306[64] = 0;
   out_1388721326752473306[65] = 0;
   out_1388721326752473306[66] = 0;
   out_1388721326752473306[67] = 0;
   out_1388721326752473306[68] = 0;
   out_1388721326752473306[69] = 0;
   out_1388721326752473306[70] = 1.0;
   out_1388721326752473306[71] = 0;
   out_1388721326752473306[72] = 0;
   out_1388721326752473306[73] = 0;
   out_1388721326752473306[74] = 0;
   out_1388721326752473306[75] = 0;
   out_1388721326752473306[76] = 0;
   out_1388721326752473306[77] = 0;
   out_1388721326752473306[78] = 0;
   out_1388721326752473306[79] = 0;
   out_1388721326752473306[80] = 1.0;
}
void f_fun(double *state, double dt, double *out_3586979400707933995) {
   out_3586979400707933995[0] = state[0];
   out_3586979400707933995[1] = state[1];
   out_3586979400707933995[2] = state[2];
   out_3586979400707933995[3] = state[3];
   out_3586979400707933995[4] = state[4];
   out_3586979400707933995[5] = dt*((-state[4] + (-center_to_front*stiffness_front*state[0] + center_to_rear*stiffness_rear*state[0])/(mass*state[4]))*state[6] - 9.8000000000000007*state[8] + stiffness_front*(-state[2] - state[3] + state[7])*state[0]/(mass*state[1]) + (-stiffness_front*state[0] - stiffness_rear*state[0])*state[5]/(mass*state[4])) + state[5];
   out_3586979400707933995[6] = dt*(center_to_front*stiffness_front*(-state[2] - state[3] + state[7])*state[0]/(rotational_inertia*state[1]) + (-center_to_front*stiffness_front*state[0] + center_to_rear*stiffness_rear*state[0])*state[5]/(rotational_inertia*state[4]) + (-pow(center_to_front, 2)*stiffness_front*state[0] - pow(center_to_rear, 2)*stiffness_rear*state[0])*state[6]/(rotational_inertia*state[4])) + state[6];
   out_3586979400707933995[7] = state[7];
   out_3586979400707933995[8] = state[8];
}
void F_fun(double *state, double dt, double *out_5085878125767614964) {
   out_5085878125767614964[0] = 1;
   out_5085878125767614964[1] = 0;
   out_5085878125767614964[2] = 0;
   out_5085878125767614964[3] = 0;
   out_5085878125767614964[4] = 0;
   out_5085878125767614964[5] = 0;
   out_5085878125767614964[6] = 0;
   out_5085878125767614964[7] = 0;
   out_5085878125767614964[8] = 0;
   out_5085878125767614964[9] = 0;
   out_5085878125767614964[10] = 1;
   out_5085878125767614964[11] = 0;
   out_5085878125767614964[12] = 0;
   out_5085878125767614964[13] = 0;
   out_5085878125767614964[14] = 0;
   out_5085878125767614964[15] = 0;
   out_5085878125767614964[16] = 0;
   out_5085878125767614964[17] = 0;
   out_5085878125767614964[18] = 0;
   out_5085878125767614964[19] = 0;
   out_5085878125767614964[20] = 1;
   out_5085878125767614964[21] = 0;
   out_5085878125767614964[22] = 0;
   out_5085878125767614964[23] = 0;
   out_5085878125767614964[24] = 0;
   out_5085878125767614964[25] = 0;
   out_5085878125767614964[26] = 0;
   out_5085878125767614964[27] = 0;
   out_5085878125767614964[28] = 0;
   out_5085878125767614964[29] = 0;
   out_5085878125767614964[30] = 1;
   out_5085878125767614964[31] = 0;
   out_5085878125767614964[32] = 0;
   out_5085878125767614964[33] = 0;
   out_5085878125767614964[34] = 0;
   out_5085878125767614964[35] = 0;
   out_5085878125767614964[36] = 0;
   out_5085878125767614964[37] = 0;
   out_5085878125767614964[38] = 0;
   out_5085878125767614964[39] = 0;
   out_5085878125767614964[40] = 1;
   out_5085878125767614964[41] = 0;
   out_5085878125767614964[42] = 0;
   out_5085878125767614964[43] = 0;
   out_5085878125767614964[44] = 0;
   out_5085878125767614964[45] = dt*(stiffness_front*(-state[2] - state[3] + state[7])/(mass*state[1]) + (-stiffness_front - stiffness_rear)*state[5]/(mass*state[4]) + (-center_to_front*stiffness_front + center_to_rear*stiffness_rear)*state[6]/(mass*state[4]));
   out_5085878125767614964[46] = -dt*stiffness_front*(-state[2] - state[3] + state[7])*state[0]/(mass*pow(state[1], 2));
   out_5085878125767614964[47] = -dt*stiffness_front*state[0]/(mass*state[1]);
   out_5085878125767614964[48] = -dt*stiffness_front*state[0]/(mass*state[1]);
   out_5085878125767614964[49] = dt*((-1 - (-center_to_front*stiffness_front*state[0] + center_to_rear*stiffness_rear*state[0])/(mass*pow(state[4], 2)))*state[6] - (-stiffness_front*state[0] - stiffness_rear*state[0])*state[5]/(mass*pow(state[4], 2)));
   out_5085878125767614964[50] = dt*(-stiffness_front*state[0] - stiffness_rear*state[0])/(mass*state[4]) + 1;
   out_5085878125767614964[51] = dt*(-state[4] + (-center_to_front*stiffness_front*state[0] + center_to_rear*stiffness_rear*state[0])/(mass*state[4]));
   out_5085878125767614964[52] = dt*stiffness_front*state[0]/(mass*state[1]);
   out_5085878125767614964[53] = -9.8000000000000007*dt;
   out_5085878125767614964[54] = dt*(center_to_front*stiffness_front*(-state[2] - state[3] + state[7])/(rotational_inertia*state[1]) + (-center_to_front*stiffness_front + center_to_rear*stiffness_rear)*state[5]/(rotational_inertia*state[4]) + (-pow(center_to_front, 2)*stiffness_front - pow(center_to_rear, 2)*stiffness_rear)*state[6]/(rotational_inertia*state[4]));
   out_5085878125767614964[55] = -center_to_front*dt*stiffness_front*(-state[2] - state[3] + state[7])*state[0]/(rotational_inertia*pow(state[1], 2));
   out_5085878125767614964[56] = -center_to_front*dt*stiffness_front*state[0]/(rotational_inertia*state[1]);
   out_5085878125767614964[57] = -center_to_front*dt*stiffness_front*state[0]/(rotational_inertia*state[1]);
   out_5085878125767614964[58] = dt*(-(-center_to_front*stiffness_front*state[0] + center_to_rear*stiffness_rear*state[0])*state[5]/(rotational_inertia*pow(state[4], 2)) - (-pow(center_to_front, 2)*stiffness_front*state[0] - pow(center_to_rear, 2)*stiffness_rear*state[0])*state[6]/(rotational_inertia*pow(state[4], 2)));
   out_5085878125767614964[59] = dt*(-center_to_front*stiffness_front*state[0] + center_to_rear*stiffness_rear*state[0])/(rotational_inertia*state[4]);
   out_5085878125767614964[60] = dt*(-pow(center_to_front, 2)*stiffness_front*state[0] - pow(center_to_rear, 2)*stiffness_rear*state[0])/(rotational_inertia*state[4]) + 1;
   out_5085878125767614964[61] = center_to_front*dt*stiffness_front*state[0]/(rotational_inertia*state[1]);
   out_5085878125767614964[62] = 0;
   out_5085878125767614964[63] = 0;
   out_5085878125767614964[64] = 0;
   out_5085878125767614964[65] = 0;
   out_5085878125767614964[66] = 0;
   out_5085878125767614964[67] = 0;
   out_5085878125767614964[68] = 0;
   out_5085878125767614964[69] = 0;
   out_5085878125767614964[70] = 1;
   out_5085878125767614964[71] = 0;
   out_5085878125767614964[72] = 0;
   out_5085878125767614964[73] = 0;
   out_5085878125767614964[74] = 0;
   out_5085878125767614964[75] = 0;
   out_5085878125767614964[76] = 0;
   out_5085878125767614964[77] = 0;
   out_5085878125767614964[78] = 0;
   out_5085878125767614964[79] = 0;
   out_5085878125767614964[80] = 1;
}
void h_25(double *state, double *unused, double *out_695354183343376158) {
   out_695354183343376158[0] = state[6];
}
void H_25(double *state, double *unused, double *out_4522013801845509539) {
   out_4522013801845509539[0] = 0;
   out_4522013801845509539[1] = 0;
   out_4522013801845509539[2] = 0;
   out_4522013801845509539[3] = 0;
   out_4522013801845509539[4] = 0;
   out_4522013801845509539[5] = 0;
   out_4522013801845509539[6] = 1;
   out_4522013801845509539[7] = 0;
   out_4522013801845509539[8] = 0;
}
void h_24(double *state, double *unused, double *out_8374737824769123930) {
   out_8374737824769123930[0] = state[4];
   out_8374737824769123930[1] = state[5];
}
void H_24(double *state, double *unused, double *out_6781126826017810538) {
   out_6781126826017810538[0] = 0;
   out_6781126826017810538[1] = 0;
   out_6781126826017810538[2] = 0;
   out_6781126826017810538[3] = 0;
   out_6781126826017810538[4] = 1;
   out_6781126826017810538[5] = 0;
   out_6781126826017810538[6] = 0;
   out_6781126826017810538[7] = 0;
   out_6781126826017810538[8] = 0;
   out_6781126826017810538[9] = 0;
   out_6781126826017810538[10] = 0;
   out_6781126826017810538[11] = 0;
   out_6781126826017810538[12] = 0;
   out_6781126826017810538[13] = 0;
   out_6781126826017810538[14] = 1;
   out_6781126826017810538[15] = 0;
   out_6781126826017810538[16] = 0;
   out_6781126826017810538[17] = 0;
}
void h_30(double *state, double *unused, double *out_4149887096770014231) {
   out_4149887096770014231[0] = state[4];
}
void H_30(double *state, double *unused, double *out_5682528282098659) {
   out_5682528282098659[0] = 0;
   out_5682528282098659[1] = 0;
   out_5682528282098659[2] = 0;
   out_5682528282098659[3] = 0;
   out_5682528282098659[4] = 1;
   out_5682528282098659[5] = 0;
   out_5682528282098659[6] = 0;
   out_5682528282098659[7] = 0;
   out_5682528282098659[8] = 0;
}
void h_26(double *state, double *unused, double *out_4907737241930833041) {
   out_4907737241930833041[0] = state[7];
}
void H_26(double *state, double *unused, double *out_780510482971453315) {
   out_780510482971453315[0] = 0;
   out_780510482971453315[1] = 0;
   out_780510482971453315[2] = 0;
   out_780510482971453315[3] = 0;
   out_780510482971453315[4] = 0;
   out_780510482971453315[5] = 0;
   out_780510482971453315[6] = 0;
   out_780510482971453315[7] = 1;
   out_780510482971453315[8] = 0;
}
void h_27(double *state, double *unused, double *out_1677438276678674270) {
   out_1677438276678674270[0] = state[3];
}
void H_27(double *state, double *unused, double *out_2180445840082523570) {
   out_2180445840082523570[0] = 0;
   out_2180445840082523570[1] = 0;
   out_2180445840082523570[2] = 0;
   out_2180445840082523570[3] = 1;
   out_2180445840082523570[4] = 0;
   out_2180445840082523570[5] = 0;
   out_2180445840082523570[6] = 0;
   out_2180445840082523570[7] = 0;
   out_2180445840082523570[8] = 0;
}
void h_29(double *state, double *unused, double *out_8888033146276828161) {
   out_8888033146276828161[0] = state[1];
}
void H_29(double *state, double *unused, double *out_504548816032293525) {
   out_504548816032293525[0] = 0;
   out_504548816032293525[1] = 1;
   out_504548816032293525[2] = 0;
   out_504548816032293525[3] = 0;
   out_504548816032293525[4] = 0;
   out_504548816032293525[5] = 0;
   out_504548816032293525[6] = 0;
   out_504548816032293525[7] = 0;
   out_504548816032293525[8] = 0;
}
void h_28(double *state, double *unused, double *out_2280754161355151787) {
   out_2280754161355151787[0] = state[0];
}
void H_28(double *state, double *unused, double *out_2468179087597619776) {
   out_2468179087597619776[0] = 1;
   out_2468179087597619776[1] = 0;
   out_2468179087597619776[2] = 0;
   out_2468179087597619776[3] = 0;
   out_2468179087597619776[4] = 0;
   out_2468179087597619776[5] = 0;
   out_2468179087597619776[6] = 0;
   out_2468179087597619776[7] = 0;
   out_2468179087597619776[8] = 0;
}
void h_31(double *state, double *unused, double *out_7185918467410673027) {
   out_7185918467410673027[0] = state[8];
}
void H_31(double *state, double *unused, double *out_154302380738101839) {
   out_154302380738101839[0] = 0;
   out_154302380738101839[1] = 0;
   out_154302380738101839[2] = 0;
   out_154302380738101839[3] = 0;
   out_154302380738101839[4] = 0;
   out_154302380738101839[5] = 0;
   out_154302380738101839[6] = 0;
   out_154302380738101839[7] = 0;
   out_154302380738101839[8] = 1;
}
#include <eigen3/Eigen/Dense>
#include <iostream>

typedef Eigen::Matrix<double, DIM, DIM, Eigen::RowMajor> DDM;
typedef Eigen::Matrix<double, EDIM, EDIM, Eigen::RowMajor> EEM;
typedef Eigen::Matrix<double, DIM, EDIM, Eigen::RowMajor> DEM;

void predict(double *in_x, double *in_P, double *in_Q, double dt) {
  typedef Eigen::Matrix<double, MEDIM, MEDIM, Eigen::RowMajor> RRM;

  double nx[DIM] = {0};
  double in_F[EDIM*EDIM] = {0};

  // functions from sympy
  f_fun(in_x, dt, nx);
  F_fun(in_x, dt, in_F);


  EEM F(in_F);
  EEM P(in_P);
  EEM Q(in_Q);

  RRM F_main = F.topLeftCorner(MEDIM, MEDIM);
  P.topLeftCorner(MEDIM, MEDIM) = (F_main * P.topLeftCorner(MEDIM, MEDIM)) * F_main.transpose();
  P.topRightCorner(MEDIM, EDIM - MEDIM) = F_main * P.topRightCorner(MEDIM, EDIM - MEDIM);
  P.bottomLeftCorner(EDIM - MEDIM, MEDIM) = P.bottomLeftCorner(EDIM - MEDIM, MEDIM) * F_main.transpose();

  P = P + dt*Q;

  // copy out state
  memcpy(in_x, nx, DIM * sizeof(double));
  memcpy(in_P, P.data(), EDIM * EDIM * sizeof(double));
}

// note: extra_args dim only correct when null space projecting
// otherwise 1
template <int ZDIM, int EADIM, bool MAHA_TEST>
void update(double *in_x, double *in_P, Hfun h_fun, Hfun H_fun, Hfun Hea_fun, double *in_z, double *in_R, double *in_ea, double MAHA_THRESHOLD) {
  typedef Eigen::Matrix<double, ZDIM, ZDIM, Eigen::RowMajor> ZZM;
  typedef Eigen::Matrix<double, ZDIM, DIM, Eigen::RowMajor> ZDM;
  typedef Eigen::Matrix<double, Eigen::Dynamic, EDIM, Eigen::RowMajor> XEM;
  //typedef Eigen::Matrix<double, EDIM, ZDIM, Eigen::RowMajor> EZM;
  typedef Eigen::Matrix<double, Eigen::Dynamic, 1> X1M;
  typedef Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> XXM;

  double in_hx[ZDIM] = {0};
  double in_H[ZDIM * DIM] = {0};
  double in_H_mod[EDIM * DIM] = {0};
  double delta_x[EDIM] = {0};
  double x_new[DIM] = {0};


  // state x, P
  Eigen::Matrix<double, ZDIM, 1> z(in_z);
  EEM P(in_P);
  ZZM pre_R(in_R);

  // functions from sympy
  h_fun(in_x, in_ea, in_hx);
  H_fun(in_x, in_ea, in_H);
  ZDM pre_H(in_H);

  // get y (y = z - hx)
  Eigen::Matrix<double, ZDIM, 1> pre_y(in_hx); pre_y = z - pre_y;
  X1M y; XXM H; XXM R;
  if (Hea_fun){
    typedef Eigen::Matrix<double, ZDIM, EADIM, Eigen::RowMajor> ZAM;
    double in_Hea[ZDIM * EADIM] = {0};
    Hea_fun(in_x, in_ea, in_Hea);
    ZAM Hea(in_Hea);
    XXM A = Hea.transpose().fullPivLu().kernel();


    y = A.transpose() * pre_y;
    H = A.transpose() * pre_H;
    R = A.transpose() * pre_R * A;
  } else {
    y = pre_y;
    H = pre_H;
    R = pre_R;
  }
  // get modified H
  H_mod_fun(in_x, in_H_mod);
  DEM H_mod(in_H_mod);
  XEM H_err = H * H_mod;

  // Do mahalobis distance test
  if (MAHA_TEST){
    XXM a = (H_err * P * H_err.transpose() + R).inverse();
    double maha_dist = y.transpose() * a * y;
    if (maha_dist > MAHA_THRESHOLD){
      R = 1.0e16 * R;
    }
  }

  // Outlier resilient weighting
  double weight = 1;//(1.5)/(1 + y.squaredNorm()/R.sum());

  // kalman gains and I_KH
  XXM S = ((H_err * P) * H_err.transpose()) + R/weight;
  XEM KT = S.fullPivLu().solve(H_err * P.transpose());
  //EZM K = KT.transpose(); TODO: WHY DOES THIS NOT COMPILE?
  //EZM K = S.fullPivLu().solve(H_err * P.transpose()).transpose();
  //std::cout << "Here is the matrix rot:\n" << K << std::endl;
  EEM I_KH = Eigen::Matrix<double, EDIM, EDIM>::Identity() - (KT.transpose() * H_err);

  // update state by injecting dx
  Eigen::Matrix<double, EDIM, 1> dx(delta_x);
  dx  = (KT.transpose() * y);
  memcpy(delta_x, dx.data(), EDIM * sizeof(double));
  err_fun(in_x, delta_x, x_new);
  Eigen::Matrix<double, DIM, 1> x(x_new);

  // update cov
  P = ((I_KH * P) * I_KH.transpose()) + ((KT.transpose() * R) * KT);

  // copy out state
  memcpy(in_x, x.data(), DIM * sizeof(double));
  memcpy(in_P, P.data(), EDIM * EDIM * sizeof(double));
  memcpy(in_z, y.data(), y.rows() * sizeof(double));
}




}
extern "C" {

void car_update_25(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea) {
  update<1, 3, 0>(in_x, in_P, h_25, H_25, NULL, in_z, in_R, in_ea, MAHA_THRESH_25);
}
void car_update_24(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea) {
  update<2, 3, 0>(in_x, in_P, h_24, H_24, NULL, in_z, in_R, in_ea, MAHA_THRESH_24);
}
void car_update_30(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea) {
  update<1, 3, 0>(in_x, in_P, h_30, H_30, NULL, in_z, in_R, in_ea, MAHA_THRESH_30);
}
void car_update_26(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea) {
  update<1, 3, 0>(in_x, in_P, h_26, H_26, NULL, in_z, in_R, in_ea, MAHA_THRESH_26);
}
void car_update_27(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea) {
  update<1, 3, 0>(in_x, in_P, h_27, H_27, NULL, in_z, in_R, in_ea, MAHA_THRESH_27);
}
void car_update_29(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea) {
  update<1, 3, 0>(in_x, in_P, h_29, H_29, NULL, in_z, in_R, in_ea, MAHA_THRESH_29);
}
void car_update_28(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea) {
  update<1, 3, 0>(in_x, in_P, h_28, H_28, NULL, in_z, in_R, in_ea, MAHA_THRESH_28);
}
void car_update_31(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea) {
  update<1, 3, 0>(in_x, in_P, h_31, H_31, NULL, in_z, in_R, in_ea, MAHA_THRESH_31);
}
void car_err_fun(double *nom_x, double *delta_x, double *out_709253069857813121) {
  err_fun(nom_x, delta_x, out_709253069857813121);
}
void car_inv_err_fun(double *nom_x, double *true_x, double *out_5721921606894944173) {
  inv_err_fun(nom_x, true_x, out_5721921606894944173);
}
void car_H_mod_fun(double *state, double *out_1388721326752473306) {
  H_mod_fun(state, out_1388721326752473306);
}
void car_f_fun(double *state, double dt, double *out_3586979400707933995) {
  f_fun(state,  dt, out_3586979400707933995);
}
void car_F_fun(double *state, double dt, double *out_5085878125767614964) {
  F_fun(state,  dt, out_5085878125767614964);
}
void car_h_25(double *state, double *unused, double *out_695354183343376158) {
  h_25(state, unused, out_695354183343376158);
}
void car_H_25(double *state, double *unused, double *out_4522013801845509539) {
  H_25(state, unused, out_4522013801845509539);
}
void car_h_24(double *state, double *unused, double *out_8374737824769123930) {
  h_24(state, unused, out_8374737824769123930);
}
void car_H_24(double *state, double *unused, double *out_6781126826017810538) {
  H_24(state, unused, out_6781126826017810538);
}
void car_h_30(double *state, double *unused, double *out_4149887096770014231) {
  h_30(state, unused, out_4149887096770014231);
}
void car_H_30(double *state, double *unused, double *out_5682528282098659) {
  H_30(state, unused, out_5682528282098659);
}
void car_h_26(double *state, double *unused, double *out_4907737241930833041) {
  h_26(state, unused, out_4907737241930833041);
}
void car_H_26(double *state, double *unused, double *out_780510482971453315) {
  H_26(state, unused, out_780510482971453315);
}
void car_h_27(double *state, double *unused, double *out_1677438276678674270) {
  h_27(state, unused, out_1677438276678674270);
}
void car_H_27(double *state, double *unused, double *out_2180445840082523570) {
  H_27(state, unused, out_2180445840082523570);
}
void car_h_29(double *state, double *unused, double *out_8888033146276828161) {
  h_29(state, unused, out_8888033146276828161);
}
void car_H_29(double *state, double *unused, double *out_504548816032293525) {
  H_29(state, unused, out_504548816032293525);
}
void car_h_28(double *state, double *unused, double *out_2280754161355151787) {
  h_28(state, unused, out_2280754161355151787);
}
void car_H_28(double *state, double *unused, double *out_2468179087597619776) {
  H_28(state, unused, out_2468179087597619776);
}
void car_h_31(double *state, double *unused, double *out_7185918467410673027) {
  h_31(state, unused, out_7185918467410673027);
}
void car_H_31(double *state, double *unused, double *out_154302380738101839) {
  H_31(state, unused, out_154302380738101839);
}
void car_predict(double *in_x, double *in_P, double *in_Q, double dt) {
  predict(in_x, in_P, in_Q, dt);
}
void car_set_mass(double x) {
  set_mass(x);
}
void car_set_rotational_inertia(double x) {
  set_rotational_inertia(x);
}
void car_set_center_to_front(double x) {
  set_center_to_front(x);
}
void car_set_center_to_rear(double x) {
  set_center_to_rear(x);
}
void car_set_stiffness_front(double x) {
  set_stiffness_front(x);
}
void car_set_stiffness_rear(double x) {
  set_stiffness_rear(x);
}
}

const EKF car = {
  .name = "car",
  .kinds = { 25, 24, 30, 26, 27, 29, 28, 31 },
  .feature_kinds = {  },
  .f_fun = car_f_fun,
  .F_fun = car_F_fun,
  .err_fun = car_err_fun,
  .inv_err_fun = car_inv_err_fun,
  .H_mod_fun = car_H_mod_fun,
  .predict = car_predict,
  .hs = {
    { 25, car_h_25 },
    { 24, car_h_24 },
    { 30, car_h_30 },
    { 26, car_h_26 },
    { 27, car_h_27 },
    { 29, car_h_29 },
    { 28, car_h_28 },
    { 31, car_h_31 },
  },
  .Hs = {
    { 25, car_H_25 },
    { 24, car_H_24 },
    { 30, car_H_30 },
    { 26, car_H_26 },
    { 27, car_H_27 },
    { 29, car_H_29 },
    { 28, car_H_28 },
    { 31, car_H_31 },
  },
  .updates = {
    { 25, car_update_25 },
    { 24, car_update_24 },
    { 30, car_update_30 },
    { 26, car_update_26 },
    { 27, car_update_27 },
    { 29, car_update_29 },
    { 28, car_update_28 },
    { 31, car_update_31 },
  },
  .Hes = {
  },
  .sets = {
    { "mass", car_set_mass },
    { "rotational_inertia", car_set_rotational_inertia },
    { "center_to_front", car_set_center_to_front },
    { "center_to_rear", car_set_center_to_rear },
    { "stiffness_front", car_set_stiffness_front },
    { "stiffness_rear", car_set_stiffness_rear },
  },
  .extra_routines = {
  },
};

ekf_lib_init(car)
