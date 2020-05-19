**Original README renamed to GPT-2.**

# gpt-2
Just playing around with this:

- Commented out model downloads from docker files.
- Tidy some basic formatting.
- Default "model" is already set to 124M.
- Edit "top_k" (diversity) to default to 40.
- Fix access path to sort in "sample.py", `tf.contrib.framework.sort`.
- Update docker files to (latest V1) tensorflow 1.15.2.
- Fix some of the compatibility issues highlighted.
```
$ docker image build --tag gpt-2:0.1 -f Dockerfile.cpu .
$ python3 download_model.py 124M
$ python3 download_model.py 1558M
$ docker run -it -v /home/john/PycharmProjects/gpt-2/:/gpt-2 gpt-2:0.1 bash
$ python3 src/generate_unconditional_samples.py
$ python3 src/interactive_conditional_samples.py --model=1558M
```
