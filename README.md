# Automatically like AniList activities every minute

## Warning
**Please do not use this**. AniList does not like user accounts being automated for something like this, it might put your account to risk. I'm archiving this repository for good.

## Getting started
The script needs an AniList OAuth access token to interact with the AniList API.
[Follow this guide to learn how to get yours.](https://anilist.gitbook.io/anilist-apiv2-docs/overview/oauth/implicit-grant)

- Rename `.env.example` file to `.env`.
- Paste your access token in the file as directed.
- Install the dependencies:
```
pip install -r requirements.txt
```
- Start the script:
```
python anial.py
```
- Watch it like a few activites every minute on your behalf.
