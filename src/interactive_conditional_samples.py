#!/usr/bin/env python3

import fire
import json
import os
import numpy as np
import tensorflow as tf

import model, sample, encoder

# Test using the wikipedia description of London.
raw_text = """
London is the capital and largest city of England and the United Kingdom. Standing on the River Thames in the south-east of England,
at the head of its 50-mile (80 km) estuary leading to the North Sea, London has been a major settlement for two millennia. Londinium
was founded by the Romans. The City of London, London's ancient core − an area of just 1.12 square miles (2.9 km2) and colloquially
known as the Square Mile − retains boundaries that closely follow its medieval limits. The City of Westminster is also an Inner
London borough holding city status. London is governed by the Mayor of London and the London Assembly.
"""

# Test using the wikipedia description of a guinea pig.
#raw_text = """
# The guinea pig or domestic guinea pig (Cavia porcellus), also known as cavy or domestic cavy, is a species of rodent belonging to 
# the family Caviidae and the genus Cavia. Despite their common name, guinea pigs are not native to Guinea, nor are they closely 
# biologically related to pigs, and the origin of the name is still unclear. They originated in the Andes of South America, and 
# studies based on biochemistry and hybridization suggest they are domesticated descendants of a closely related species of cavy such 
# as C. tschudii, and therefore do not exist naturally in the wild. They were originally domesticated as livestock, as a source of 
# food, and continue to be.
# """


def interact_model(
    model_name='1558M',
    seed=None,
    nsamples=10,
    batch_size=1,
    length=150,
    temperature=1,
    top_k=40,
    top_p=1,
    models_dir='models',
):
    """
    Interactively run the model
    :model_name=124M : String, which model to use
    :seed=None : Integer seed for random number generators, fix seed to reproduce
     results
    :nsamples=1 : Number of samples to return total
    :batch_size=1 : Number of batches (only affects speed/memory).  Must divide nsamples.
    :length=None : Number of tokens in generated text, if None (default), is
     determined by model hyperparameters
    :temperature=1 : Float value controlling randomness in boltzmann
     distribution. Lower temperature results in less random completions. As the
     temperature approaches zero, the model will become deterministic and
     repetitive. Higher temperature results in more random completions.
    :top_k=40 : Integer value controlling diversity. 1 means only 1 word is
     considered for each step (token), resulting in deterministic completions,
     while 40 means 40 words are considered at each step. 0 (default) is a
     special setting meaning no restrictions. 40 generally is a good value.
     :models_dir : path to parent folder containing model subfolders
     (i.e. contains the <model_name> folder)
    """
    models_dir = os.path.expanduser(os.path.expandvars(models_dir))
    if batch_size is None:
        batch_size = 1
    assert nsamples % batch_size == 0

    enc = encoder.get_encoder(model_name, models_dir)
    hparams = model.default_hparams()
    with open(os.path.join(models_dir, model_name, 'hparams.json')) as f:
        hparams.override_from_dict(json.load(f))

    if length is None:
        length = hparams.n_ctx // 2
    elif length > hparams.n_ctx:
        raise ValueError("Can't get samples longer than window size: %s" % hparams.n_ctx)

    with tf.compat.v1.Session(graph=tf.Graph()) as sess:
        context = tf.compat.v1.placeholder(tf.int32, [batch_size, None])
        np.random.seed(seed)
        tf.compat.v1.set_random_seed(seed)
        output = sample.sample_sequence(
            hparams=hparams, length=length,
            context=context,
            batch_size=batch_size,
            temperature=temperature, top_k=top_k, top_p=top_p
        )

        saver = tf.compat.v1.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join(models_dir, model_name))
        saver.restore(sess, ckpt)

        context_tokens = enc.encode(raw_text)
        generated = 0
        for _ in range(nsamples // batch_size):
            out = sess.run(output, feed_dict={
                context: [context_tokens for _ in range(batch_size)]
            })[:, len(context_tokens):]
            for i in range(batch_size):
                generated += 1
                text = enc.decode(out[i])
                print("=" * 40 + " SAMPLE " + str(generated) + " " + "=" * 40)
                print(text)
        print("=" * 80)


if __name__ == '__main__':
    fire.Fire(interact_model)
