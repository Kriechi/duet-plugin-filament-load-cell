#include <Wire.h>
#include <HX711.h>

#define I2C_ADDRESS 0x08
#define OFFSET -102300
#define SCALE -822.0

#define P_DOUT PD5
#define P_SCK  PD6

float current_value;
HX711 scale;

void requestEvent() {
  Serial.println("request event");
  Wire.write((byte*)&current_value, sizeof(float));
}

void setup() {
  Serial.begin(9600);

  Wire.begin(I2C_ADDRESS);
  Wire.onRequest(requestEvent);

  scale.begin(P_DOUT, P_SCK);
  scale.set_scale(SCALE);
  scale.set_offset(OFFSET);
}

void loop() {
  // read multiple times to average out noise
  float value = scale.get_units(3);

  // sanity filter values to 0g to 2kg
  current_value = constrain(value, 0.0, 2000.0);

  Serial.println(current_value);

  scale.power_down();
  delay(1000);
  scale.power_up();
}
