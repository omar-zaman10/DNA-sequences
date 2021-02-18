#include <FastLED.h>
#define NUM_LEDS 52
#define LED_PIN 7

CRGB leds[NUM_LEDS];
uint8_t paletteIndex = 0;
uint8_t starting_hue  = 0;


#define x_pin  A0
#define y_pin  A1
#define switch_pin  9
#define max_animation 5

int colour_mode = 1;
int Speed = 0;
int max_col = 8;
int max_speed = 1;
int animation = 1;


void control_setting(int max_col,int max_speed){


  //Changes The Animation
  EVERY_N_MILLISECONDS(500){

  if (digitalRead(switch_pin) == 0) {
    if (animation < max_animation) {
      animation +=1; }
    else {
      animation = 1;
      }
    }

  // Changes the Colour
  
  if (analogRead(y_pin) == 1023) {
    if (colour_mode < max_col) {
      colour_mode +=1; }
    else {
      colour_mode = 1;
      }
    }
  else if (analogRead(y_pin) == 0){
    if (colour_mode > 1) {
      colour_mode -=1; }
    else {
      colour_mode = max_col;
      }
    }

   // Changes Speed of animation

   if (analogRead(x_pin) == 1023) {
    if (Speed < max_speed) {
      Speed +=1; }
    else {
      Speed = 0;
      }
    }
  else if (analogRead(x_pin) == 0){
    if (Speed > 0) {
      Speed -=1; }
    else {
      Speed = max_speed;
      }
    }
   }
  }

void setup() {
  // put your setup code here, to run once:
  FastLED.addLeds<WS2812, LED_PIN,GRB>(leds,NUM_LEDS);
  pinMode(switch_pin,INPUT);
  digitalWrite(switch_pin,HIGH);
  Serial.begin(9600);
}



DEFINE_GRADIENT_PALETTE( fire ) {
    0, 255,255,145,
   28, 255,255,145,
   28, 255,217, 79,
   56, 255,217, 79,
   56, 252,178, 37,
   84, 252,178, 37,
   84, 252,115, 12,
  113, 252,115, 12,
  113, 249, 69,  6,
  141, 249, 69,  6,
  141, 247, 18,  2,
  170, 247, 18,  2,
  170, 188,  1,  1,
  198, 188,  1,  1,
  198, 117,  0,  2,
  226, 117,  0,  2,
  226,  42,  0,  2,
  255,  42,  0,  2};


DEFINE_GRADIENT_PALETTE( sea ) {
    0,   1,221, 53,
  255,  73,  3,178};

void lpm(CRGBPalette16 mypal){
  EVERY_N_MILLISECONDS(25){
  fill_palette(leds,NUM_LEDS,paletteIndex,255/NUM_LEDS,mypal,255,LINEARBLEND);
  paletteIndex += 1;
  FastLED.show();
  }
}

void lps(CRGBPalette16 mypal){
  EVERY_N_MILLISECONDS(25){
  fill_palette(leds,NUM_LEDS,paletteIndex,255/NUM_LEDS,mypal,255,LINEARBLEND);
  FastLED.show();
  }
}

void rainbow_move(){
  EVERY_N_MILLISECONDS(50) {
      fill_rainbow(leds, NUM_LEDS, starting_hue, 255/NUM_LEDS);
      starting_hue += 255/NUM_LEDS;
    }
    FastLED.show();
    }

void rainbow_stationary(){
  EVERY_N_MILLISECONDS(100) {
      fill_rainbow(leds, NUM_LEDS, starting_hue, 255/NUM_LEDS);
    }
    FastLED.show();
    }
    

void dual_colour(CRGB colour1, CRGB colour2){
  for  (int i = 0; i < NUM_LEDS/2; i++) {
      leds[i] = colour1; 
      // lilac
      }
    for  (int i = NUM_LEDS/2; i < NUM_LEDS; i++) {
      leds[i] = colour2;
      // blue pastel
      } 
    FastLED.show();
    //delay(1000);
  }

 //void dual_colour_switch


CRGB blue_pastel = CRGB (0,255,255);
CRGB lilac = CRGB (255,0,171);

void loop() {
  // put your main code here, to run repeatedly:
  
  control_setting(max_col,max_speed);

  switch (animation){
    case 1:
     if (Speed == 0){
        dual_colour(blue_pastel,lilac);}
      else {
        
        dual_colour(blue_pastel,lilac);
        delay(300);
        dual_colour(lilac,blue_pastel);
        delay(300);
        }
      break;
      
      
      break;
    case 2:
      if (Speed == 0){
        rainbow_stationary();}
      else {
        rainbow_move();
        } 
      break;

    case 3:
      if (Speed == 0){
        lps(sea);}
      else {
        lpm(sea);
        } 
      break;
      
    case 4:
      if (Speed == 0){
        lps(fire);}
      else {
        lpm(fire);
        } 
      break;
    
     
    case 5:
    EVERY_N_MILLISECONDS(100) {
    FastLED.clear();
    FastLED.show();}
      break;
    
    }

   Serial.print("Colour Mode:");
   Serial.print(colour_mode);
   Serial.print("\n");
   Serial.print("Speed Mode:");
   Serial.print(Speed);
   Serial.print("\n");
   Serial.print("Animation:");
   Serial.print(animation);
   Serial.print("\n");
   Serial.print("\n");


/*

     
     //blur1d (leds, NUM_LEDS ,  255);
     //fadeToBlackBy (leds, NUM_LEDS, 250);
     for (int i = 0; i<256; i++){
        fadeToBlackBy(leds,NUM_LEDS,blur);
        blur += 1;
        delay(100);
        FastLED.show();
     }

      
     FastLED.show();
*/




}
