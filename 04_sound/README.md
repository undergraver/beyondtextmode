This describes another important part of today's multimedia applications, namely the sound. We will show a simple example of playing a sound with the help of the portaudio library: https://www.portaudio.com/

This is yet another example of a framework where you need to provide a callback function that is called whenever the "speakers" want to play some sound.

```
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <portaudio.h>

#define SAMPLE_RATE       44100
#define FREQUENCY         10000.0
#define AMPLITUDE         0.5
#define DURATION_SECONDS  2
#define FRAMES_PER_BUFFER 64
#define TWO_PI            (2.0 * 3.14159265)

#define TOTAL_FRAMES (SAMPLE_RATE * DURATION_SECONDS)

typedef struct {
    float phase;
    unsigned long frameIndex;
} paTestData;

// Audio callback function
static int paCallback(const void *inputBuffer, void *outputBuffer,
                      unsigned long framesPerBuffer,
                      const PaStreamCallbackTimeInfo* timeInfo,
                      PaStreamCallbackFlags statusFlags,
                      void *userData) {
    paTestData *data = (paTestData*)userData;
    float *out = (float*)outputBuffer;
    (void)inputBuffer; // Prevent unused variable warning

    for (unsigned long i = 0; i < framesPerBuffer; i++) {
        if (data->frameIndex >= TOTAL_FRAMES) {
            *out++ = 0.0f; // Output silence after duration
        } else {
            *out++ = (float)(AMPLITUDE * sin(data->phase));
            data->phase += (float)(TWO_PI * FREQUENCY / SAMPLE_RATE);
            if (data->phase >= TWO_PI)
                data->phase -= TWO_PI;
            data->frameIndex++;
        }
    }

    return (data->frameIndex >= TOTAL_FRAMES) ? paComplete : paContinue;
}

int main(void) {
    PaStream *stream;
    PaError err;
    paTestData data = {0};

    printf("Initializing PortAudio...\n");
    err = Pa_Initialize();
    if (err != paNoError) goto error;

    err = Pa_OpenDefaultStream(&stream,
                               0,          // No input channels
                               1,          // Mono output
                               paFloat32,  // 32-bit floating point output
                               SAMPLE_RATE,
                               FRAMES_PER_BUFFER,
                               paCallback,
                               &data);
    if (err != paNoError) goto error;

    err = Pa_StartStream(stream);
    if (err != paNoError) goto error;

    printf("Playing 10kHz sine wave for %d seconds...\n", DURATION_SECONDS);
    while (Pa_IsStreamActive(stream)) {
        Pa_Sleep(100);  // Wait for stream to finish
    }

    err = Pa_CloseStream(stream);
    if (err != paNoError) goto error;

    Pa_Terminate();
    printf("Playback finished.\n");
    return 0;

error:
    fprintf(stderr, "PortAudio error: %s\n", Pa_GetErrorText(err));
    if (stream) Pa_AbortStream(stream);
    Pa_Terminate();
    return 1;
}

```
This callback function is asynchronous and you will have to abstain from using locks (mutexes), opening/reading from files, allocating memory etc. See these pages for details:
* https://github.com/PortAudio/portaudio/wiki/Tips_Callbacks
* https://www.portaudio.com/docs/v19-doxydocs/writing_a_callback.html

In case you want to use locks please make sure you use some lock free data structures. For more details about those please see:
* https://github.com/DNedic/lockfree
* https://en.wikipedia.org/wiki/Non-blocking_algorithm

