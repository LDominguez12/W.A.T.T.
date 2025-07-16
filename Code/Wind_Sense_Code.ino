//Pin Assignments//
const int anem_pin = 2;
const int rain_gauge_pin = 3;
const int wind_vane_pin = A3;

// Counters
volatile int wind_clicks = 0;
volatile int rain_tips = 0;

unsigned long last_sample_time = 0;
const unsigned long sample_interval = 1000;

// Constants
const float rain_per_tip = 0.2794; //mm per tip
const float wind_factor = 2.25; //mph per click per sec

void setup() {
  Serial.begin(9600);

  pinMode(anem_pin, INPUT_PULLUP);
  pinMode(rain_gauge_pin, INPUT_PULLUP);
  pinMode(wind_vane_pin, INPUT);

  attachInterrupt(digitalPinToInterrupt(anem_pin), countWind, FALLING);
  attachInterrupt(digitalPinToInterrupt(rain_gauge_pin), countRain, FALLING);
}

void loop(){
  if (millis() - last_sample_time >= sample_interval){
    noInterrupts();
    int wind = wind_clicks;
    int rain = rain_tips;
    wind_clicks = 0;
    rain_tips = 0;
    interrupts();

    float wind_speed = (wind*wind_factor);
    float wind_speed_ms = wind_speed * 0.44704;
    float rainfall = rain* rain_per_tip;
    int wind_vane_val = analogRead(wind_vane_pin);

    Serial.print("Wind Speed: ");
    Serial.print(wind_speed);
    serial.println(" m/s")
    
    Serial.print("Rainfall: ");
    Serial.print("Wind Vane (raw): ");
    Serial.println(wind_vane_val);

    lastSampleTime = millis();
  }
}

void count_wind(){
  wind_clicks++;
}

void count_rain(){
  rain_tips++;
}