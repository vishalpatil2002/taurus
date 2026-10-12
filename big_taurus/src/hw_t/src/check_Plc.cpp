#include <iostream>
#include <unistd.h>        // sleep()
#include <modbus/modbus.h>

int main()
{
    modbus_t* ctx;
    uint8_t coil;

    // Connect to PLC
    ctx = modbus_new_tcp("192.168.7.5", 502);
    if (modbus_connect(ctx) == -1) {
        std::cerr << "Connection failed\n";
        return -1;
    }

    // Loop
    while (true)
    {
        // Write M0 = TRUE
        modbus_write_bit(ctx, 11, 1);

        // Read M0 back
        modbus_read_bits(ctx, 11, 1, &coil);

        // Print result
        std::cout << "M0 value = " << (int)coil << std::endl;

        sleep(1);   // 1 second delay
    }

    // Cleanup (never reached here)
    modbus_close(ctx);
    modbus_free(ctx);

    return 0;
}
