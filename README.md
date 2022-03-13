# Metron

Metron project tackles use case of measurement of objects. It is a great platform to test various computer vision
approaches or as well to be used for commercial Proof of Concepts.

## Key Features

:boom: efficient input video source streaming engine
:boom: various input video sources - video files, camera device
:boom: fully configurable using Facebook Research - Hydra framework
:boom: run on a bare metal or using Docker Compose
:boom: deployable on Linux, MacOS, Windows

## Table of Content

[1. Project Installation](/docs/project_installation.md)\
[2. Architecture](/docs/architecture.md)\
[3. Development Notes](/docs/development_notes.md)

## Roadmap

> ##### :warning: Attention :exclamation: :raised_hands: :exclamation:
> During roadmap timeline gaps, the work is conducted on Metron AI research track. Take a look on 
> [Peer Repositories](#peer-repositories) links section.

### 0.2.0 (~~October - December 2021~~ March - May 2022)

- [ ] setup Metron Shine component SW skeleton
- [ ] add message broker component (Redis)
- [ ] testing of the message broker component
- [ ] document message broker component
- [ ] setup Metron Shine configuration
- [ ] implement Video Receiver module
- [ ] implement Results Renderer module
- [ ] implement Results Streamer module
- [ ] testing of Metron Shine
- [ ] develop Metron Shine demo app
- [ ] dockerize Metron Shine
- [ ] documentation of Metron Shine


### 0.1.0 (April - ~~May~~ ~~June~~ July 2021)

- [x] software architecture
- [x] setup Metron Conduit software skeleton
- [x] add video file source option to Metron Conduit
- [x] add usb cam source option to Metron Conduit
- [x] complete basic Video Streamer functionality of Metron Conduit
- [x] dockerize Metron Conduit
- [x] setup Docker Compose deployment skeleton
- [x] add Hydra configuration framework
- [ ] ~~camera stream input module~~
- [ ] ~~camera stream calibration~~

## Peer Repositories

### Metron AI Research
- [Artificial Data Generator (ArDaGen)](https://github.com/OndrejSzekely/metron_ai_ardagen)
