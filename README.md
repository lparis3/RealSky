# RealSky

RealSky is a simulation pipeline for the deeplens ML4SCI collaboration. Functionally, RealSky is a wrapper package for lenstronomy and pyhalo that incorporates real astronomical images and utilizes a physically accurate sampling of galaxy and halo parameters. 

Using the pipeline will require the GalaxiesML dataset. The paper explaining the dataset can be found [here](https://arxiv.org/abs/2410.00271v1). The dataset itself can be found [here](https://zenodo.org/records/11117528) and the filtered dataset used to create Model A can be found here[https://drive.google.com/file/d/1mzgEayCSmXnriMgEjR166r2QVIUPQMiZ/view?usp=sharing].

The core dependencies for the pipeline are `numpy`, `scipy`, `matplotlib`, `tqdm`, `torch`, `nflows`,`lenstronomy`, `pyHalo`, `colossus`, `h5py`, `pandas`, `pyyaml`, `scikit-learn`, `seaborn`.

Please refer to the `RealSky_pipeline_tutorial.ipynb` file for more specific instructions on installation, setup, and usage, as well as a more in depth explanation of the modified GalaxiesML dataset used to simulate Model A.
