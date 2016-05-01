# Shinsai-Simulator

Term Project for 15-112 at Carnegie Mellon University.

Created by Riki Singh Khorana

### Purpose
This project was initiated to inspire many other product-developers to build a realistic simulator of a _shinsai_ (Japanese word for “earthquake disaster”).

March 11, 2016 marked the fifth year since the Great East Japan Earthquake and Tsunami hit Tohoku, Japan. Although the awareness of preparing for emergencies have risen considerably since the event, there are still many people who are not yet mentally prepared to face the situation. After all, such abnormal events are still considered “fiction” before we face it. This is why I decided to work on a simulation software that could recreate the city that we live in, and show the destruction that a tsunami would cause. Watching realistic scenes of your own town being destroyed will bring shock, but also awareness.

### How to use the app
Download Shinsai-Simulator from this GitHub repository using the Download ZIP button, and unzip the file in a directory that you would remember. If that doesn’t work, use your terminator/command line to download the repository as shown [here](https://help.github.com/articles/importing-a-git-repository-using-the-command-line/).

This app utilizes the Panda3D framework maintained by Carnegie Mellon University. To download the framework, access the Panda3D website via [this link](http://www.panda3d.org/download.php). The "_Panda3D Runtime for End-Users_" should be sufficient in running Shinsai-Simulator. However, I do recommend downloading the "_Panda3D SDK for Developers_" because you can change a few settings of Shinsa-Simulator to your own preferences, and it comes with a lot of sample programs that you can play around with! Panda3D has it’s own version of Python available for use, so you do not have to download Python separately. (To change Panda3D settings to run the program using your own version of Python, refer to [this link](https://www.panda3d.org/manual/index.php/General_Preparation))

Once Panda3D is downloaded, locate your Shinsai-Simulator folder via the Command Line.

`cd exampleDirectory/exampleFolder1/exampleFolder2/Shinsai-Simulator`

Then type in:

`ppython Shinsai-Simulator.py`


The main app controls are gone over in the video below:

<a href="http://www.youtube.com/watch?feature=player_embedded&v=ns1BbU5z5jE
" target="_blank"><img src="http://img.youtube.com/vi/ns1BbU5z5jE/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="540" height="405" border="0" /></a>

### Future Updates
Although this project is only an entry-level one, there are many features that I haven't implemented yet, and plan to do so in the near future.

* City generator
  * Currently, the buildings in the cities are generated randomly, but the city blocks aren't
  * I would like to add an option to place blocks on the terrain on your own


* Building Collision
  * The built in Panda3D collision system did not work well with my method of exploring through the terrain
  * I would like to investigate further in object collision methods so the player wouldn't be cheating through the buildings

* Obstacles
  * Randomly generating obstacles, or having buildings fallen over is a possibility in real-life situations
  * I would like to continue writing more classes and having them being randomly generated on the terrain.

### Note to Advanced Developers
It would be great if someone can take this project and bring to the next level. Things I've imagined but could not build into my projects were things such as:

* Implementing complex wave equations in order to generate a better tsunami model
* Working with Google Earth to use their wonderful model of our earth (They only share terrain info... boo)
* Having an inventories option, so decision making on what to bring is also simulated
* Many more...!

I am open to answering any questions and/or comments regarding my code and ideas.
Please do not hesitate to contact me via my email adress: rkhorana@andrew.cmu.edu
