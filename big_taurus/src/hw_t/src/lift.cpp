#include "lift_control.h"
#include <iostream>
#include <unistd.h>

int main()
{
    Moons lift;

    if (!lift.isConnected())
        return -1;

    int slave = 3;

    // SAFE slow speed (jog)
    lift.setLiftSpeed(slave, 300);

    std::cout << "\nLift Control\n";
    std::cout << "1 : Lift UP (jog)\n";
    std::cout << "2 : Lift DOWN (jog)\n";
    std::cout << "3 : STOP\n";
    std::cout << "4 : ZERO encoder\n";
    std::cout << "5 : Move to POSITION\n";
    std::cout << "q : Quit\n\n";

    char cmd;
    while (true)
    {
        std::cout << "Enter command: ";
        std::cin >> cmd;

        if (cmd == '1')
        {
            lift.liftUp(slave);
        }
        else if (cmd == '8'){
            while (true){
                sleep(2);
                lift.liftUp(slave);
                sleep(40);
                lift.stopLift(slave);
                sleep(2);
                lift.liftDown(slave);

                sleep(40);
                lift.stopLift(slave);
            }
        }
        else if (cmd == '2')
        {
            lift.liftDown(slave);
        }
        else if (cmd == '3')
        {
            lift.stopLift(slave);
            lift.readAlarm(slave);
            lift.getencoder(slave);
            lift.resetAlarm(slave);
        }
        else if (cmd == '4')
        {
            lift.stopLift(slave);          // safety
            sleep(1);
            lift.zeroEncoder(slave);       // 👈 encoder = 0
        }
        else if (cmd == '5')
        {
            int32_t pos, speed;
            std::cout << "Enter target position: ";
            std::cin >> pos;
            std::cout << "Enter speed: ";
            std::cin >> speed;

            sleep(1);
            lift.setPosition(slave, pos, speed);
        }
        else if (cmd == 'q' || cmd == 'Q')
        {
            lift.stopLift(slave);          // SAFETY STOP
            break;
        }
        else
        {
            std::cout << "Invalid command\n";
        }

        // Status feedback
        int32_t pos = lift.getLiftPosition(slave);
        std::cout << "Lift position: " << pos << std::endl;

        lift.readAlarm(slave);
    }

    std::cout << "Exiting lift control\n";
    return 0;
}//g++ lift.cpp lift_function.cpp -o lift -lmodbus -std=c++11
