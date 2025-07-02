const int mq2Pin = A1;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int sensorValue = analogRead(mq2Pin);
  Serial.print("MQ-2 Reading: ");
  Serial.println(sensorValue);

  delay(2000);
}
