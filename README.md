[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Blockchain Software

## Purpose
Written in python3 this blockchain software was created for educational purposes, here you can learn how to build a blockchain layer 1 software from scratch.

## File Usage

#### While this software is not provided the whole functionallity of blockchain, here you can understand the basic of blockchain technology and needed to be improved.
- **how to created key pair and wallet address**
- **how to created the block**
- **how to chaining the validated block**
- **how to mining using proof-of-work**
- **how to mined genesis block**
- **how to compute merkle trees**
- **how to save into database**


## Running the Program
To test and run the program, simply execute the following command in the terminal:

- git clone https://github.com/ChyKusuma/py-LearnBlockchain.git blockchain-repo
- cd blockchain-repo
- command on your terminal `python3 src/main.py`

## My tests result (Updated)

`Block 2`
- **Previous Hash**: 0000dbeb1289e8baf5e0b029ee49ac746b6628d2063927eef8e486532d617b92
- **Hash**: 0000a3b55fa20cc226840daaaf395dbe0befeeb526d74d305250d110648fa153
- **Transactions Timestamp**: 13 Apr 24 07:49:49

`Block 1`
- **Previous Hash**: 0000ebca739949e3270444c7da9b4e74cd0e5b57b788941c80dece225d45c8c6
- **Hash**: 0000dbeb1289e8baf5e0b029ee49ac746b6628d2063927eef8e486532d617b92
- **Transactions**
  - **Transaction ID**: 273aeaf02833c85b8c560e7f6fb21cbcef08aafb36654087529c9b3d0f6bd0a7
  - **Type**: Coinbase Transaction
  - **Reward Amount**: 10 COINS
- **Timestamp**: 13 Apr 24 07:49:48

`Genesis Block 0`
- **Previous Hash**: None
- **Hash**: 0000ebca739949e3270444c7da9b4e74cd0e5b57b788941c80dece225d45c8c6
- **Timestamp**: 13 Apr 24 07:49:46

## Installation Guide for Python3
If Python3 is not installed on your system, follow these steps to install it:

1. **Linux/Ubuntu**:
   - Open the terminal.
   - Run the following command:
     ```
     sudo apt-get update
     sudo apt-get install python3
     ```

2. **MacOS**:
   - Open a web browser.
   - Go to the [Python website](https://www.python.org/downloads/mac-osx/) and download the latest Python 3 installer.
   - Run the installer and follow the instructions.

3. **Windows**:
   - Open a web browser.
   - Go to the [Python website](https://www.python.org/downloads/windows/) and download the latest Python 3 installer.
   - Run the installer and make sure to check the box that says "Add Python 3.x to PATH".
   - Follow the instructions to complete the installation.


This README provides information about the purpose of the blockchain software, its file usage, how to run the program, and a guide for installing Python3.