clear all;

N = 4;

omega_1 = pi/7;
omega_2 = pi/3;
phi_1 = 4.3*pi;
phi_2 = 2.11*pi;
alpha_1 = 3;
alpha_2 = 5;
var_V = 0.15;
sigma = sqrt(var_V);

A_1 = alpha_1 * cos(phi_1);
A_2 = alpha_2 * cos(phi_2);
B_1 = -alpha_1 * sin(phi_1);
B_2 = -alpha_2 * sin(phi_2);

% Matriz S(vector_omega)
S = zeros(N, 4);
S(1,:) = [1, 1, 0, 0];
for n = 2:N
    S(n,:) = [cos((n-1)*omega_1), cos((n-1)*omega_2), sin((n-1)*omega_1), sin((n-1)*omega_2)];
end

% Random vector V
V = zeros(N, 1);
V = normrnd(0, sigma, [N,1]);

% Random vector Z
Z = zeros(N, 1);
for n = 1:N
    Z(n) = A_1 * cos(omega_1*n) + A_2 * cos(omega_2*n) + B_1 * sin(omega_1*n) + B_2 * sin(omega_2*n) + V(n);
end

% Matriz J
Omega_1 = pi/7-3 : 0.1 : pi/7+3;
Omega_2 = pi/3-3 : 0.1 : pi/3+3;
[O1, O2] = meshgrid(pi/7-1 : 0.1 : pi/7+1, pi*1.82-1 : 0.1 : pi*1.82+1);
mat_J = zeros(length(Omega_1), length(Omega_2));
for i = 1:length(Omega_1)
    for j = 1:length(Omega_2)
        o1 = Omega_1(1,i);
        o2 = Omega_2(1,j);
        mat_J(i, j) = fun_J(Z, o1, o2);
    end
end

surf(mat_J);

% Función J
function J = fun_J(Z, omega_1, omega_2)
    N = length(Z);
    
    % Defino S
    S = zeros(N, 4);
    for n = 1:N
        S(n,:) = [cos((n-1)*omega_1), cos((n-1)*omega_2), sin((n-1)*omega_1), sin((n-1)*omega_2)];
    end
    
    J = (Z') * S * inv((S')*S) * S' *Z;
end