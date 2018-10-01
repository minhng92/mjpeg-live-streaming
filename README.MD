MJPEG live streaming server has features:
+ Backend using Flask
+ Automatically recycle old images
+ Easy to integrate to web application with only an image tag
+ Cross-platform supported
+ Set up in one command line with Docker

Python backend source code is greatly inspired by [`Miguel Grinberg`](https://blog.miguelgrinberg.com/author/Miguel%20Grinberg).

# USAGE

0. Install dependencies

```
$ pip install -r requirements.txt
```

1. Start MJPEG Server:

```
$ cd src
$ python main.py
```

2. Simulate a simple stream:

```
$ python test_mjpeg.py src/images
```

3. View the stream locally by opening **show_mjpeg.html** file with your browser.

4. Optionally configure nginx with the template at **nginx_mjpeg.conf**. Check the stream by using **show_mjpeg_nginx.html**

# USAGE - DOCKER

0. You are at root folder.

1. Build and start MJPEG Server:

```
$ docker-compose up -d
```

2. Simulate a simple stream (note that **images** folder is mounted to **src/images**):

```
$ python test_mjpeg.py images
```

3. View the stream locally by opening **show_mjpeg.html** file with your browser.

4. Optionally configure nginx with the template at **nginx_mjpeg.conf**. Check the stream by using **show_mjpeg_nginx.html**

**screenshot:**
![screenshot](video_stream_screenshot.png)
