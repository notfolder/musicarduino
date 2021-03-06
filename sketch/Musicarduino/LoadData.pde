/*
 * データ取得モジュール
 * リングバッファを抽象化
 * 実際のデータリードはMusicDataモジュールに抽象化する予定
 */
typedef struct NOTE {
  byte data;
  byte t1;
  byte t2;
  byte t3;
};

#define BUFFER_SIZE 128
NOTE notes[BUFFER_SIZE];
volatile int note_index_read = 0;
volatile int note_index_write = 0;
volatile int note_index_count = 0;

struct NOTE *getNextNote() {
  return dequeue();
}

bool loadNote() {
  while (!is_full()) {
    //Serial.println("load...");
    NOTE *note = getLast();
    if (note == 0) return true;
    bool ret = loadNextNote(note);
    enqueue();
    if (!ret) {
      Serial.println("load Last!!");
      return false; // 終了マーク読み出し
    }
  }
  return true;
}

void clearNote() {
  clearMusic();
  note_index_read = 0;
  note_index_write = 0;
  note_index_count = 0;
}

unsigned long getNextTime(NOTE *note) {
  return ((unsigned long)note->t1 << 16) + ((unsigned long)note->t2 << 8) + note->t3;
}

int getData(NOTE *note) {
  return note->data;
}

bool is_full(){
  return note_index_count == BUFFER_SIZE;
}

struct NOTE* getLast() {
  if (is_full()) return 0;
  return &notes[note_index_write];
}

bool enqueue() {
  if (is_full()) return false;
  note_index_write++;
  note_index_count++;
  if (note_index_write == BUFFER_SIZE)
    note_index_write = 0;
  return true;
}

bool is_empty() {
  return note_index_count == 0;
}

struct NOTE* dequeue(){
  if (is_empty()) {
    return 0;
  }
  NOTE *x = &notes[note_index_read++];
  //Serial.print("note: ");
  //Serial.println(x->data, HEX);
  note_index_count--;
  if (note_index_read == BUFFER_SIZE)
    note_index_read = 0;
  return x;
}

