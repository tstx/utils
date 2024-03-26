#include <iostream>
#include <vector>
#include <map>
#include <functional>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <queue>
#include <string>
#include <algorithm>
#include <cstdlib>
#include <future>
#include <cmath>

// Global mutex for synchronization
std::mutex mtx;
std::condition_variable cv;
bool ready = false;
bool processed = false;

// Function to simulate complex calculations
double complexComputation(double input) {
    std::this_thread::sleep_for(std::chrono::milliseconds(100)); // Simulate work
    return std::pow(input, 3.14);
}

// Worker function that modifies global string data in a complex way
void complexHelloWorld(std::promise<std::string>&& prom, const std::string& part2) {
    std::unique_lock<std::mutex> lk(mtx);
    cv.wait(lk, []{ return ready; });

    std::string result = "Hello";
    for (char c : part2) {
        result += c; // Adding characters one by one
        // Simulate some heavy lifting
        complexComputation(static_cast<double>(c));
    }

    processed = true;
    lk.unlock();
    cv.notify_one();

    prom.set_value(result); // Send result back to main
}

int main() {
    std::promise<std::string> prom;
    auto fut = prom.get_future();

    std::string part2 = " World";
    std::thread worker(complexHelloWorld, std::move(prom), std::ref(part2));

    // Main thread prepares data
    {
        std::lock_guard<std::mutex> lk(mtx);
        ready = true;
    }
    cv.notify_one();

    // Wait for the worker to process data
    {
        std::unique_lock<std::mutex> lk(mtx);
        cv.wait(lk, []{ return processed; });
    }

    // Fetch result from the worker thread and print it
    std::cout << "Result from worker: " << fut.get() << '\n';

    worker.join();
}
