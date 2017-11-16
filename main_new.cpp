#include <stdio.h>
#include <iostream> // for standard I/O
#include <string>   // for strings
#include <iomanip>  // for controlling float print precision
#include <sstream>  // string to number conversion
#include <opencv2/opencv.hpp>
#include <opencv2/core/core.hpp>     // Basic OpenCV structures (cv::Mat, Scalar)
#include <opencv2/imgproc/imgproc.hpp>  // Gaussian Blur
#include <opencv2/video/video.hpp>
#include <opencv2/highgui/highgui.hpp>  // OpenCV window I/O

#include "common.h"


#define TRACE_FUNC() do {\
    printf("[%s %d]\n", __func__, __LINE__);\
} while (0)

using namespace std;
using namespace cv;

static int start_cap(void);
static void show_frame(Mat frame);
static void save_img(Mat frame);
static void call_recognize(Mat frame);
static void push_stream(Mat frame);

static VideoCapture g_vin = VideoCapture(0);
static VideoWriter g_vout;

static int init(void)
{
    g_vin.set(CV_CAP_PROP_FRAME_WIDTH , DEF_FRAME_WIDTH);
    g_vin.set(CV_CAP_PROP_FRAME_HEIGHT, DEF_FRAME_HEIGHT);

    Size size = Size(g_vin.get(CV_CAP_PROP_FRAME_WIDTH),
            g_vin.get(CV_CAP_PROP_FRAME_HEIGHT));
    int fourcc = CV_FOURCC('F','L','V','1');
    fourcc = -1;
    g_vout = VideoWriter(DEF_OUT_VIDEO_NAME, fourcc,
            DEF_OUT_VIDEO_FPS, size);

    namedWindow(SHOW_WIN_NAME, SHOW_WIN_SIZE);

    return OK;
}

static int start_cap(void)
{
    char key;
    while((key = waitKey(DEF_INTERVAL_TIME))) {
        if(key == KEY_ESC) {
            break;
        }

        Mat frame;
        g_vin >> frame;
        if (frame.empty()) {
            break;
        }

        if (key == KEY_SPACE) {
            call_recognize(frame);
        }
        push_stream(frame);
        show_frame(frame);
    }
    g_vout.release();
    g_vin.release();

    return OK;
}

static void show_frame(Mat frame)
{
    imshow(SHOW_WIN_NAME, frame);
}

static void save_img(Mat frame)
{
    TRACE_FUNC();
    vector<int> params;
    params.push_back(CV_IMWRITE_JPEG_QUALITY);
    params.push_back(90);
    imwrite(DEF_OUT_IMAGE_NAME, frame, params);
}

static void call_recognize(Mat frame)
{
    save_img(frame);

    // TODO
}

static void push_stream(Mat frame)
{
    static int counter = 0;

    g_vout.write(frame);
    counter++;

    if (counter > 100) {
        cout << "asdf" << endl;
        counter = 0;
    }
    // TODO
}

//int main(int argc, char *argv[])
int main(void)
{
    TRACE_FUNC();
    init();
    start_cap();

    return 0;
}
