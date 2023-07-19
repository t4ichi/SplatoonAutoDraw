#include <NintendoSwitchControlLibrary.h>
#include "data.h"

//現在の座標の保持変数
int x_pos = 0;
int y_pos = 0;

//終了したかどうかのフラグ
bool finFlag = false;

uint16_t PRESS_WAIT_TIME   = 30;
uint16_t RELEASE_WAIT_TIME = 30;
uint8_t A_PUSH_COUNT = 10;
uint8_t OVER_PUSH_COUNT = 10;
bool FINISH_SAVE = true;

int cnt = 0;

bool GetDot(int x, int y){
  uint8_t v = pgm_read_byte(&(ImageData[y][x/8]));
  return (v & (1 << (7 - (x % 8)))) > 0;
}

uint8_t GetDirection(uint8_t &command,int &cnt){
  auto dir = [&](bool v1, bool v2) {
      return (v1 ? 2 : 0) + (v2 ? 1 : 0);
  };
  
  uint8_t bitIndex = cnt % 4;
  uint8_t shift1 = 7 - (bitIndex * 2);
  uint8_t shift2 = shift1 - 1;
  return dir((command & (1 << shift1)) > 0, (command & (1 << shift2)) > 0);
}

//ドット打ち
void DotBlack(){
  SwitchControlLibrary().pressButton(Button::A);
  SwitchControlLibrary().sendReport();   
  delay(PRESS_WAIT_TIME);
  SwitchControlLibrary().releaseButton(Button::A);
  SwitchControlLibrary().sendReport();   
  delay(RELEASE_WAIT_TIME);
}

//十字キーの入力
void pushHatEx(uint8_t hat){
  SwitchControlLibrary().pressHatButton(hat);
  SwitchControlLibrary().sendReport();   
  delay(PRESS_WAIT_TIME);
  SwitchControlLibrary().releaseHatButton();   
  SwitchControlLibrary().sendReport();   
  delay(RELEASE_WAIT_TIME);
}

void drawDot(){
  if(cnt >= FINISH_COUNT){
    return;
  }
  
  bool dot = GetDot(x_pos,y_pos);
  if( !dot ) DotBlack();
  
  uint8_t commandData = pgm_read_byte(&CommandData[cnt/4]);
  uint8_t command = GetDirection(commandData,cnt);
  
  if(command == 0){
    y_pos--;
    pushHatEx(Hat::UP);
  }else if(command == 1){
    x_pos++;
    pushHatEx(Hat::RIGHT);  
  }else if(command == 2){
    y_pos++;
    pushHatEx(Hat::DOWN);
  }else if(command == 3){
    x_pos--;
    pushHatEx(Hat::LEFT);
  }
  cnt++;
}

void setup(){
  //コントローラーの決定でAボタンを5回0.5秒ごと押す
  pushButton(Button::A, 500, A_PUSH_COUNT);
   
  //小さいペンに変える
  pushButton(Button::L, 500, 5);
  
  //ペン先を左上に持ってくる
  tiltLeftStick(Stick::MIN, Stick::MIN, 5000);
  
   //全面クリア
   pushButton(Button::LCLICK);
}

void loop(){
  drawDot();
}
