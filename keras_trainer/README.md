

### How to use
```python

from keras_trainer.trainer import KerasTrainer

train_epoch = 10
model = get_model()
# if you want multi gpu training.
# is_multi, model, original_model = KerasTrainer.apply_multi_gpu_if_available(get_model)
# but, when save to file use original model

trainer = KerasTrainer()
model, history = trainer.train(get_model(),
                               get_train_dataset_loader(),
                               get_val_dataset_loader(),
                               train_epoch)

model.save('./model_file.h5')
```