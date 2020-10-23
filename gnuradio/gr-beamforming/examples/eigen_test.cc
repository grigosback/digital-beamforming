#include <eigen3/Eigen/Core>
#include <eigen3/Eigen/SVD>
#include <eigen3/Eigen/Dense>
#include <complex>
#include <iostream>

using namespace Eigen;
using namespace std::literals;

int main()
{
    /*Eigen::MatrixXcf m(2, 2);
    m << 1.0f + 2.0if, 2.0f + 1.0if, 3.0f - 1.0if, 4.0f - 2.0if;
    std::std::cout << m << std::std::endl;*/

    /*MatrixXcf C;
    C.setRandom(27, 18);
    JacobiSVD<MatrixXd> svd(C, ComputeThinU | ComputeThinV);
    MatrixXd Cp = svd.matrixU() * svd.singularValues().asDiagonal() * svd.matrixV().transpose();
    MatrixXd diff = Cp - C;
    std::cout << "diff:\n"
         << diff.array().abs().sum() << "\n";*/

    MatrixXcf m = MatrixXcf::Random(3, 2);
    std::cout << "Here is the matrix m:" << std::endl
              << m << std::endl;
    JacobiSVD<MatrixXcf> svd(m, ComputeThinU | ComputeThinV);
    std::cout << "Its singular values are:" << std::endl
              << svd.singularValues() << std::endl;
    std::cout << "Its left singular vectors are the columns of the thin U matrix:" << std::endl
              << svd.matrixU() << std::endl;
    std::cout << "Its right singular vectors are the columns of the thin V matrix:" << std::endl
              << svd.matrixV() << std::endl;
    Vector3f rhs(1, 0, 0);
    std::cout << "Now consider this rhs vector:" << std::endl
              << rhs << std::endl;
    std::cout << "A least-squares solution of m*x = rhs is:" << std::endl
              << svd.solve(rhs) << std::endl;
    return 0;
}