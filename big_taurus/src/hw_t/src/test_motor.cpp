#include <modbus/modbus.h>
#include <stdio.h>
#include <unistd.h>
#include <errno.h>

#define DEVICE "/dev/CONVEYOR"
#define BAUD 115200
#define SLAVE_ID 4

#define REG_SPEED   48    // 40049
#define REG_COMMAND 124   // 40125

#define CMD_JOG_PREP 159
#define CMD_RUN      150
#define CMD_STOP     226
#define CMD_DISABLE  158

void write_reg(modbus_t *ctx, int addr, int value)
{
    modbus_set_slave(ctx, SLAVE_ID);

    if (modbus_write_register(ctx, addr, value) == -1)
        printf("Write failed: %s\n", modbus_strerror(errno));
}

// run motor (sign = direction)
void run_motor(modbus_t *ctx, int speed)
{
    printf("Running speed: %d\n", speed);

    write_reg(ctx, REG_SPEED, speed);   // 🔥 16-bit write

    write_reg(ctx, REG_COMMAND, CMD_JOG_PREP);
    write_reg(ctx, REG_COMMAND, CMD_RUN);
}

void stop_motor(modbus_t *ctx)
{
    printf("STOP\n");

    write_reg(ctx, REG_COMMAND, CMD_STOP);
    write_reg(ctx, REG_COMMAND, CMD_DISABLE);
}

int main()
{
    modbus_t *ctx = modbus_new_rtu(DEVICE, BAUD, 'N', 8, 1);

    if (!ctx)
    {
        printf("Modbus init failed\n");
        return -1;
    }

    if (modbus_connect(ctx) == -1)
    {
        printf("Connection failed: %s\n", modbus_strerror(errno));
        return -1;
    }

    printf("Connected\n");

    // Forward
    run_motor(ctx, 1000);
    sleep(5);

    stop_motor(ctx);
    sleep(2);

    // Reverse (negative speed)
    run_motor(ctx, -1000);
    sleep(5);

    stop_motor(ctx);

    modbus_close(ctx);
    modbus_free(ctx);

    return 0;
}