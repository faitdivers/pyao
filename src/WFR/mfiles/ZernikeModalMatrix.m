function[Z,Zsparse]=ZernikeModalMatrix(N, lambda)
% This function compute the Zernike Derivative Modal Matrix to be used in a
% modal integration to reconstruct the wavefront from the gradient
% measurement. The only necessary input is the length of the data point
% that is the max number of spot in one direction
%
% latest update 1/6/2011
% written by Alessandro Polo

%% domain definition
gridx   = linspace(-1,1,N);
[x,y]   = meshgrid(gridx,gridx);
r   =sqrt( x.^2+y.^2);

A   = zeros(N); % Initialize       
idx=r<1;
A(idx)=lambda;
%%  Building the Modal Matrix
% X derivative
dzx1=0.*A;

dzx2=2.*A;
dzx3=0.*A;

dzx4= sqrt(6)*2.*x.*A;
dzx5=sqrt(3)* 4.*x.*A;
dzx6=sqrt(6)*2.*y.*A;

dzx7=sqrt(8)*(3.*x.^2-3.*y.^2).*A;
dzx8=sqrt(8)*(9.*x.^2+3.*y.^2-2).*A;
dzx9=sqrt(8)*6.*x.*y.*A;
dzx10=sqrt(8)*6.*x.*y.*A;

dzx11=sqrt(10)*(4.*x.^3-12.*x.*y.^2).*A;
dzx12=sqrt(10)*(16.*x.^3-6.*x).*A;
dzx13=sqrt(5)*(24.*x.^3+24.*x.*y.^2-12.*x).*A;
dzx14=sqrt(10)*(24.*x.^2.*y+8.*y.^3-6.*y).*A;
dzx15=sqrt(10)*(12.*x.^2.*y-4.*y.^3).*A;

dzx16=sqrt(12)*(5.*x.^4-30.*x.^2.*y.^2+5.*y.^4).*A;
dzx17=sqrt(12)*(25.*x.^4-30.*x.^2.*y.^2-15.*y.^4-12.*x.^2+12.*y.^2).*A;
dzx18=sqrt(12)*(50.*x.^4+60.*x.^2.*y.^2+10.*y.^4-36.*x.^2-12.*y.^2+3).*A;
dzx19=sqrt(12)*(40.*x.^3.*y+40.*x.*y.^3-24.*x.*y).*A;
dzx20=sqrt(12)*(60.*x.^3.*y+20.*x.*y.^3-24.*x.*y).*A;
dzx21=sqrt(12)*(20.*x.^3.*y-20.*x.*y.^3).*A;

dzx22=sqrt(14)*(6.*x.^5-60.*x.^3.*y.^2+30.*x.*y.^4).*A;
dzx23=sqrt(14)*(36.*x.^5-120.*x.^3.*y.^2-60.*x.*y.^4-20.*x.^3+60.*x.*y.^2).*A;
dzx24=sqrt(14)*(90.*x.^5+60.*x.^3.*y.^2-30.*x.*y.^4-80.*x.^3+12.*x).*A;
dzx25=sqrt(7)*(120.*x.^5+240.*x.^3.*y.^2+120.*x.*y.^4-120.*x.^3-120.*x.*y.^2+24.*x).*A;
dzx26=sqrt(14)*(150.*x.^4.*y+180.*x.^2.*y.^3+30.*y.^5-120.*x.^2.*y-40.*y.^3+12.*y).*A;
dzx27=sqrt(14)*(120.*x.^4.*y-24.*y.^5-60.*x.^2.*y+20.*y.^3).*A;
dzx28=sqrt(14)*(30.*x.^4.*y-60.*x.^2.*y.^3+6.*y.^5).*A;

dzx29=4*(7.*x.^6-105.*x.^4.*y.^2+105.*x.^2.*y.^4-7.*y.^6).*A;
dzx30=4*(49.*x.^6-315.*x.^4.*y.^2-105.*x.^2.*y.^4+35.*y.^6-30.*x.^4+180.*x.^2.*y.^2-30.*y.^4).*A;
dzx31=4*(147.*x.^6-105.*x.^4.*y.^2-315.*x.^2.*y.^4-63.*y.^6-150.*x.^4+180.*x.^2.*y.^2+90.*y.^4+30.*x.^2-30.*y.^2).*A;
dzx32=4*(245.*x.^6+525.*x.^4.*y.^2+315.*x.^2.*y.^4+35.*y.^6-300.*x.^4-360.*x.^2.*y.^2-60.*y.^4+90.*x.^2+30.*y.^2-4).*A;
dzx33=4*(210.*x.^5.*y+420.*x.^3.*y.^3+210.*x.*y.^5-240.*x.^3.*y-240.*x.*y.^3+60.*x.*y).*A;
dzx34=4*(378.*x.^5.*y+420.*x.^3.*y.^3+42.*x.*y.^5-360.*x.^3.*y-120.*x.*y.^3+60.*x.*y).*A;
dzx35=4*(210.*x.^5.*y-140.*x.^3.*y.^3-126.*x.*y.^5-120.*x.^3.*y+120.*x.*y.^3).*A;
dzx36=4*(42.*x.^5.*y-140.*x.^3.*y.^3+42.*x.*y.^5).*A;

DZX=[dzx1(:)' ;  dzx2(:)' ;   dzx3(:)'   ;     dzx4(:)'   ;   dzx5(:)'   ;     dzx6(:)'  ;
   dzx7(:)' ;      dzx8(:)'  ;   dzx9(:)'  ;     dzx10(:)'  ;  dzx11(:)'  ;    dzx12(:)' ;
   dzx13(:)'  ;    dzx14(:)'  ; dzx15(:)'  ;    dzx16(:)'  ;  dzx17(:)'  ;    dzx18(:)'  ;
   dzx19(:)'  ;    dzx20(:)'  ; dzx21(:)'  ;    dzx22(:)'  ;  dzx23(:)'  ;    dzx24(:)'  ;
   dzx25(:)'  ;    dzx26(:)'  ; dzx27(:)' ;    dzx28(:)'  ;  dzx29(:)'  ;    dzx30(:)'  ;
   dzx31(:)'  ;    dzx32(:)'  ; dzx33(:)'  ;    dzx34(:)'  ;  dzx35(:)'  ;    dzx36(:)' ]';


% Y derivative
dzy1= 0.*A;
dzy2= 0.*A;
dzy3= 2.*A;

dzy4= sqrt(6)*(-2.*y.*A);
dzy5=sqrt(3)*4.*y.*A;
dzy6=sqrt(6)* 2.*x.*A;

dzy7=sqrt(8)*(-6.*x.*y.*A);
dzy8=sqrt(8)*(6.*x.*y.*A);
dzy9=sqrt(8)*(3.*x.^2+9.*y.^2-2).*A;
dzy10=sqrt(8)*(3.*x.^2-3.*y.^2).*A;

dzy11=sqrt(10)*(-12.*x.^2.*y+4.*y.^3).*A;
dzy12=sqrt(10)*(-16.*y.^3+6.*y).*A;
dzy13=sqrt(5)*(24.*x.^2.*y+24.*y.^3-12.*y).*A;
dzy14=sqrt(10)*(8.*x.^3+24.*x.*y.^2-6.*x).*A;
dzy15=sqrt(10)*(4.*x.^3-12.*x.*y.^2).*A;

dzy16=sqrt(12)*(-20.*x.^3.*y+20.*x.*y.^3).*A;
dzy17=sqrt(12)*(-20.*x.^3.*y-60.*x.*y.^3+24.*x.*y).*A;
dzy18=sqrt(12)*(40.*x.^3.*y+40.*x.*y.^3-24.*x.*y).*A;
dzy19=sqrt(12)*(10.*x.^4+60.*x.^2.*y.^2+50.*y.^4-12.*x.^2-36.*y.^2+3).*A;
dzy20=sqrt(12)*(15.*x.^4+30.*x.^2.*y.^2-25.*y.^4-12.*x.^2+12.*y.^2).*A;
dzy21=sqrt(12)*(5.*x.^4-30.*x.^2.*y.^2+5.*y.^4).*A;

dzy22=sqrt(14)*(-30.*x.^4.*y+60.*x.^2.*y.^3-6.*y.^5).*A;
dzy23=sqrt(14)*(-60.*x.^4.*y-120.*x.^2.*y.^3+36.*y.^5+60.*x.^2.*y-20.*y.^3).*A;
dzy24=sqrt(14)*(30.*x.^4.*y-60.*x.^2.*y.^3-90.*y.^5+80.*y.^3-12.*y).*A;
dzy25=sqrt(7)*(120.*x.^4.*y+240.*x.^2.*y.^3+120.*y.^5-120.*x.^2.*y-120.*y.^3+24.*y).*A;
dzy26=sqrt(14)*(30.*x.^5+180.*x.^3.*y.^2+150.*x.*y.^4-40.*x.^3-120.*x.*y.^2+12.*x).*A;
dzy27=sqrt(14)*(24.*x.^5-120.*x.*y.^4-20.*x.^3+60.*x.*y.^2).*A;
dzy28=sqrt(14)*(6.*x.^5-60.*x.^3.*y.^2+30.*x.*y.^4).*A;

dzy29=4*(-42.*x.^5.*y+140.*x.^3.*y.^3-42.*x.*y.^5).*A;
dzy30=4*(-126.*x.^5.*y-140.*x.^3.*y.^3+210.*x.*y.^5+120.*x.^3.*y-120.*x.*y.^3).*A;
dzy31=4*(-42.*x.^5.*y-420.*x.^3.*y.^3-378.*x.*y.^5+120.*x.^3.*y+360.*x.*y.^3-60.*x.*y).*A;
dzy32=4*(210.*x.^5.*y+420.*x.^3.*y.^3+210.*x.*y.^5-240.*x.^3.*y-240.*x.*y.^3+60.*x.*y).*A;
dzy33=4*(35.*x.^6+315.*x.^4.*y.^2+525.*x.^2.*y.^4+245.*y.^6-60.*x.^4-360.*x.^2.*y.^2-300.*y.^4+30.*x.^2+90.*y.^2-4).*A;
dzy34=4*(63.*x.^6+315.*x.^4.*y.^2+105.*x.^2.*y.^4-147.*y.^6-90.*x.^4-180.*x.^2.*y.^2+150.*y.^4+30.*x.^2-30.*y.^2).*A;
dzy35=4*(35.*x.^6-105.*x.^4.*y.^2-315.*x.^2.*y.^4+49.*y.^6-30.*x.^4+180.*x.^2.*y.^2-30.*y.^4).*A;
dzy36=4*(7.*x.^6-105.*x.^4.*y.^2+105.*x.^2.*y.^4-7.*y.^6).*A;

DZY=[dzy1(:)' ;  dzy2(:)' ;   dzy3(:)'   ;     dzy4(:)'   ;   dzy5(:)'   ;     dzy6(:)'  ;
   dzy7(:)' ;      dzy8(:)'  ;   dzy9(:)'  ;     dzy10(:)'  ;  dzy11(:)'  ;    dzy12(:)' ;
   dzy13(:)'  ;    dzy14(:)'  ; dzy15(:)'  ;    dzy16(:)'  ;  dzy17(:)'  ;    dzy18(:)'  ;
   dzy19(:)'  ;    dzy20(:)'  ; dzy21(:)'  ;    dzy22(:)'  ;  dzy23(:)'  ;    dzy24(:)'  ;
   dzy25(:)'  ;    dzy26(:)'  ; dzy27(:)' ;    dzy28(:)'  ;  dzy29(:)'  ;    dzy30(:)'  ;
   dzy31(:)'  ;    dzy32(:)'  ; dzy33(:)'  ;    dzy34(:)'  ;  dzy35(:)'  ;    dzy36(:)' ]';

%% Building the matrix
%Modal Matrix
Z=ones(2*N*N,36);
pp=1;
for ii=1:2:2*N*N
    Z(ii,:)=DZX(pp,:);
    Z(ii+1,:)=DZY(pp,:);
    pp=pp+1;
end

Zsparse=sparse(Z);
