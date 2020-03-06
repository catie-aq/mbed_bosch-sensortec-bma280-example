/*
 * Copyright (c) 2018, CATIE
 * SPDX-License-Identifier: Apache-2.0
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#include "bma280.h"
#include "mbed.h"

using namespace sixtron;

namespace {
#define PERIOD_MS 500
}

static DigitalOut led1(LED1);
static I2C i2c(I2C_SDA, I2C_SCL);
static BMA280 bma280(&i2c);
bma280_acceleration_t acceleration;

// main() runs in its own thread in the OS
// (note the calls to Thread::wait below for delays)
int main()
{
    if (!bma280.initialize(BMA280::Range::Range_4g, BMA280::Bandwidth::Bandwidth_62_50_Hz)) {
        printf("failed to detect BMA280\n");
        return -1;
    }
    printf("Alive!\n");

    while (true) {
        acceleration = bma280.acceleration();
        printf("Acceleration (m/s²): %6.3f %6.3f %6.3f\n", acceleration.x, acceleration.y, acceleration.z);
        led1 = !led1;
        ThisThread::sleep_for(PERIOD_MS);
    }
}
