const unsigned int music_data[] PROGMEM = {0x9F00, 0x0000, 0x8000, 0x0400, 0x0, 0x0};
volatile int music_index = 0;

void convert(unsigned long value, struct NOTE* note) {
  note->t3 = value & 0xff;
  value >>= 8;
  note->t2 = value & 0xff;
  value >>= 8;
  note->t1 = value & 0xff;
  value >>= 8;
  note->data = value & 0xff;
}

bool getNextNote(struct NOTE *x) {
  unsigned long value = (unsigned long)pgm_read_word_near(music_data + music_index*2) << 16 + (unsigned long)pgm_read_word_near(music_data + (music_index*2 + 1));
  if (value == 0) {
    return false;
  }
  music_index++;
  convert(value, x);
  return true;
}

void clearMusic() {
  music_index = 0;
}

