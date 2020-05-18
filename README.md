**Original README renamed to GPT-2.**

# gpt-2
Just playing around with this.

- Commented out model downloads from docker files.
- Tidy some basic formatting.
- Default "model" is set to 124M.
- Edit "top_k" (diversity) to default to 40.
- Fix access path to sort in "sample.py", `tf.contrib.framework.sort`.

```
docker image build --tag gpt-2:0.1 -f Dockerfile.cpu .
python3 download_model.py 124M
docker run -it -v /home/john/PycharmProjects/gpt-2/:/gpt-2 gpt-2:0.1 bash
python3 src/generate_unconditional_samples.py
python3 src/interactive_conditional_samples.py
```
