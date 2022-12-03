# Randomizer Tool

## Index Table

- [Randomizer Tool](#randomizer-tool)
  - [Index Table](#index-table)
  - [Introduction](#introduction)
  - [Using this Repo](#using-this-repo)
  - [Things you need](#things-you-need)
  - [How to install](#how-to-install)
  - [Running the application locally](#running-the-application-locally)
  - [Generate your own version .exe](#generate-your-own-version-exe)
  - [I generate my mod .zip, What's next?](#i-generate-my-mod-zip-whats-next)
- [Question and Answers](#question-and-answers)
  - [Author and thanks](#author-and-thanks)

## Introduction

This is a tool that allow you to randomize the pokemon from Scarlet and Violet, is still on a alpha version, but I gonna try to keep a consist working on it to make it better.

![Tool Screenshot](https://images.gamebanana.com/img/ss/tools/638a2a73b274d.jpg)

There are several issues, but this not break the experience, as far I know.

Anyway there are so many things that haven't be tested yet, but that's why I released the tool on GameBanana, to have feedback of their experiences.

You can keep a better track of the releases I gonna keep working on in
[Primitive Randomizer Tool](https://gamebanana.com/tools/11402).

## Using this Repo

You can clone this repo to generate your own .exe on your computer if you not feel confident to download it from GameBanana, this work with python so checkout the [How to install](#how-to-install) section for more information.

## Things you need

Things you need to install:
* PyEnv
* Python

For install PyEnv, you can go to the [Install Section](https://github.com/pyenv/pyenv#installation) of the tool and follow the guide

On my case, I use windows so I follow this [Guide](https://github.com/pyenv-win/pyenv-win#quick-start) instead.

>  **Why you use PyEnv and not only Python if are the same internally?**

Well, while working on this, I have problems with certain library and that force me to do it on this way, so in order to try avoiding you can meet this problems also, you can follow this way instead.

Then with PyEnv installed, you will use it to install the last stable version of Python, in my case was the `3.11.0`, you can do it with this:

```
pyenv install -l
```

This will give you the list of all the versions you can install, you can check what is the last stable version on the [Python Download Page](https://www.python.org/downloads/).

After you select which version will install, you can execute

```
pyenv install <version>
```

For example: ```pyenv install 3.11.0```

Then you will make that version of python your global version

```
pyenv global <version>
```

And with that, you install Python

You can check it with

```
python -V
```

## How to install

Just run ```python -m pip install -r requirements.txt``` on the root of this repo and that will install all the dependencies that you need at the moment

## Running the application locally

When you have all the dependencies installed correctly, you can run the application without the need of generating an executable, just use ```python index.py``` and that will start the Tool and you can use it without problems

## Generate your own version .exe

If you want to generate an Executable instead of running the source code, you can run the .sh file called `create-exe.sh`, you need to pass a parameter (I called a version), just for my internal control actually but you can pass whatever you want

```
sh create-exe.sh
```

This will run the process to make your own executable with the static files that need in order to work correctly, once is finish, you will see a folder called `dist` on the root folder, all that folder will be your application folder and you can move it whatever place you want to make use of it

And that's it, now you have your own executable of this tool.

## I generate my mod .zip, What's next?

Now that you can execute the Tool and make your own randomized mod, you can install it using the [Trinity Mod Loader](https://gamebanana.com/tools/11366)

# Question and Answers

> **The randomized mod works on Switch?**

I only test this mod on Ryujinx Emulator (I thinks can also be used on Yuzu, but haven't tested yet), if you want to use it on your Switch, you are on your own risk.

> **Can I randomize every pokemon of the franchise?**

At this moment just the Paldea's Dex is available, that means that you cannot see pokemon like Ultra beast or Hisuian forms... at the moment.

> **The executable is detected as a virus, are you scamming me?**

This is my first time working with executable files, so I think that I missed several "good practices", that's why I bring access to this repo, that way you can see the source code and be aware of what's going on.

> **I see eggs spawning on the overworld, my game will crash if I interact with them?**

Yeah, that's something that I'm not 100% aware about why is happening, but my theory is that when I randomize, the pokemon with diferent forms, like the Paldean Tauros, Squawkabilly or Rotom, need a specific way of be randomized and I'm not doing it, so they become "Bad eggs" instead.

You cannot do anything with this Eggs, you can interact with them but at the moment of start the battle, this will finish instantly, getting no XP nor material.

A funny think is that every egg will be Shiny and Lv. 0.

> **I activated the Items option, but a pokemon I catched don't bring any item**

This is because the randomizer try to force the pokemon to bring an item, but if the item that is try to be set is invalid for be held by a pokemon (like the Miraidon/Koraidon Pokeball), the game will ignore that and just make the pokemon no bring any item.

## Author and thanks

This tool was made entirely by me, `ZadenOwer`.

Special thanks to the people of discord of Pokemon Switch Modding that help me to understand How to get access to the files and How to read it, modify and everything else.

> **"From fans and for fans"** 
