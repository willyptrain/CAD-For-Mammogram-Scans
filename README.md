# “Development of a Computer Aided System for the Classification of Breast Lesions from Mammogram Scans”

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;My mission for this research focused on using machine learning algorithms in the application of mammography screening. I utilized a support vector machine trained on mammogram lesion numerical records and a convolutional neural network, learning from a collection of digitized mammogram scans. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The support vector machine was trained on numerical values (age, shape, density, margin, radiologist's assessment) with a corresponding scale to represent each characteristic. To find the optimal hyperparameters (C, gamma, and kernel type) for the support vector machine, a genetic algorithm was developed. The genetic algorithm behaved by creating generations of support vector machines, each with their own assigned hyperparameters. The hyperparameters returning the highest accuracy were used more frequently in the production of traits for future generations. Thus, traits most associated with higher accuracies were more prevalent within each successive generation. After 50 generations the fittest, or most accurate, support vector machine was taken from the population and used in testing. The support vector machine returned an accuracy of 89.7% in grouping malignant masses as malignant; for classifying benign lesions as benign, the support vector machine produced an accuracy rating of 68.1%. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A convolutional neural network was then developed, learning from a dataset of a few thousand mammogram scans that had been digitized. The convolutional neural network architecture was modelled after a similar CNN architecture trained to classify the MNIST digit database. Following training of the model, the CNN returned an accuracy of close to 89% in classifying highlighted breast lesions into their respective benign or malignant class. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ultimately, this research highlights the great potential of machine learning applications in the healthcare industry, if not their potential in all areas of industry. I aim to continue learning about the advances in machine learning and how they can be applied to solve real world problems.

<p align="center">
<img src="https://github.com/willyptrain/CAD-For-Mammogram-Scans/blob/master/Screen%20Shot%202019-10-06%20at%209.41.44%20PM.png">
</p>
