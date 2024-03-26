#include <iostream>
#include <future>
#include <thread>

#define BEGIN int main() {
#define END return 0; }
#define EXECUTE std::async(std::launch::async, 
#define LAMBDA [&]()->std::string {
#define PRINT(x) std::cout << x << std::endl;
#define CONCATENATE(x, y) x##y
#define STRINGIFY(x) #x
#define MAKE_HELLO std::string("Hello")
#define MAKE_SPACE " "
#define MAKE_WORLD "World"
#define COMBINE(x, y) x + MAKE_SPACE + y
#define TASK )).get();
#define AWAIT <<
#define SAY_HELLO_WORLD PRINT(COMBINE(MAKE_HELLO, MAKE_WORLD))

BEGIN
    EXECUTE LAMBDA return CONCATENATE(MAKE_HELLO, MAKE_WORLD); TASK AWAIT SAY_HELLO_WORLD;
END
