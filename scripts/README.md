# Order to Run

1. `gen_noise.py` Creates noise data to send for approximating the channel
2. Send noise using `send_noise.grc` through GNU Radio Companion
3. `channel_trimmer.py` Trim the receieved noise so we can work with it
4. `channel_estimator.py` Estimate the channel response from our noise
5. `gen_data.py` To generate data to send
6. Send data using `send_data.grc`
7. `decoder_functional.py` to decode the received data
