// shuffle algorithm example
#include <iostream>  // std::cout
#include <algorithm> // std::shuffle
#include <array>     // std::array
#include <random>    // std::default_random_engine
#include <chrono>    // std::chrono::system_clock

unsigned seed = 42;

int main()
{
    int len = 20;
    //std::array<int, len> d_idx;

    std::vector<int> d_idx;
    for (int i = 0; i < len; i++)
    {
        d_idx.push_back(i);
    }

    shuffle(d_idx.begin(), d_idx.end(), std::default_random_engine(seed));

    std::cout << "shuffled elements:";
    for (int &x : d_idx)
        std::cout << ' ' << x;
    std::cout << '\n';

    return 0;
}