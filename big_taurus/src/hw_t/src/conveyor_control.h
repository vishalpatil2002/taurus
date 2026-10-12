#ifndef CONVEYOR_CONTROL_H
#define CONVEYOR_CONTROL_H

#include <modbus/modbus.h>
#include <vector>
#include <cstdint>

class ConveyorControl
{
public:
    ConveyorControl();
    ~ConveyorControl();

    bool isConnected() const;
    void end();

    // -------- Conveyor control --------
    void conveyorForward(int slave);   // removed speed
    void conveyorBackward(int slave);  // removed speed
    void conveyorStop(int slave);
    void setConveyorSpeed(int slave);  // removed speed
    
    // -------- Status --------
    int32_t getConveyorPosition(int slave, int32_t prev = 0);
    std::vector<int> readAlarm(int slave);
    void resetAlarm(int slave);

private:
    modbus_t* mod_;
    bool connected_;
    int conveyor_status_;

    // 🔥 Hardcoded speed
    static const int32_t FIXED_SPEED = 3000;

    // -------- Low-level helpers --------
    void writeRegister(int address, int value, int slave);
    int32_t readRegister(int address, int slave, bool signed_mode);
    void longWrite(int address, int32_t value, int slave);
    int32_t longRead(int address, int slave, bool unsigned_mode, int32_t prev);
  
    std::vector<int> getBits(uint32_t val, int bits);
    int32_t two_cmp(uint32_t val, int bits);
};

#endif