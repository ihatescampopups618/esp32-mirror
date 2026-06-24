#include <TFT_eSPI.h>

TFT_eSPI tft;

#define W 160
#define H 80
#define SIZE (W * H * 2)

uint8_t buffer[SIZE];

void setup() {
  Serial.begin(921600);
  Serial.setTimeout(50);

  tft.init();
  tft.setRotation(3); // Right-side up landscape mode
  tft.fillScreen(TFT_BLACK);

  tft.setSwapBytes(true); // Keeps your working colors active
}

bool readHeader() {
  const char sig[5] = {'S','T','A','R','T'};
  int i = 0;

  while (i < 5) {
    if (!Serial.available()) continue;

    char c = Serial.read();

    if (c == sig[i]) i++;
    else i = (c == 'S') ? 1 : 0;
  }

  return true;
}

void loop() {
  if (!readHeader()) return;

  while (Serial.available() < 4);

  uint32_t size =
    (Serial.read() << 24) |
    (Serial.read() << 16) |
    (Serial.read() << 8)  |
     Serial.read();

  if (size != SIZE) return;

  size_t got = Serial.readBytes((char*)buffer, SIZE);

  if (got == SIZE) {
    // FIXED CORRECTION: 
    // Resetting both X and Y to 0,0 since the REDTAB profile maps your display cleanly!
    tft.pushImage(0, 0, W, H, (uint16_t*)buffer);
  }
}