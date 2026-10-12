#ifndef MOONS_MODBUS_H
#define MOONS_MODBUS_H

#include <modbus/modbus.h>
#include <vector>
#include <utility>
#include <cstdint>

class Moons
{
public:
    Moons();
    ~Moons();

    bool isConnected() const;
    void end();

    // -------- Lift control --------
    void setLiftSpeed(int slave, int32_t speed);
    void liftUp(int slave);
    void liftDown(int slave);
    void stopLift(int slave);
    void setPosition(int slave, int32_t position, int32_t speed);
    void zeroEncoder(int slave, int32_t value = 0);    
    void resetAlarm(int slave);
    double getencoder(int slave);
    std::vector<int> readAlarm(int slave);
    // -------- Encoder --------
    int32_t getLiftPosition(int slave, int32_t prev = 0);

private:
    modbus_t* mod_;
    bool connected_;
    int motor_status_;

    // -------- Low-level helpers --------
    void writeRegister(int address, int value, int slave);
    int32_t readRegister(int address, int slave, bool signed_mode);
    void longWrite(int address, int32_t value, int slave);
    int32_t longRead(int address, int slave, bool unsigned_mode, int32_t prev);
  
    std::vector<int> getBits(uint32_t val, int bits);

    int32_t two_cmp(uint32_t val, int bits);
};

#endif
