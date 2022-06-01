# InfinitelyOvercast
Selfhosted, Transparent, Infinite RSS Generator for Overcast Podcasts


## About

  Infinitely Overcast is an infinite RSS Feed Generator for [Overcast](https://overcast.fm). This project, given one or several podcasts, creates a never ending feed of content for Overcast to pull from, while simultaneously ensuring you listen to the entire backlog before repeating any episodes, while pushing new content to the top of the list! InfinitelyOvercast provides this functionality by leveraging Overcast's User OPML export function, which provides listening history and subscribed feed data. True to the spirit of the official Overcast app, this project only parses and generates RSS Feeds, all content is streamed from the listener, thereby providing the content creator with true and accurate listening metrics.

## Authentication

  This project utilizes automated authentication to the Overcast account page. It is **ALWAYS** a bad idea to give an untrusted program access to your raw credentials. Please take a moment to peruse the Python source to independently verify your credentials are not shared beyond the scope implied by this project. As the author, I do however certify that this project only utilizes your credentials as described in this README.
  
  While this project uses none of Overcast's internal APIs, this Author did not obtain permission to leverage the account system in this fashion. Sorry Marco, please reach out if this project is a problem for you and your excellent app. 
  
  The credentials required for authentication to the Overcast platform are stored in either a config file or enviornment variable in **PLAIN TEXT**. This is *highly insecure*, in the event your computer is breached, your credentials are easily accessible. This Author wholeheartedly dissuades anyone and everyone from using this project without first independently researching what data would be availible to an attacker in the event of a compromised account. Furthermore, I encourage any users of this project to create a unique password for use with this project, to prevent the pwning of multiple accounts, should a breach of your machine occur.
  
## Usage

### Python

This project may be run via Python3.9 with the following commands from the project directory.
```bash
python -m pip install requirements.txt #Install Dependencies
```
```bash
python main.py #Start Server
```
The feed will be accessible at http://0.0.0.0:8080

### Docker

This project may be run via docker compose with the following snippet.
```docker
version: "3.8"
services:
  infinitely_overcast:
    image: "zetatauepsilon/infinitelyovercast"
    command: python main.py
    volumes:
      - /path/to/config.json:/python-flask/config.json
    ports:
      - "8080:8080"

```

## Configuration

The project is managed through a `config.json` file, an example of which is given below.

```json
{
  "includeType": "overcastID", //Valid Values: overcastID, title
  "feeds": [],
  "bias": "default", //Valid Values: default, newest, oldest, random
  "username": "",
  "password": "",

  "title": "InfinitelyOvercast",
  "description": "InfinitelyOvercast Beta",
  "url": "https://github.com/ZetaTauEpsilon/InfinitelyOvercast/"
}
```

### Explanation of values

#### ***includeType***
Used to filter subscribed podcasts when determining pertinent listening history.
Valid Values:
- `overcastID` Can be found in overcast.opml
- `title` Podcast Title, must match exactly.

#### ***feeds***
JSON list of values of type given by [includeType](https://github.com/ZetaTauEpsilon/InfinitelyOvercast/new/main?readme=1#includetype)

#### ***bias***
Used to determine ordering out output RSS
Valid Values:
- `default`
  - Orders non-recently listened episodes randomly, with unlistened "New" episodes topping the list.
- `oldest`
  - Orders non-recently listened episodes oldest to newest.
- `newest`
  - Orders non-recently listened episodes newest to oldest.
- `random`
  - Orders non-recently listened episodes randomly.

#### ***username***
Overcast.FM account username

#### ***password***
Overcast.FM account password

#### ***title***
Title of the RSS feed

#### ***description***
Description of the RSS feed

#### ***url***
url of the RSS feed

