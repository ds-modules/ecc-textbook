# ecc-ai

Repository for AI modules at El Camino College.

![img](https://raw.githubusercontent.com/ds-modules/ecc-textbook/refs/heads/main/modules/_static/ecc-header.png)

Launch links open notebooks on [DataHub](https://elcamino.cloudbank.2i2c.cloud/).

## Chatbot

| Notebook | Launch on DataHub |
|---|---|
| Intro to API Keys and Chatbots | [![Launch DataHub](https://img.shields.io/badge/Launch-DataHub-blue.svg)](https://elcamino.cloudbank.2i2c.cloud/hub/user-redirect/git-pull?repo=https%3A%2F%2Fgithub.com%2Fds-modules%2Fecc-ai&branch=main&urlpath=tree%2Fecc-ai%2Fchatbot%2Fintro_api_keys_chatbot.ipynb) |

The chatbot notebook uses [`chatbot/chat_ui.py`](chatbot/chat_ui.py) for the interactive chat interface.

## Small Models

| Notebook | Launch on DataHub |
|---|---|
| Introduction to AI and LLM Technologies | [![Launch DataHub](https://img.shields.io/badge/Launch-DataHub-blue.svg)](https://elcamino.cloudbank.2i2c.cloud/hub/user-redirect/git-pull?repo=https%3A%2F%2Fgithub.com%2Fds-modules%2Fecc-ai&branch=main&urlpath=tree%2Fecc-ai%2Fsmall-models%2FElCaminoIntrotoAI.ipynb) |

## Bias

| Notebook | Launch on DataHub |
|---|---|
| When AI Learns the Wrong Thing: Auditing Name Bias in a Salary Prediction Model | [![Launch DataHub](https://img.shields.io/badge/Launch-DataHub-blue.svg)](https://elcamino.cloudbank.2i2c.cloud/hub/user-redirect/git-pull?repo=https%3A%2F%2Fgithub.com%2Fds-modules%2Fecc-ai&branch=main&urlpath=tree%2Fecc-ai%2Fbias%2FBob_and_Ray_AI_Ethics_Lab.ipynb) |

## Fruit fly connectome

| Notebook | Launch on DataHub |
|---|---|
| From a Fruit Fly Brain Map to an AI Model | [![Launch DataHub](https://img.shields.io/badge/Launch-DataHub-blue.svg)](https://elcamino.cloudbank.2i2c.cloud/hub/user-redirect/git-pull?repo=https%3A%2F%2Fgithub.com%2Fds-modules%2Fecc-ai&branch=main&urlpath=tree%2Fecc-ai%2Ffruit-fly%2FFrom_a_Fruit_Fly_Brain_Map_to_an_AI_Model.ipynb) |

The notebook reads a six-neuron MaleCNS v1.0 excerpt from [`fruit-fly/data/`](fruit-fly/data/). Provenance and the CC BY 4.0 attribution are in [`fruit-fly/data/README.md`](fruit-fly/data/README.md).

## ChessFly

| Notebook | Launch on DataHub |
|---|---|
| ChessFly | [![Launch DataHub](https://img.shields.io/badge/Launch-DataHub-blue.svg)](https://elcamino.cloudbank.2i2c.cloud/hub/user-redirect/git-pull?repo=https%3A%2F%2Fgithub.com%2Fds-modules%2Fecc-ai&branch=main&urlpath=tree%2Fecc-ai%2Fchessfly%2FChessFly_DataHub_prototype.ipynb) |

Students play the published ChessFly demo from [`chessfly/ChessFly_DataHub_prototype.ipynb`](chessfly/ChessFly_DataHub_prototype.ipynb). The browser downloads the FlyWire wiring and the trained weights. A separate lab, [`chessfly/ChessFly_train_readout_prototype.ipynb`](chessfly/ChessFly_train_readout_prototype.ipynb), has students build a legal-move scorer on activity from that same network. It is not classroom-ready until it has been run on DataHub with `anywidget`. Instructor notes are in [`chessfly/INSTRUCTOR_NOTES.md`](chessfly/INSTRUCTOR_NOTES.md).
