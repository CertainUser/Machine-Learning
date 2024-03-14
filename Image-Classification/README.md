## Convolutional neural network model to distinguish between 6 types of objects ##

![Example Image](https://github.com/LambdaKappa/Machine-Learning/assets/153376810/75bd49b3-70c9-4cde-bbbe-d304f2324ece)

# Information #

- Convolutional neural network to categorize images build using TensorFlow with simple graphical interface provided aimed to show model predictions.

_If you encounter issues with any of the files in this directory, feel free to send me a message._ 

Training and validation datasets were taken from https://www.kaggle.com/datasets/puneet6060/intel-image-classification.

# Instructions #      
- Clone this folder or the entire repository.

- Consider downloading mentioned dataset and putting it in this directory. Rename it as "intel_image_dataset".

Directory tree should look like this:
```Ruby
...
  ├── ...
  └── Image-Classification
      ├── other_project_files
      └── intel_image_dataset
          ├── seg_pred
          ├── seg_test
          └── seg_train
      ...
...
```

- Run the following command in the project's directory to install dependencies:
```zsh
pip3 install -r requirements.txt
```

- You can either follow along with the Jupyter notebook to train the model or make use of the 'classifier.keras' model in this folder.


- Run 'interface.py' to see how the model predicts labels for images. Make sure all of the steps above were taken.
```zsh
python3 interface.py
