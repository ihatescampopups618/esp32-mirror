#define ST7735_DRIVER            

// CHANGED: Switching to REDTAB fixes the pixel line alignment stacking issue
#define ST7735_REDTAB160x80    

#define TFT_WIDTH  80
#define TFT_HEIGHT 160

#define TFT_MISO -1        
#define TFT_MOSI 23        
#define TFT_SCLK 18        
#define TFT_CS    5        
#define TFT_DC    4        
#define TFT_RST  26        

#define SPI_FREQUENCY  27000000