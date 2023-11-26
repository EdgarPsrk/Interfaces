// Código del Arduino
int ledPin1 = 9;  // Pin para el primer LED
int ledPin2 = 10; // Pin para el segundo LED

void setup() {
  Serial.begin(9600);
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
}

void loop() {
  float valor_A0 = analogRead(A0) / 1023.0 * 5.0;
  float valor_A1 = analogRead(A1) / 1023.0 * 5.0;

  Serial.println(valor_A0);
  delay(100);

  Serial.println(valor_A1);
  delay(100);

  if (Serial.available() > 0) {
    String mensaje = Serial.readStringUntil('\n');

    if (mensaje.startsWith("LED1:")) {
      int valor_led = mensaje.substring(5).toInt();
      analogWrite(ledPin1, valor_led);
    } else if (mensaje.startsWith("LED2:")) {
      int valor_led = mensaje.substring(5).toInt();
      analogWrite(ledPin2, valor_led);
    }
  }
}
