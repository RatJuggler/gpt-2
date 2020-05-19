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

### Some example outputs
Londoners, the people of London, are proud of their city's rich culture and heritage, the importance of which can be seen in the 
many national and cultural sits of honor. 
Historically, London remains one of the world's principal cities of literature, music, theatre, drama and architecture. One of the 
oldest extant sites for artistic performance, theater and architecture is the British Library. This famous institution, the oldest 
and most significant in the UK, houses some of the world's greatest collections of manuscripts, paintings, prints, art, pottery and
the collection of world monuments ″from the Pyramids to Stonehenge to Wembley Stadium to London Bridge to Nelson's Column.

The London Eye was built in 1794. The London Eye, which is the main light at the heart of the city, was constructed to show the 
location of The New Great Exhibition, which began in the autumn of 1851 and lasted for over a year. The original London Eye was 
constructed as much in honour of The London Times as it was to help display the sights of the city at night. The London Eye was 
constructed by architect Sir Richard B. Smith (1788–1871) and the former editor of the London Times, Joseph Needham (1810–1860). 
It consists of a 60-foot (18 m) high white iron structure (the London Eye's tower) and a 50-
