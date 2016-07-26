/*
   name Muscarduino.pde
   date Thu Jul 21 22:24:34 JST 2016

   Released under the 'Buy Me a Beer' license
   (If we ever meet, you buy me a beer)
*/
#include <MsTimer2.h>
// Pin割り当て
// constants won't change. They're used here to
// set pin numbers:
int         D2 =   2;  // Switch:Push
int         D8 =   8;  // Led:Red
int         D9 =   9;  // Led:Red
int        D11 =  11;  // Led:Red
int        D12 =  12;  // Led:Red
int        D10 =  10;  // Led:Red
int        D13 =  13;  // Arduino:uno_r3

// ボタンの状態制御
volatile int push_state = 0;
// 演奏時間
volatile int time = 0;
// データを出力する時間
volatile int next_time = 0;
// 次に出力するデータ
volatile int data = 0;
volatile int state = 0;

bool readNextNote() {
    NOTE *note = getNextNote();
    if (note == 0) {
      clearNote();
      time = 0;
      push_state = 0;
      next_time = 0;
      data = 0;
      state = 0;
      MsTimer2::stop();
      return false;
    }
    next_time = getNextTime(note);
    data = getData(note);
    return true;
}

// ボタンが押されるたびに呼ばれる関数
void push() {
  Serial.println("PUSH");
  if (push_state == 0) {
    // 初めてボタンが押されたので処理を開始する
    push_state = 1;
    MsTimer2::start();             // タイマー割り込み開始
    readNextNote(); // 初回ノートを読みだしておく
  }
}

// 演奏開始後1ms毎に呼ばれる関数(メインの処理)
void timer() {
//  Serial.println("TIMER");
  // 次のデータの時間になった
  if (time >= next_time) {
    Serial.println("TIMER2");
    PORTB = data;
    if (!readNextNote()) return;
  }
  // 演奏時間を1ms進める
  time++;
}

void setup() {
  // initialize
  Serial.begin(9600);

  pinMode(D2,  INPUT_PULLUP);  // Switch:Push
  pinMode(D8, OUTPUT);  // Led:Red
  pinMode(D9, OUTPUT);  // Led:Red
  pinMode(D10, OUTPUT);  // Led:Red
  pinMode(D11, OUTPUT);  // Led:Red
  pinMode(D12, OUTPUT);  // Led:Red
  pinMode(D13, OUTPUT);  // Arduino:uno_r3

  loadNote();  // リングバッファにデータをロードしておく
  MsTimer2::set(1, timer);     // 1ms毎にtimer( )割込み関数を呼び出す様に設定
  attachInterrupt(0, push, FALLING);  // PIN2がHIGH->LOW(ボタンが押された時)にpushを呼ぶ
  Serial.println("START");
}

void loop() {
  if (state = 0) {
    // 常にバッファを貯めておく
    if (!loadNote()) {
      state = 1;
    }
  }
  delay(1);
}


