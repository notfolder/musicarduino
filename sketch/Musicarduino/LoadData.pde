/*
 * データ取得モジュール
 * リングバッファを抽象化
 * 実際のデータリードはMusicDataモジュールに抽象化する予定
 */
#include <avr/pgmspace.h>
typedef struct NOTE {
  byte data;
  byte t1;
  byte t2;
  byte t3;
};

const unsigned int music_data[] PROGMEM = {0x9F00, 0x0000, 0x8000, 0x0400, 0x0, 0x0};
volatile int music_index = 0;

#define BUFFER_SIZE 32
NOTE notes[BUFFER_SIZE];
//volatile int note_index_read = 0;
//volatile int note_index_write = 0;

void convert(unsigned long value, struct NOTE* note) {
  note->t3 = value & 0xff;
  value >>= 8;
  note->t2 = value & 0xff;
  value >>= 8;
  note->t1 = value & 0xff;
  value >>= 8;
  note->data = value & 0xff;
}

struct NOTE *getNextNote() {
  unsigned long value = (unsigned long)pgm_read_word_near(music_data + music_index*2) << 16 + (unsigned long)pgm_read_word_near(music_data + (music_index*2 + 1));
  if (value == 0) {
    return 0;
  }
  music_index++;
  convert(value, &notes[0]);
  return &notes[0];
}

void clearNote() {
  music_index = 0;
//  note_index_read = 0;
}

int getNextTime(NOTE *note) {
  return note->t1 << 16 + note->t2 << 8 + note->t3;
}

int getData(NOTE *note) {
  return note->data;
}

