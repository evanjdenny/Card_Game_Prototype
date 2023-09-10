#include <iostream>
#include <string>
using namespace std;

class Base {
private:
    int value;
    string name;
public:
    Base(int value, string name) : value(value), name(name) {
        cout << "Value: " << this->value << endl;
        cout << "Name: " << this->name << endl;
    }
};

int main() {
    Base evan = Base(25, "Evan Denny");
}