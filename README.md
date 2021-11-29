Welcome to the tutorial!
We will learn how we can create a live streaming audio and video app where we can plug our super deep learning models with a few lines of codes! 🔥

We are going to use **Streamlit**, and more specifically amazing **streamlit-webrtc** component to do so.

## First, let's create another website project

We will create a new project directory for the code of our website.

This directory will be located inside of our *projects directory*: `~/code/<user.github_nickname>`.

We will first clone this repository. It can take some times (you are loading a 200 MB tensorflow model).


```bash
cd ~/code/<user.github_nickname>
gh repo clone Yanka13/live-streaming-app
cd live-streaming-app


```
Let's now install all the dependencies needed to run our app locally.
Thenn we will launch example.py and streamlit_app.py to discover how it work.

```bash
pip install -r requirements.txt


```
```bash
streamlit run example.py
```

Easy he ? [streamlit web-rtc](https://github.com/user/repo/blob/branch/other_file.md) did all the magic for us.

Now let's try with the full app and play with it (try to do some [language signs](https://www.google.com/search?q=language+sign&oq=language+sign&aqs=chrome.0.69i59l3j0i10j46i512j69i60l3.3677j0j7&sourceid=chrome&ie=UTF-8) on the webcam !)

```bash
streamlit run streamlit_app.py
```

When your done understanding the code (you can have a look at [this article](https://blog.streamlit.io/how-to-build-the-streamlit-webrtc-component/) to dig more), you are now ready to push the app into production, we wiil do it directly on [streamlit new cloud](https://share.streamlit.io/)
Streamlit Cloud is a new feature from strealit that allow you to push your application very easily.
## Production
First, let's create a remote repository on your **GitHub** account (repo need to be public to use free streamlit cloud services):

``` bash
git init
git remote remove origin
gh repo create
```
Install the very handy **git-lfs** tool, which allow to push for free heavy file > 100 mb to github (free until 1GB of storage per month)! To do that, follow the instruction [here]( https://git-lfs.github.com/) to install the package.
Then type the command  below to push to our heavy deep learning model located in the models folder to our remote repository

``` bash
git lfs install
git lfs track "*.h5"
git add models/model.h5
```
Add now every other files we need as usual, commit and push!

``` bash
git add .
git commit --m "App V0"
git push origin master
```

Now it's time to push our app into streamlit: Go [here](https://share.streamlit.io/), create an account, link it to your github account, click on "create a new app", select your live-streaming-app repository, create you app and... voilà!

