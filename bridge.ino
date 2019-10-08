#include <Keyboard.h>

void setup()
{
    Serial1.begin(9600);
}

void loop()
{
    char ch;

    while ((ch = Serial1.read()) != -1) {
      Keyboard.print(ch);
    }
}

