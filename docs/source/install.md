# Installation Instructions

The easiest way to install `iglsynth` is  using [Docker](https://www.docker.com/). The installation instructions for docker are available at these links: [Ubuntu](https://docs.docker.com/v17.09/engine/installation/linux/docker-ce/ubuntu/), [Mac](https://docs.docker.com/v17.09/docker-for-mac/install/) and [Windows](https://docs.docker.com/v17.09/docker-for-windows/install/). For users who do not want to use Docker, the installation instructions are given in section [Install from Source](http://localhost:63342/iglsynth/docs/build/install.html#install-from-source).



We provide two docker images aimed at users and developers. 

* **For users:** The docker image has the latest version of `iglsynth` installed along with its dependencies. The docker image can be used as remote interpreter for Python. 
* **For developers:** The docker image only comes with dependencies installed. The developers must mount the repository while creating a docker container, and use docker image as remote interpreter for Python.



The following instructions assume the Python IDE used is [JetBrains PyCharm Professional](https://www.jetbrains.com/pycharm/) which supports [Remote Interpreter using Docker](https://www.jetbrains.com/help/pycharm/using-docker-as-a-remote-interpreter.html).





## Install using Docker: for Users

Assuming PyCharm are already installed and docker service is running. 

1. Get the docker image - `abhibp1993/iglsynth:latest`

   ```bash
   docker pull abhibp1993/iglsynth
   ```

   

2. Configure PyCharm to use Python 3.7 from docker image as remote interpreter as follows. 
   * Create a new project / open a project: <ProjectName>. 
   * Go to `PyCharm --> File --> Settings`.
   * In the left navigation menu go to `Build, Execution and Deployment --> Docker`.
   * Click the `+` to add a new Docker server. Provide a name to server, and select `Unix Socket` for `Connect to Docker daemon with ` section. 
   * In the left navigation menu, go to `Project: <ProjectName> --> Project Interpreter` .
   * Click on gear symbol next to `Project Interpreter` and select `Add`. 
   * In the pop-up window, select `Docker` from left navigation menu. 
   * Select the server you created and set `Image Name: abhibp1993/iglsynth` and `Python Project Interpreter: python3`
   * Select `OK` to exit pop-up window, and then `Apply` and `OK` to exit settings. 
   * The PyCharm will take some time updating skeletons – and you are all set!





## Install using Docker: for Developers

Assuming PyCharm are already installed and docker service is running. 

1. Get the docker image - `abhibp1993/iglsynth:dev`

   ```bash
   docker pull abhibp1993/iglsynth:dev
   ```

   

2. Clone the repository from Github somewhere, say `/home/projects/iglsynth`

   ```bash
   git clone https://github.com/abhibp1993/iglsynth.git
   ```

    It is a patience demanding process! &nbsp;

3. Open the project in PyCharm. 

   * Open PyCharm.

   * Go to `File --> Open`, navigate to `/home/iglsynth`, and select `Open`.

     
   
    &nbsp;

4. Configure PyCharm to use Python 3.7 from docker image as remote interpreter as follows. 

   - Go to `PyCharm --> File --> Settings`.

   - In the left navigation menu go to `Build, Execution and Deployment --> Docker`.

   - Click the `+` to add a new Docker server. Provide a name to server, and select `Unix Socket` for `Connect to Docker daemon with ` section. 

   - In the left navigation menu, go to `Project: <ProjectName> --> Project Interpreter` .

   - Click on gear symbol next to `Project Interpreter` and select `Add`. 

   - In the pop-up window, select `Docker` from left navigation menu. 

   - Select the server you created and set `Image Name: abhibp1993/iglsynth` and `Python Project Interpreter: python3`

   - Select `OK` to exit pop-up window, and then `Apply` and `OK` to exit settings. 

   - The PyCharm will take some time updating skeletons – and you are all set!

     
   
    &nbsp;

5. At this moment, you should be able to run examples, tests using usual run/debug process `Run --> Run <filename>` or `Run --> Debug <filename>`. 

   * It may happen that `Debug` process may not start properly sometime with error saying “ports cannot be opened” or similar. In this case, try restarting PyCharm and Docker service in that case. 

    &nbsp;

   

6. **Generating Documentation:** The docker image comes with documentation tools installed. Follow the instructions to generate documentation. [Note: The instructions are written for Ubuntu, but similar workflow can be followed for Mac/Windows)

   * Open a terminal window and run 

     ```bash
     docker run -it -v /home/projects/iglsynth:/home/iglsynth abhibp1993/iglsynth:dev
     ```

     to create a new container of image while mounting the local `iglsynth` directory at `/home/iglsynth` directory within container.

     

   * Now, navigate to `docs` folder within docker container and run `sphinx-build` as follows, 

     ```bash
     cd /home/iglsynth/docs
     sphinx-build -b html source build 
     ```

     The documentation will be generated in `docs/build` directory, which can be accessed  from `index.html`. 

      

   

## Install from Source

`iglsynth` depends on following C++/Python packages. 

* [Python >= 3.7.x](https://www.python.org/downloads/)
* [graph_tool](https://graph-tool.skewed.de/)
* [spot](https://spot.lrde.epita.fr/)
* [pytest](https://docs.pytest.org/en/latest/index.html)



The packages `graph_tool` and `spot` are both written in C++ and use python binding to expose their respective functionality. All the tools can be installed using `apt-get` package manager for `Ubuntu 19.04` and above. However, for any other operating system (or version of Ubuntu), these packages must be compiled from source (see respective web-pages for instructions). 

**Warning:** `spot` and `graph_tool` have several dependencies that must be installed from source too (due to version requirements). It is a patience demanding process! 

Once the dependencies are installed, installing `iglsynth` can be done using following instructions

```bash
git clone https://github.com/abhibp1993/iglsynth.git
cd iglsynth
python3 setup.py install
```



