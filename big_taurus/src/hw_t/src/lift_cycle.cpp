// #include "lift_control.h"
// #include <iostream>
// #include <unistd.h>

// int main()
// {
//     Moons lift;

//     if (!lift.isConnected())
//         return -1;

//     int slave = 3;

//     // SAFE slow speed (set once)
//     lift.setLiftSpeed(slave, 300);

//     std::cout << "\nLift Control\n";
//     std::cout << "1 : Lift UP\n";
//     std::cout << "2 : Lift DOWN\n";
//     std::cout << "3 : STOP\n";
//     std::cout << "q : Quit\n\n";

//     char cmd;
//     while (true)
//     {
//         std::cout << "Enter command: ";
//         std::cin >> cmd;

//         if (cmd == '1')
//         {
//             lift.liftUp(slave);
//         }
//         else if (cmd == '2')
//         {
//             lift.liftDown(slave);
//         }
//         else if (cmd == '3')
//         {   lift.readAlarm(slave);
//             lift.stopLift(slave);
//             lift.resetAlarm(slave);
//         }
//         else if (cmd == 'q' || cmd == 'Q')
//         {
//             lift.stopLift(slave);  // SAFETY STOP before exit
//             break;
//         }
//         else
//         {
//             std::cout << "Invalid command\n";
//         }

//         // Optional: show encoder every command
//         int32_t pos = lift.getLiftPosition(slave);
//         std::vector<int> alarm  = lift.readAlarm(slave);
//         std::cout << "Lift position: " << pos << std::endl;
//     }

//     std::cout << "Exiting lift control\n";
//     return 0;
// }  




// this is a code need to make a short utomation i neeed a code that will be 1 for 20 sec nd 
// stop -3 nd 2 for 20 sec it should ask me cycle only , remember first 1, stop-3, 2 , stop , nd 1