def model_inputs():
    input=tf.placeholder(tf.int32,[None,None],name="Inputs")
    targets=tf.placeholder(tf.int32,[None,None],name="Targets")
    lr=tf.placeholder(tf.float32,name="learning_rate")
    keep_prob=tf.placeholder(tf.float32,name="keep_prob")
    return inputs,targets,lr,keep_prob
