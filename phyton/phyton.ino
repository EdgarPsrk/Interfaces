void setup() {
  Serial.begin(9600);
}

void loop() {
  float valor = analogRead(A0) / 1023.0 * 5.0;
  Serial.println(valor);
  delay(100);
}
