In order to understand the modern operating systems and their offerings we might want to first have a look at a simple operating systems that was popular until mid 90s (until Windows 95 finally arrived and made it obsolete).

This operating system is called MSDOS and nowadays you can check its way of working by using an exmulator like dosbox: https://www.dosbox.com/

Once you've installed dosbox you need to:
* install a compiler (I've discovered that openwatcome offers compilers running on MSDOS and producing MSDOS executables: https://github.com/open-watcom/open-watcom-v2/releases/tag/Current-build )
* compile the `video.c` file below using the instructions

video.c contents:

On short: this writes directly in the video memory (adress 0xA0000) of the graphics video mode 0x13 (320x200 - 256 colors)

```
#include <dos.h>
#include <conio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define VIDEO_INT 0x10
#define MODE_13H  0x13
#define TEXT_MODE 0x03
#define SCREEN_WIDTH  320
#define SCREEN_HEIGHT 200
#define VIDEO_SEGMENT 0xA000

void set_video_mode(unsigned char mode) {
    union REGS regs;
    regs.h.ah = 0x00;
    regs.h.al = mode;
    int86(VIDEO_INT, &regs, &regs);
}

void putpixel(int x, int y, unsigned char color,unsigned char far *buffer) {
    unsigned char far* video_memory = buffer != NULL ? buffer : (unsigned char far*)MK_FP(VIDEO_SEGMENT, 0);
    video_memory[y * SCREEN_WIDTH + x] = color;
}

void drawScene(int offset,unsigned char far *buffer)
{
	int x,y;
	for (y = 0; y < SCREEN_HEIGHT/10; y++) {
		for (x = 0; x < SCREEN_WIDTH; x++) {
			putpixel(x, y, (offset + x + y) % 256,buffer);  // Simple gradient
		}
	}	
}

void copyToVideoMem(unsigned char far *buf)
{
	unsigned char far* video_memory = (unsigned char far*)MK_FP(VIDEO_SEGMENT, 0);
	memcpy(video_memory,buf,SCREEN_HEIGHT*SCREEN_WIDTH);
}

int main() {
	int done = 0;
    double secondsElapsed = 0;
	clock_t t1,t2;
	unsigned char far *buf = malloc(SCREEN_WIDTH*SCREEN_HEIGHT);
	
	int useDoubleBuffer = 1;
	int offset = 0;
	int increment = 4;
    
	
	
	set_video_mode(MODE_13H);  // Switch to 320x200x256 mode
	t1 = clock();
	
	memset(buf,0,SCREEN_WIDTH*SCREEN_HEIGHT);
	drawScene(offset,buf);
	copyToVideoMem(buf);
	
	
	
	
	
    while(!done) {
		
		if (useDoubleBuffer) {
			copyToVideoMem(buf);
		} else {
			drawScene(offset,NULL);
		}
		
		if (kbhit()) {
			int ch = getch();
			switch(ch)
			{
				case 72: // up arrow press
				done = 1;
				break;
				case 75: // left arrow
				increment+=2;
				break;
				case 77: // righ arrow
				increment-=2;
				break;
			}
			
		}

		t2 = clock();
		secondsElapsed = (t2 - t1)/CLOCKS_PER_SEC;
		if (secondsElapsed >= 0) {
			t1 = t2;
			offset+=increment;
			offset%=256;
			drawScene(offset,buf);
		}
	}


    set_video_mode(TEXT_MODE);  // Restore text mode
    return 0;
}

```

Compile this with this command: `wcl -mh video.c`

The important thing is to follow the program flow:

1. starts the program
2. enters video mode
3. loops while the user doesn't exit (press up key)
4. the loop is always drawing, never blocks because we are making an animation
5. the `kbhit` functions just checks if there's a key pressed and returns 1 if that's the case, or 0 otherwise
6. The user checks the key in case it was pressed and takes action
7. If up key is pressed it will exit the loop
8. If left key is pressed the drawing will move left
9. If right key is pressed the drawing will move right

Mind that this is a loop highly used in video games. We have a loop that draws continuously (we don't wait for a key to be pressed) and when some key is pressed (checked by `khbit` MSDOS function) we quickly handle it and then we go back to drawing.

This is a very rudimentary way of working compared to nowadays (2025) but it is very important to be understood as modern OSes offer much more functionality that masks what happens behind the scenes.

# The message loop

That loop we see in the code is called the message loop and it does exaclty what its name says, it checks for "messages" (or events) and handles them accordingly. Those messages are then handled as users wants (in this case a simple switch statement but this can be done in different functions).

There can be other types of messages, not only keyboard strokes. You can interact with the mouse but that will not be covered here as it goes very deep into MSDOS low level things.
