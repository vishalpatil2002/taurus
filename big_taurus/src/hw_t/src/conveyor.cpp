#include <modbus/modbus.h>
#include <iostream>
#include <string>
#include <thread>
#include <chrono>
#include <cerrno>

modbus_t* connect_modbus()
{
    while (true) {
        modbus_t* ctx = modbus_new_tcp("192.168.7.5", 502);
        if (!ctx) {
            std::cerr << "Failed to create Modbus context. Retrying...\n";
            std::this_thread::sleep_for(std::chrono::seconds(2));
            continue;
        }

        if (modbus_connect(ctx) == -1) {
            std::cerr << "Connection failed: "
                      << modbus_strerror(errno) << "\n";
            modbus_free(ctx);
            std::this_thread::sleep_for(std::chrono::seconds(2));
            continue;
        }

        std::cout << "✅ Modbus connected\n";
        return ctx;
    }
}

int main()
{
    modbus_t* ctx = connect_modbus();

    std::cout << "Enter  s=0, f=1, b=2, (q to quit)\n";

    while (true) {
        std::string input;
        std::cout << "> ";
        std::cin >> input;

        if (input == "q" || input == "Q") {
            break;
        }

        int val;
        try {
            val = std::stoi(input);
        } catch (...) {
            std::cout << "❌ Invalid input\n";
            continue;
        }

        int coil = -1;
        uint8_t value = 1;

        if (val == 1) {
            coil = 7;   // M7
        } else if (val == 2) {
            coil = 8;   // M8
        } else if (val == 0) {
            coil = 9;   // M9
        } else {
            std::cout << "❌ Only 1, 0, -1 allowed\n";
            continue;
        }

        if (modbus_write_bit(ctx, coil, value) == -1) {
            std::cerr << "⚠ Write failed: "
                      << modbus_strerror(errno) << "\n";

            // reconnect on failure    1-b 2-f
            modbus_close(ctx);
            modbus_free(ctx);
            std::cout << "🔄 Reconnecting...\n";
            ctx = connect_modbus();
        } else {
            std::cout << "✅ Successfully wrote M" << coil << "\n";
        }
    }

    modbus_close(ctx);
    modbus_free(ctx);
    std::cout << "Disconnected.\n";
    return 0;
}
