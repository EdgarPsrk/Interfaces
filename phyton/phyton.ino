// Código del Arduino
void setup() {
  Serial.begin(9600);
  pinMode(9,OUTPUT);
}

void loop() {
  float valor_A0 = analogRead(A0) / 1023.0 * 5.0;
  float valor_A1 = analogRead(A1) / 1023.0 * 5.0;

  Serial.println(valor_A0);
  delay(100);

  Serial.println(valor_A1);
  delay(100);

  if(Serial.available() > 0){
    String mensaje = Serial.readStringUntil('\n');

    if(mensaje.startsWith("LED:")){
      int valor_led = mensaje.substring(4).toInt();
      analogWrite(9,valor_led);
    }
  }
}
